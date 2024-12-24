import { callAPITemplate } from '../utils';

import React from 'react';
import { useNavigate } from 'react-router-dom';

function SignInPage() {
    const navigate = useNavigate();
    const [email, setEmail] = React.useState('');
    const [password, setPassword] = React.useState('');
    const [message, setMessage] = React.useState('');

    const callSignInAPI = (email, password) => {
        callAPITemplate(
            'todolist/api/user/signin',
            JSON.stringify({ "email": email, "password": password }),
            (data) => {
                const authToken = data.authenticationToken;
                localStorage.setItem('authToken', authToken);
                navigate('/');
            },
            (message) => setMessage(message || 'An error occurred'),
            (e) => setMessage('Error: ' + e.message)
        )
    }

    const isValidEmail = (email) => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    const handleSubmit = () => {
        if (email === '' || password === '') {
            setMessage('Please fill in all fields');
            return;
        }
        if (!isValidEmail(email)) {
            setMessage('Email is invalid!');
            return;
        }
        callSignInAPI(email, password);
    }
    return (
        <div>
            <h1>Sign In</h1>
            <div>
                <label>
                    Email:
                    <input type="email" name="email" value={email} onChange={(e) => setEmail(e.target.value)} />
                </label>
                <br />
                <label>
                    Password:
                    <input type="password" name="password" value={password} onChange={(e) => setPassword(e.target.value)} />
                </label>
                <br />
                <button type="submit" onClick={() => handleSubmit()}>Sign In</button>
            </div>
            <p>{message}</p>
            <button onClick={() => navigate('/register')}>Sign Up</button>
        </div>
    );
}

export default SignInPage;