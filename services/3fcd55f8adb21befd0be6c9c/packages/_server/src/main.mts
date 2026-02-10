import { writeSync } from 'node:fs';
import { createServer } from 'http';
import { run } from './server.mjs';

process.on('unhandledRejection', (error, promise) => {
    // Will print "unhandledRejection err is not defined"
    console.log('Unhandled Rejection at:', promise, 'reason:', error);
});

process.on('uncaughtException', (error, origin) => {
    writeSync(process.stderr.fd, `Caught exception: ${error}\n` + `Exception origin: ${origin}`);
});

// process.on('uncaughtExceptionMonitor', (error, origin) => {
//     writeSync(process.stderr.fd, `Caught exception: ${error}\n` + `Exception origin: ${origin}`);
// });

const port = process.env.PORT ? parseInt(process.env.PORT, 10) : 3000;
const isHttpMode = process.env.HTTP_MODE === 'true';

if (isHttpMode) {
    // Simple HTTP server for health checks and basic API
    const server = createServer((req, res) => {
        // CORS headers
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
        res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

        if (req.method === 'OPTIONS') {
            res.writeHead(200);
            res.end();
            return;
        }

        const url = new URL(req.url, `http://localhost:${port}`);
        const pathname = url.pathname;

        if (pathname === '/health' || pathname === '/') {
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ status: 'healthy', service: 'code-spell-checker-server' }));
        } else if (pathname === '/api/info') {
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({
                name: 'code-spell-checker-server',
                version: '2.0.0',
                description: 'Spell Checker Language Server',
                endpoints: {
                    health: 'GET /health',
                    info: 'GET /api/info'
                }
            }));
        } else {
            res.writeHead(404, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Not found' }));
        }
    });

    server.listen(port, () => {
        console.log(`HTTP server listening on port ${port}`);
    });

    server.on('error', (err) => {
        console.error('Server error:', err);
        process.exit(1);
    });
} else {
    run();
}
