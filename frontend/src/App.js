import styles from './App.module.css';

import SideBar from './components/SideBar';

import HomePage from './pages/HomePage';
import TodayPage from './pages/TodayPage';
import SignInPage from './pages/SignInPage';
import RegisterPage from './pages/RegisterPage';
import NotFoundPage from './pages/NotFoundPage';

import React from 'react';
import { Routes, Route } from 'react-router-dom';

function App() {
    const [selectedProject, setSelectedProject] = React.useState(null);

    return (
        <div className={styles.App}>
            <Routes>
                <Route path='/' element={
                    <LayoutWithNavBar
                        selectedProject={selectedProject}
                        setSelectedProject={setSelectedProject}>
                        <HomePage />
                    </LayoutWithNavBar>
                } />
                <Route path='/today' element={
                    <LayoutWithNavBar
                        selectedProject={selectedProject}
                        setSelectedProject={setSelectedProject}>
                        <TodayPage />
                    </LayoutWithNavBar>
                } />
                <Route path='/signin' element={<SignInPage />} />
                <Route path='/register' element={<RegisterPage />} />
                <Route path='/*' element={<NotFoundPage />} />
            </Routes>
        </div>
    );
}

export default App;

function LayoutWithNavBar({ children, selectedProject, setSelectedProject }) {
    return (
        <div className={styles.container}>
            <SideBar selectedProject={selectedProject} setSelectedProject={setSelectedProject} />
            {children.type === HomePage
                ? React.cloneElement(children, { selectedProject })
                : children
            }
        </div>
    );
}