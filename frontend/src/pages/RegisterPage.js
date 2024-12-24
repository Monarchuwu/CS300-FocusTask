import styles from './RegisterPage.module.css';

import { callAPITemplate } from '../utils';

import React from 'react';
import { useNavigate } from 'react-router-dom';

function RegisterPage() {
    const navigate = useNavigate();
    const [username, setUsername] = React.useState('');
    const [email, setEmail] = React.useState('');
    const [password, setPassword] = React.useState('');
    const [message, setMessage] = React.useState('');

    const callRegisterAPI = (username, email, password) => {
        callAPITemplate(
            'todolist/api/user/register',
            JSON.stringify({ "username": username, "email": email, "password": password }),
            (data) => setMessage('User registered successfully!'),
            (message) => setMessage(message || 'An error occurred'),
            (e) => setMessage('Error: ' + e.message)
        )
    }

    const isValidEmail = (email) => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    const handleSubmit = () => {
        if (username === '' || email === '' || password === '') {
            setMessage('Please fill in all fields');
            return;
        }
        if (!isValidEmail(email)) {
            setMessage('Email is invalid!');
            return;
        }
        callRegisterAPI(username, email, password);
    }
    return (
        <div>
            <h1>Register</h1>
            <div>
                <label>
                    Username:
                    <input type="text" name="username" value={username} onChange={(e) => setUsername(e.target.value)} />
                </label>
                <br />
                <label>
                    Email:
                    <input type="email" name="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
                </label>
                <br />
                <label>
                    Password:
                    <input type="password" name="password" value={password} onChange={(e) => setPassword(e.target.value)} />
                </label>
                <br />
                <button type="submit" onClick={() => handleSubmit()}>Register</button>
            </div>
            <p>{message}</p>
            <button onClick={() => navigate('/signin')}>Sign In</button>
        </div>
    );
}

export default RegisterPage;