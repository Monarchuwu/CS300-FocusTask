import styles from './RegisterPage.module.css';

import { callAPITemplate } from '../utils';

import React from 'react';
import { useNavigate } from 'react-router-dom';

import {
    TextField,
    Button,
    Alert, 
} from '@mui/material';

import { Helmet } from 'react-helmet';

function RegisterPage() {
    const navigate = useNavigate();
    const [username, setUsername] = React.useState('');
    const [email, setEmail] = React.useState('');
    const [password, setPassword] = React.useState('');
    const [message, setMessage] = React.useState('');

    const callRegisterAPI = (username, email, password) => {
        callAPITemplate(
            'http://localhost:8000/todolist/api/user/register',
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
        if (!isValidEmail(email)) {
            setMessage('Email is invalid!');
            return;
        }
        callRegisterAPI(username, email, password);
    }
    return (
        <div>
            <Helmet>
                <title>Sign Up - FocusTask</title>
            </Helmet>
            <div id="SignUpForm">
                <h1>Sign up</h1>
                <div>
                    <TextField type="text" name="username" value={username} 
                        sx={{ mb: '24px' }} label="Username" onChange={(e) => setUsername(e.target.value)} required/>
                    <br />
                    <TextField type="email" name="email" value={email}
                        sx={{ mb: '24px' }} label="Email" onChange={(e) => setEmail(e.target.value)} required />
                    <br />
                    <TextField type="password" name="password" value={password} 
                        sx={{ mb: '24px' }} label="Password" onChange={(e) => setPassword(e.target.value)} required/>
                    <br />
                    <Button variant='contained' type="submit" sx={{ mb: '24px' }}
                        onClick={() => handleSubmit()}>Create Account</Button>
                </div>
                <Alert severity="error">{message}</Alert>
                <Button variant='text' onClick={() => navigate('/signin')}>Already had an account? Log in</Button>
            </div>
        </div>
    );
}

export default RegisterPage;