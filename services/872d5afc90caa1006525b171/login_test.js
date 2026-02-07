const { chromium } = require('playwright');

const PUBLIC_IP = '34.127.19.15';
const PORT = 40436;
const BASE_URL = `http://${PUBLIC_IP}:${PORT}`;

const accounts = [
  { role_type: 'admin', username: 'admin', password: 'password', login_url: '/login' },
  { role_type: 'normal', username: 'testuser', password: 'password', login_url: '/login' }
];

async function captureSessionData(page) {
  const cookies = await page.context().cookies();
  const formattedCookies = cookies.map(c => ({
    name: c.name,
    value: c.value,
    domain: c.domain,
    path: c.path || '/',
    expires: c.expires,
    httpOnly: c.httpOnly,
    secure: c.secure,
    sameSite: c.sameSite || 'Lax'
  }));

  return {
    cookies: formattedCookies,
    headers: [],
    local_storage: {},
    session_storage: {}
  };
}

async function login(page, account) {
  const loginUrl = `${BASE_URL}${account.login_url}`;
  console.log(`Login URL: ${loginUrl}`);

  try {
    // Go directly to login page
    await page.goto(loginUrl, { waitUntil: 'load', timeout: 30000 });
    await page.waitForSelector('input[name="username"]', { timeout: 10000 });

    const title = await page.title();
    console.log(`Page title: ${title}`);

    await page.fill('input[name="username"]', account.username);
    console.log('Filled username');

    await page.fill('input[name="password"]', account.password);
    console.log('Filled password');

    await page.click('button[type="submit"]');
    console.log('Clicked submit');

    await page.waitForTimeout(3000);

    const currentUrl = page.url();
    console.log(`URL after login: ${currentUrl}`);

    // Check if login failed
    if (currentUrl.includes('/login?error') || currentUrl.includes('error=true')) {
      console.log(`Login FAILED for ${account.username}`);
      return null;
    }

    console.log(`Login SUCCESS for ${account.username}`);
    const sessionData = await captureSessionData(page);
    console.log(`Cookies: ${sessionData.cookies.length}`);

    return {
      role_name: account.role_type,
      login_url: loginUrl,
      origin_request_data: sessionData
    };

  } catch (error) {
    console.log(`Error: ${error.message}`);
    return null;
  }
}

async function main() {
  const authInfos = [];
  let browser = null;

  try {
    browser = await chromium.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    for (const account of accounts) {
      const context = await browser.newContext({ ignoreHTTPSErrors: true });
      const page = await context.newPage();

      const result = await login(page, account);
      if (result) {
        authInfos.push(result);
        console.log(`Success: ${account.role_type}`);
      } else {
        console.log(`Failed: ${account.role_type}`);
      }
      await context.close();
    }

  } catch (error) {
    console.log(`Error: ${error.message}`);
  } finally {
    if (browser) await browser.close();
  }

  const result = {
    accessible: authInfos.length > 0,
    summary: authInfos.length === accounts.length
      ? 'Service is accessible and both login accounts verified successfully'
      : `Service accessible but ${authInfos.length}/${accounts.length} login(s) successful`,
    service_url: BASE_URL,
    service_port: PORT,
    generated_files: ['/home/ubuntu/deploy-projects/872d5afc90caa1006525b171/login_test.js'],
    auth_infos: authInfos
  };

  console.log('\n=== RESULT ===');
  console.log(JSON.stringify(result, null, 2));
}

main();
