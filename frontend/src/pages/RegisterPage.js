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
    const [messageSeverity, setMessageSeverity] = React.useState('');
    const [confirmPassword, setConfirmPassword] = React.useState('');

    const callRegisterAPI = (username, email, password) => {
        return new Promise((resolve, reject) => {
            callAPITemplate(
                `${process.env.REACT_APP_API_URL}/user/register`,
                JSON.stringify({ "username": username, "email": email, "password": password }),
                (data) => {
                    setMessageSeverity('success');
                    setMessage('User registered successfully!');
                    resolve('User registered successfully!');
                },
                (message) => {
                    setMessageSeverity('error');
                    setMessage(message || 'An error occurred');
                    reject(message);
                },
                (e) => {
                    setMessageSeverity('error');
                    setMessage('Error: ' + e.message);
                    reject(e.message);
                }
            );
        });
    }

    const callSignInAPI = (email, password) => {
        callAPITemplate(
            `${process.env.REACT_APP_API_URL}/user/signin`,
            JSON.stringify({ "email": email, "password": password }),
            (data) => {
                const authToken = data.authenticationToken;
                localStorage.setItem('authToken', authToken);
                navigate('/');
            },
            (message) => {
                setMessage(message || 'An error occurred');
                setMessageSeverity('error');
            },
            (e) => {
                setMessage('Error: ' + e.message);
                setMessageSeverity('error');
            }
        )
    }
    const handleConfirmPasswordChange = (e) => {
        setConfirmPassword(e.target.value);
    };


    const isValidEmail = (email) => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    const handleSubmit = () => {
        if (!isValidEmail(email)) {
            setMessageSeverity('error');
            setMessage('Email is invalid!');
            return;
        }
        if (password !== confirmPassword) {
            setMessageSeverity('error');
            setMessage('Passwords do not match');
            return;
        }
        callRegisterAPI(username, email, password).then((message) => {
            if (message === 'User registered successfully!') {
                console.log(email + ' User registered successfully!');
                callSignInAPI(email, password);
            }
        }, (error) => {
            console.log(email + ' ' + error);
        });
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
                        <TextField type="password" name="confirmPassword" value={confirmPassword} 
                            sx={{ mb: '24px' }} 
                            color = {password === confirmPassword ? 'success' : 'error'}
                            label="Confirm Password" onChange={handleConfirmPasswordChange} fullWidth required/>
                        <br />
                        <Button variant='contained' type="submit" sx={{ mb: '24px' }}
                            onClick={() => handleSubmit()} fullWidth className={styles.SignInButton}>Create Account</Button>
                        {message && <Alert severity={messageSeverity === '' ? "warning" : messageSeverity}>{message}</Alert>}
                        <Button variant='text' onClick={() => navigate('/signin')}
                            sx='text-align: center; display: block; margin: 0 auto;'>Already had an account? Log in</Button>
                    </Box>
                </Grid>
            </Grid>
        </div>
    );
}

export default RegisterPage;