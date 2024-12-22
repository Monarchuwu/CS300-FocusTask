import { callAPITemplate } from '../utils';

import React from 'react';
import { useNavigate } from 'react-router-dom';

import {
    TextField,
    Button,
    Alert,
    Grid2 as Grid
} from '@mui/material';

import { Helmet } from 'react-helmet';

import Introduction from '../components/Introduction';

import LogoText from '../components/LogoText';


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
        <div>
            <Helmet>
                <title>Log In - FocusTask</title>
            </Helmet>
            <Grid container spacing={2} justifyContent="center">
                <Grid size={{ xs: 12, md: 7 }}>
                    <Introduction />
                </Grid>
                <Grid id="LogInForm" size={{ xs: 12, md: 5 }}>
                    <LogoText width='260px'/>
                    <h1>Log in</h1>
                    <TextField id="email" label="Email" value={email} 
                        sx={{ mb: '24px' }} onChange={(e) => setEmail(e.target.value)} required/>
                    <br />
                    <TextField id="password" label="Password" type="password" 
                        value={password} sx={{ mb: '24px' }} 
                        onChange={(e) => setPassword(e.target.value)} required/>
                    <br />
                    <Button variant="contained" type="submit" onClick={() => handleSubmit()}
                        sx={{ mb: '24px' }}>Log In</Button>
                    {message && <Alert severity="error">{message}</Alert>}
                    <Button variant="text" onClick={() => navigate('/register')}>Don't have an account? Sign Up</Button>
                </Grid>
            </Grid>
        </div>
    );
}

export default SignInPage;