import styles from './App.module.css';

import SideBar from './components/SideBar';
import TaskDetailBar from './components/TaskDetailBar';

import HomePage from './pages/HomePage';
import TodayPage from './pages/TodayPage';
import SignInPage from './pages/SignInPage';
import RegisterPage from './pages/RegisterPage';
import NotFoundPage from './pages/NotFoundPage';

import React from 'react';
import { Routes, Route } from 'react-router-dom';

function App() {
    const [selectedProject, setSelectedProject] = React.useState(null);
    const [viewTaskDetailID, setViewTaskDetailID] = React.useState(null);
    const [updateTaskAttrs, setUpdateTaskAttrs] = React.useState(0);

    return (
        <div className={styles.App}>
            <Routes>
                <Route path='/' element={
                    <LayoutWithNavBar
                        selectedProject={selectedProject}
                        setSelectedProject={setSelectedProject}
                        viewTaskDetailID={viewTaskDetailID}
                        setViewTaskDetailID={setViewTaskDetailID}
                        updateTaskAttrs={updateTaskAttrs}
                        setUpdateTaskAttrs={setUpdateTaskAttrs}>
                        <HomePage />
                    </LayoutWithNavBar>
                } />
                <Route path='/today' element={
                    <LayoutWithNavBar
                        selectedProject={selectedProject}
                        setSelectedProject={setSelectedProject}
                        viewTaskDetailID={viewTaskDetailID}
                        setViewTaskDetailID={setViewTaskDetailID}
                        updateTaskAttrs={updateTaskAttrs}
                        setUpdateTaskAttrs={setUpdateTaskAttrs}>
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

function LayoutWithNavBar({
    children,
    selectedProject, setSelectedProject,
    viewTaskDetailID, setViewTaskDetailID,
    updateTaskAttrs, setUpdateTaskAttrs
}) {
    return (
        <div className={viewTaskDetailID ? styles.container_3Columns : styles.container_2Columns}>
            <SideBar selectedProject={selectedProject} setSelectedProject={setSelectedProject} />
            {children.type === HomePage
                ? React.cloneElement(children, { selectedProject, setViewTaskDetailID, updateTaskAttrs, setUpdateTaskAttrs })
                : React.cloneElement(children, { setViewTaskDetailID, updateTaskAttrs, setUpdateTaskAttrs })
            }
            {viewTaskDetailID && <TaskDetailBar
                taskID={viewTaskDetailID}
                setTaskID={setViewTaskDetailID}
                updateTaskAttrs={updateTaskAttrs}
                setUpdateTaskAttrs={setUpdateTaskAttrs}
            />}
        </div>
    );
}