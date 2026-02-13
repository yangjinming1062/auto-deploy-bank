const http = require('http');
const ts = require('./built/local/typescript.js');
const path = require('path');
const fs = require('fs');

const PORT = process.env.PORT || 3000;

function compileTypeScript(code, filename) {
  const compilerOptions = {
    target: ts.ScriptTarget.ES2020,
    module: ts.ModuleKind.CommonJS,
    strict: true,
    esModuleInterop: true,
    skipLibCheck: true,
    noEmitOnError: false,
    outDir: '/tmp',
    moduleResolution: ts.ModuleResolutionKind.Bundler
  };

  // Create a virtual file system
  const files = {};
  const outputFiles = [];

  // Create the input file in memory
  files[filename] = { version: '0', scriptSnapshot: ts.ScriptSnapshot.fromString(code) };

  // Create custom host
  const host = {
    getSourceFile(name, languageVersion) {
      if (name === filename) {
        return ts.createSourceFile(name, code, languageVersion, true);
      }
      const file = files[name];
      if (file) {
        return ts.createSourceFile(name, file.scriptSnapshot.getText(0), languageVersion, true);
      }
      return undefined;
    },
    getDefaultLibFileName: () => 'lib.d.ts',
    writeFile: (name, text) => {
      outputFiles.push({ name, text });
    },
    getCurrentDirectory: () => '/',
    getCanonicalFileName: (name) => name,
    useCaseSensitiveFileNames: () => true,
    getNewLine: () => '\n',
    fileExists: (name) => name in files,
    readFile: () => undefined,
    directoryExists: () => false,
    getDirectories: () => []
  };

  const program = ts.createProgram([filename], compilerOptions, host);
  const emitResult = program.emit();
  const allDiagnostics = ts.getPreEmitDiagnostics(program).concat(emitResult.diagnostics);

  return {
    outputFiles,
    diagnostics: allDiagnostics
  };
}

const server = http.createServer((req, res) => {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  if (req.method === 'POST' && req.url === '/compile') {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      try {
        const { code, filename = 'input.ts' } = JSON.parse(body);
        const result = compileTypeScript(code, filename);

        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({
          success: true,
          output: result.outputFiles[0]?.text || '',
          diagnostics: result.diagnostics.map(d => ({
            message: ts.flattenDiagnosticMessageText(d.messageText, '\n'),
            category: ts.DiagnosticCategory[d.category],
            code: d.code
          }))
        }));
      } catch (error) {
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: false, error: error.message }));
      }
    });
  } else if (req.method === 'GET' && req.url === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'ok', version: ts.version }));
  } else if (req.method === 'GET' && req.url === '/') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      service: 'TypeScript Compiler Service',
      version: ts.version,
      endpoints: {
        'GET /': 'This info',
        'GET /health': 'Health check',
        'POST /compile': 'Compile TypeScript code'
      }
    }));
  } else {
    res.writeHead(404);
    res.end('Not Found');
  }
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`TypeScript compiler service running on port ${PORT}`);
});