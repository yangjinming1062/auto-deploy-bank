const express = require('express');
const qs = require('./lib/index');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get('/', (req, res) => {
    res.json({
        name: 'qs',
        description: 'A querystring parser that supports nesting and arrays',
        version: require('./package.json').version
    });
});

app.get('/parse', (req, res) => {
    const { url } = req.query;
    if (!url) {
        return res.status(400).json({ error: 'Missing url query parameter' });
    }
    try {
        const parsed = qs.parse(url);
        res.json({ parsed });
    } catch (e) {
        res.status(400).json({ error: e.message });
    }
});

app.get('/stringify', (req, res) => {
    const { obj } = req.query;
    if (!obj) {
        return res.status(400).json({ error: 'Missing obj query parameter' });
    }
    try {
        const parsed = JSON.parse(obj);
        const stringified = qs.stringify(parsed);
        res.json({ stringified });
    } catch (e) {
        res.status(400).json({ error: e.message });
    }
});

app.listen(PORT, () => {
    console.log(`qs library service running on port ${PORT}`);
});