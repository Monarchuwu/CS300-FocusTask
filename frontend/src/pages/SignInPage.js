import { callAPITemplate } from '../utils';

import React from 'react';
import { useNavigate } from 'react-router-dom';

import {
    TextField,
    Button,
} from '@mui/material';


function SignInPage() {
    const navigate = useNavigate();
    const [email, setEmail] = React.useState('');
    const [password, setPassword] = React.useState('');
    const [message, setMessage] = React.useState('');

    const callSignInAPI = (email, password) => {
        callAPITemplate(
            'http://localhost:8000/todolist/api/user/signin',
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
        if (!isValidEmail(email)) {
            setMessage('Email is invalid!');
            return;
        }
        callSignInAPI(email, password);
    }
    return (
        <form id="LogInForm">
            <h1>Log In</h1>
            <div>
                <TextField id="email" label="Email" value={email} 
                    sx={{ mb: '24px' }} onChange={(e) => setEmail(e.target.value)} required/>
                <br />
                <TextField id="password" label="Password" type="password" 
                    value={password} sx={{ mb: '24px' }} 
                    onChange={(e) => setPassword(e.target.value)} required/>
                <br />
                <Button variant="contained" type="submit" onClick={() => handleSubmit()}>Log In</Button>
            </div>
            <p>{message}</p>
            <Button variant="text" onClick={() => navigate('/register')}>Don’t have an account? Sign Up</Button>
        </form>
    );
}

export default SignInPage;