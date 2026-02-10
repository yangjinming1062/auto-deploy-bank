const { chromium } = require('playwright');
const fs = require('fs');

async function loginAndCapture(url, authCode, role) {
    console.log(`\n========================================`);
    console.log(`Login attempt for ${role} account`);
    console.log(`URL: ${url}`);
    console.log(`Auth Code: ${authCode}`);
    console.log(`========================================\n`);

    const browser = await chromium.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const context = await browser.newContext({
        acceptDownloads: true,
        ignoreHTTPSErrors: true
    });

    const page = await context.newPage();

    // Capture console messages
    const consoleLogs = [];
    page.on('console', msg => {
        consoleLogs.push({ type: msg.type(), text: msg.text() });
    });

    try {
        // Navigate to the login page
        console.log('Navigating to login page...');
        await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
        console.log('Page loaded successfully');

        // Wait for the page to be interactive
        await page.waitForLoadState('domcontentloaded');
        await page.waitForTimeout(1000);

        // Check if we're already on the application (already logged in)
        const pageContent = await page.content();
        if (pageContent.includes('Auth failed') || pageContent.includes('auth')) {
            console.log('Authentication required, proceeding with login...');
        }

        // Look for the password/auth code input
        const inputSelector = 'input[type="password"], input[placeholder*="auth"], input[placeholder*="code"], input[placeholder*="Access"]';
        let inputFound = false;

        try {
            await page.waitForSelector(inputSelector, { timeout: 5000 });
            inputFound = true;
            console.log('Auth input field found');
        } catch (e) {
            console.log('Standard auth input not found, trying alternative selectors...');
        }

        if (!inputFound) {
            // Try to find any input field
            const inputs = await page.$$('input');
            if (inputs.length > 0) {
                inputFound = true;
                console.log(`Found ${inputs.length} input fields`);
            }
        }

        // Fill in the auth code
        console.log('Filling auth code...');
        await page.fill(inputSelector, authCode);

        // Check "Remember me" if checkbox exists
        const rememberCheckbox = await page.$('input[type="checkbox"]');
        if (rememberCheckbox) {
            const isChecked = await rememberCheckbox.isChecked();
            if (!isChecked) {
                await rememberCheckbox.check();
                console.log('Checked "Remember me"');
            }
        }

        // Click the login/unlock button
        console.log('Clicking unlock button...');
        const buttonSelectors = [
            'button:has-text("Unlock")',
            'button:has-text("Login")',
            'button[type="submit"]',
            'button:has-text("Sign")',
            'button'
        ];

        for (const selector of buttonSelectors) {
            const button = await page.$(selector);
            if (button) {
                await button.click();
                console.log(`Clicked button: ${selector}`);
                break;
            }
        }

        // Wait for navigation/login to complete
        await page.waitForTimeout(3000);
        await page.waitForLoadState('networkidle');

        // Check if login was successful
        const finalUrl = page.url();
        console.log(`Current URL after login attempt: ${finalUrl}`);

        const finalContent = await page.content();
        const loginSuccess = !finalContent.includes('Auth failed') ||
                            finalContent.includes('workspace') ||
                            finalContent.includes('notebook') ||
                            finalContent.includes('dashboard');

        console.log(`\nLogin status: ${loginSuccess ? 'SUCCESS' : 'FAILED/NEEDS VERIFICATION'}`);

        // Capture session data
        console.log('\nCapturing session data...');

        // Get all cookies
        const cookies = await context.cookies();
        console.log(`Cookies captured: ${cookies.length}`);

        // Get LocalStorage data
        const localStorageData = await page.evaluate(() => {
            const data = {};
            for (let i = 0; i < localStorage.length; i++) {
                const key = localStorage.key(i);
                data[key] = localStorage.getItem(key);
            }
            return data;
        });
        console.log(`LocalStorage keys captured: ${Object.keys(localStorageData).length}`);

        // Get SessionStorage data
        const sessionStorageData = await page.evaluate(() => {
            const data = {};
            for (let i = 0; i < sessionStorage.length; i++) {
                const key = sessionStorage.key(i);
                data[key] = sessionStorage.getItem(key);
            }
            return data;
        });
        console.log(`SessionStorage keys captured: ${Object.keys(sessionStorageData).length}`);

        // Prepare result object
        const result = {
            role: role,
            login_url: url,
            login_success: loginSuccess,
            final_url: finalUrl,
            cookies: cookies.map(c => ({
                name: c.name,
                value: c.value,
                domain: c.domain,
                path: c.path,
                expires: c.expires,
                secure: c.secure,
                httpOnly: c.httpOnly,
                sameSite: c.sameSite
            })),
            local_storage: localStorageData,
            session_storage: sessionStorageData,
            console_logs: consoleLogs
        };

        console.log('\nSession data captured successfully!');
        return result;

    } catch (error) {
        console.error(`Error during login: ${error.message}`);
        return {
            role: role,
            login_url: url,
            login_success: false,
            error: error.message,
            cookies: [],
            local_storage: {},
            session_storage: {}
        };
    } finally {
        await browser.close();
    }
}

// Main execution
async function main() {
    const args = process.argv.slice(2);
    const url = args[0] || 'http://34.127.19.15:42045/check-auth';
    const authCode = args[1] || 'Admin@123';
    const role = args[2] || 'admin';

    console.log('========================================');
    console.log('SiYuan Login Capture Script');
    console.log('========================================');

    const result = await loginAndCapture(url, authCode, role);

    // Save result to file
    const outputFile = `login-result-${role}.json`;
    fs.writeFileSync(outputFile, JSON.stringify(result, null, 2));
    console.log(`\nResults saved to ${outputFile}`);

    // Print summary
    console.log('\n========================================');
    console.log('RESULT SUMMARY');
    console.log('========================================');
    console.log(`Role: ${result.role}`);
    console.log(`Login URL: ${result.login_url}`);
    console.log(`Login Success: ${result.login_success}`);
    console.log(`Cookies: ${result.cookies.length}`);
    console.log(`LocalStorage Keys: ${Object.keys(result.local_storage).length}`);
    console.log(`SessionStorage Keys: ${Object.keys(result.session_storage).length}`);

    if (result.cookies.length > 0) {
        console.log('\nCookie Domains:');
        result.cookies.forEach(c => {
            console.log(`  - ${c.name}: domain=${c.domain}`);
        });
    }
}

main().catch(console.error);