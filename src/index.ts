import express from 'express';

const app = express();
const PORT = process.env.PORT || 3000;

app.get('/', (req, res) => {
    res.send('Welcome to PRAX SHS 2025!');
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});