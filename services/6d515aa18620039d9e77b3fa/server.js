const express = require('express');
const limdu = require('./index');

const app = express();
const PORT = process.env.PORT || 3000;

// Health check endpoint
app.get('/', (req, res) => {
  res.json({
    status: 'ok',
    service: 'limdu',
    message: 'Machine learning library is running'
  });
});

// Expose limdu classifiers info
app.get('/classifiers', (req, res) => {
  res.json({
    available: Object.keys(limdu.classifiers || {}),
    features: Object.keys(limdu.features || {}),
    formats: Object.keys(limdu.formats || {}),
    utils: Object.keys(limdu.utils || {})
  });
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Limdu service running on port ${PORT}`);
});