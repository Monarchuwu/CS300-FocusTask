import styles from './App.module.css';

import HomePage from './pages/HomePage';
import SignInPage from './pages/SignInPage';
import RegisterPage from './pages/RegisterPage';
import NotFoundPage from './pages/NotFoundPage';

import React from 'react';
import { Routes, Route } from 'react-router-dom';

function App() {
    return (
        <div className={styles.App}>
            <Routes>
                <Route path='/' element={<HomePage />} />
                <Route path='/signin' element={<SignInPage />} />
                <Route path='/register' element={<RegisterPage />} />
                <Route path='/*' element={<NotFoundPage />} />
            </Routes>
        </div>
    );
}

export default App;
