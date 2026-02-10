const { chromium } = require('playwright');
const fs = require('fs');

async function loginNormalUser(url, username, password, role) {
    console.log(`\n========================================`);
    console.log(`Normal User Login: ${role}`);
    console.log(`URL: ${url}`);
    console.log(`Username: ${username}`);
    console.log(`========================================\n`);

    const browser = await chromium.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const context = await browser.newContext({
        acceptDownloads: true,
        ignoreHTTPSErrors: true,
        // HTTP Basic Auth credentials
        httpCredentials: {
            username: username,
            password: password
        }
    });

    const page = await context.newPage();

    try {
        // Navigate to the publish service
        console.log('Navigating to publish service...');
        await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
        console.log('Page loaded successfully');

        // Wait for potential redirects
        await page.waitForTimeout(2000);
        await page.waitForLoadState('networkidle');

        // Capture session data
        console.log('\nCapturing session data...');

        // Get all cookies
        const cookies = await context.cookies();
        console.log(`Cookies captured: ${cookies.length}`);

        // Get LocalStorage data
        const localStorageData = await page.evaluate(() => {
            const data = {};
            try {
                for (let i = 0; i < localStorage.length; i++) {
                    const key = localStorage.key(i);
                    data[key] = localStorage.getItem(key);
                }
            } catch (e) {
                console.log('LocalStorage not accessible');
            }
            return data;
        });
        console.log(`LocalStorage keys captured: ${Object.keys(localStorageData).length}`);

        // Get SessionStorage data
        const sessionStorageData = await page.evaluate(() => {
            const data = {};
            try {
                for (let i = 0; i < sessionStorage.length; i++) {
                    const key = sessionStorage.key(i);
                    data[key] = sessionStorage.getItem(key);
                }
            } catch (e) {
                console.log('SessionStorage not accessible');
            }
            return data;
        });
        console.log(`SessionStorage keys captured: ${Object.keys(sessionStorageData).length}`);

        // Prepare result object
        const result = {
            role: role,
            login_url: url,
            login_success: cookies.length > 0,
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
            session_storage: sessionStorageData
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
    const url = args[0] || 'http://34.127.19.15:42046/';
    const username = args[1] || 'normal';
    const password = args[2] || 'User@123';
    const role = args[3] || 'normal';

    console.log('========================================');
    console.log('SiYuan Normal User Login Capture');
    console.log('========================================');

    const result = await loginNormalUser(url, username, password, role);

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
        console.log('\nCookie Details:');
        result.cookies.forEach(c => {
            console.log(`  - ${c.name}: domain=${c.domain}, path=${c.path}, httpOnly=${c.httpOnly}`);
        });
    }
}

main().catch(console.error);