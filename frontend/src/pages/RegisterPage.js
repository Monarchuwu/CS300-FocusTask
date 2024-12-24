import styles from './SignInRegister.module.css';

import { callAPITemplate } from '../utils';

import React from 'react';
import { useNavigate } from 'react-router-dom';

import {
    TextField,
    Button,
    Alert, 
    Grid2 as Grid,
    Box
} from '@mui/material';

import { Helmet } from 'react-helmet';

import Introduction from '../components/Introduction';
import LogoText from '../components/LogoText';


function RegisterPage() {
    const navigate = useNavigate();
    const [username, setUsername] = React.useState('');
    const [email, setEmail] = React.useState('');
    const [password, setPassword] = React.useState('');
    const [message, setMessage] = React.useState('');

    const callRegisterAPI = (username, email, password) => {
        callAPITemplate(
            `${process.env.REACT_APP_API_URL}/user/register`,
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
            <Grid container spacing={2} justifyContent="center">
                <Grid size={{ xs: 12, md: 7 }}>
                    <Introduction />
                </Grid>
                <Grid id="SignUpForm" size={{ xs: 12, md: 5 }} height='100vh'>
                    <LogoText width='260px' />
                    <Box sx={{ px: '100px', width: '100%', maxWidth: '570px' }}>
                        <h1>Sign up</h1>
                        <TextField type="text" name="username" value={username} 
                            sx={{ mb: '24px' }} label="Username" onChange={(e) => setUsername(e.target.value)} fullWidth required/>
                        <br />
                        <TextField type="email" name="email" value={email}
                            sx={{ mb: '24px' }} label="Email" onChange={(e) => setEmail(e.target.value)} fullWidth required />
                        <br />
                        <TextField type="password" name="password" value={password} 
                            sx={{ mb: '24px' }} label="Password" onChange={(e) => setPassword(e.target.value)} fullWidth required/>
                        <br />
                        <Button variant='contained' type="submit" sx={{ mb: '24px' }}
                            onClick={() => handleSubmit()} fullWidth className={styles.SignInButton}>Create Account</Button>
                        {message && <Alert severity="error">{message}</Alert>}
                        <Button variant='text' onClick={() => navigate('/signin')}
                            sx='text-align: center; display: block; margin: 0 auto;'>Already had an account? Log in</Button>
                    </Box>
                </Grid>
            </Grid>
        </div>
    );
}

export default RegisterPage;