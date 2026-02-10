const express = require('express');
const carbone = require('./lib');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static('templates'));

// Root endpoint - returns service status
app.get('/', (req, res) => {
  res.json({
    service: 'carbone',
    version: '3.5.6',
    status: 'running',
    endpoints: {
      health: 'GET /health',
      templates: 'GET /templates',
      render: 'POST /render'
    }
  });
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'carbone' });
});

// Example render endpoint using Carbone
app.post('/render', (req, res) => {
  const { template, data, options } = req.body;

  if (!template) {
    return res.status(400).json({ error: 'template is required' });
  }

  const templatePath = path.join(__dirname, 'templates', template);

  fs.readFile(templatePath, (err, buffer) => {
    if (err) {
      return res.status(404).json({ error: 'Template not found' });
    }

    carbone.addTemplate(template, buffer, (err) => {
      if (err) {
        return res.status(500).json({ error: 'Failed to add template' });
      }

      carbone.render(template, data || {}, options || {}, (err, result) => {
        if (err) {
          return res.status(500).json({ error: err.message });
        }

        // If result is a buffer, send it directly
        if (Buffer.isBuffer(result)) {
          res.setHeader('Content-Disposition', 'attachment; filename=report.pdf');
          return res.send(result);
        }

        // If result is a path, read and send the file
        if (typeof result === 'string') {
          return res.sendFile(result, (err) => {
            if (err) {
              res.status(500).json({ error: 'Failed to send file' });
            }
          });
        }

        res.json({ reportName: result });
      });
    });
  });
});

// List available templates
app.get('/templates', (req, res) => {
  const templatesDir = path.join(__dirname, 'templates');
  fs.readdir(templatesDir, (err, files) => {
    if (err) {
      return res.json([]);
    }
    res.json(files.filter(f => f.endsWith('.docx') || f.endsWith('.xlsx') || f.endsWith('.odt')));
  });
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Carbone service running on port ${PORT}`);
});