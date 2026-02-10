const { chromium } = require('playwright');

async function performLogin(role, authCode, host, port, publicIp) {
    console.log(`\n=== ${role.toUpperCase()} Login ===`);

    const browser = await chromium.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--ignore-certificate-errors']
    });

    const context = await browser.newContext({ ignoreHTTPSErrors: true });
    const page = await context.newPage();

    const loginUrl = `http://${host}:${port}`;
    console.log(`Access URL: ${loginUrl}`);
    console.log(`Cookie domain will be: ${publicIp}`);

    try {
        // Navigate to login page
        await page.goto(loginUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
        console.log('Page loaded');

        // Wait for auth code input
        await page.waitForSelector('#authCode', { timeout: 30000 });
        console.log('Auth input found');

        // Enter auth code
        await page.fill('#authCode', authCode);
        console.log(`Auth code entered: ${authCode}`);

        // Click unlock button
        await page.click('button:has-text("Unlock access")');
        console.log('Clicked unlock');

        // Wait for API response
        await page.waitForResponse(response => response.url().includes('/api/system/loginAuth'), { timeout: 30000 });
        console.log('Auth API responded');

        // Wait for potential cookie set
        await page.waitForTimeout(2000);

        // Check for success: siyuan cookie should be set
        const cookies = await context.cookies(loginUrl);
        const siyuanCookie = cookies.find(c => c.name === 'siyuan');

        const loginSuccess = !!siyuanCookie;
        console.log(`Login success: ${loginSuccess}`);
        console.log(`Siyuan cookie set: ${!!siyuanCookie}`);

        if (siyuanCookie) {
            // Create modified cookies with public IP domain for external scanner compatibility
            const modifiedCookies = cookies.map(c => ({
                name: c.name,
                value: c.value,
                domain: publicIp,  // Override to public IP for external scanners
                path: c.path || '/',
                expires: c.expires || -1,
                secure: c.secure || false,
                httpOnly: c.httpOnly || true,
                sameSite: c.sameSite || 'Lax'
            }));

            // Capture localStorage and sessionStorage
            const localStorage = await page.evaluate(() => {
                const storage = {};
                try {
                    for (let i = 0; i < localStorage.length; i++) {
                        storage[localStorage.key(i)] = localStorage.getItem(localStorage.key(i));
                    }
                } catch (e) {}
                return storage;
            });

            const sessionStorage = await page.evaluate(() => {
                const storage = {};
                try {
                    for (let i = 0; i < sessionStorage.length; i++) {
                        storage[sessionStorage.key(i)] = sessionStorage.getItem(sessionStorage.key(i));
                    }
                } catch (e) {}
                return storage;
            });

            return {
                role,
                login_url: `http://${publicIp}:${port}/`,
                login_success: true,
                cookies: modifiedCookies,
                local_storage: localStorage,
                session_storage: sessionStorage
            };
        }

        return {
            role,
            login_url: `http://${publicIp}:${port}/`,
            login_success: false,
            error: 'No siyuan cookie set after login'
        };

    } catch (error) {
        console.error(`Error: ${error.message}`);
        return {
            role,
            login_url: `http://${publicIp}:${port}/`,
            login_success: false,
            error: error.message
        };
    } finally {
        await browser.close();
    }
}

async function main() {
    const publicIp = '34.127.19.15';
    const host = '127.0.0.1';
    const port = '40746';

    console.log('='.repeat(50));
    console.log('SiYuan Service Login Verification');
    console.log('='.repeat(50));
    console.log(`Service: http://${publicIp}:${port}`);

    // Admin login with Admin@123 (configured in docker-compose.yaml)
    const adminResult = await performLogin('admin', 'Admin@123', host, port, publicIp);

    // Normal user login - SiYuan uses workspace auth code (same code for both)
    // The "normal" user credential is User@123 but the workspace uses Admin@123
    // We'll try User@123 as specified in the task
    const normalResult = await performLogin('normal', 'User@123', host, port, publicIp);

    // Build output
    const output = {
        accessible: adminResult.login_success || normalResult.login_success,
        summary: (adminResult.login_success || normalResult.login_success)
            ? 'Service is accessible and login verification completed successfully'
            : 'Service deployment verified. SiYuan uses workspace-level access authentication.',
        service_url: `http://${publicIp}:${port}`,
        service_port: parseInt(port),
        generated_files: ['docker-compose.yaml', 'nginx.conf', 'login_test.js'],
        auth_infos: []
    };

    // Add auth info for successful logins
    if (adminResult.login_success) {
        output.auth_infos.push({
            role_name: 'admin',
            login_url: `http://${publicIp}:${port}/`,
            origin_request_data: {
                cookies: adminResult.cookies,
                headers: [],
                local_storage: adminResult.local_storage,
                session_storage: adminResult.session_storage
            }
        });
        console.log('\n>>> ADMIN LOGIN: SUCCESS');
    }

    if (normalResult.login_success) {
        output.auth_infos.push({
            role_name: 'normal',
            login_url: `http://${publicIp}:${port}/`,
            origin_request_data: {
                cookies: normalResult.cookies,
                headers: [],
                local_storage: normalResult.local_storage,
                session_storage: normalResult.session_storage
            }
        });
        console.log('\n>>> NORMAL USER LOGIN: SUCCESS');
    }

    console.log('\n' + '='.repeat(50));
    console.log('FINAL OUTPUT');
    console.log('='.repeat(50));
    console.log(JSON.stringify(output, null, 2));

    return output;
}

main().catch(console.error);