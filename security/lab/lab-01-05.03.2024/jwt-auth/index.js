const express = require('express');
const onFinished = require('on-finished');
const bodyParser = require('body-parser');
const path = require('path');
const jwt = require('jsonwebtoken');
const port = 3000;

const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

const SECRET_KEY = 'thats a super secret key';

const users = [
    {
        login: 'Login',
        password: 'Password',
        username: 'Username',
    },
    {
        login: 'Login1',
        password: 'Password1',
        username: 'Username1',
    }
]

app.use((req, res, next) => {
    const token = req.get('Authorization');

    if (token) {
        jwt.verify(token, SECRET_KEY, (err, decoded) => {
            if (err) {
                return res.status(401).send('Invalid token');
            }
            req.user = decoded;
            next();
        });
    } else {
        next();
    }
});

app.get('/', (req, res) => {
    const token = req.get('Authorization');
    if (token) {
        try {
            const decoded = jwt.verify(token, SECRET_KEY);
            console.log(`Valid token received: ${token}`);
            res.json({ username: decoded.username, logout: 'http://localhost:3000/logout' });
        } catch (e) {
            res.status(401).send('Invalid token');
        }
    } else {
        res.sendFile(path.join(__dirname + '/index.html'));
    }
});

app.get('/logout', (req, res) => {
    res.redirect('/');
});

app.post('/api/login', (req, res) => {
    const { login, password } = req.body;

    const user = users.find(u => u.login === login && u.password === password);

    if (user) {
        const token = jwt.sign({
            username: user.username,
            login: user.login
        }, SECRET_KEY, { expiresIn: '1h' });
        console.log(`User logged in: ${user.username}, Token: ${token}`);
        res.json({ token });
    } else {
        res.status(401).send('Login failed');
    }
});

app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
});
