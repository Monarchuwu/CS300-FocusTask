import styles from './App.module.css';

import SideBar from './components/SideBar';
import TaskDetailBar from './components/TaskDetailBar';
import SuggestTaskBar from './components/SuggestTaskBar';

import HomePage from './pages/HomePage';
import TodayPage from './pages/TodayPage';
import SignInPage from './pages/SignInPage';
import RegisterPage from './pages/RegisterPage';
import NotFoundPage from './pages/NotFoundPage';

import { callAPITemplate } from './utils';

import React from 'react';
import { Routes, Route, useNavigate, useLocation } from 'react-router-dom';

function App() {
    const navigate = useNavigate();
    const location = useLocation();
    // State variable for DOM to wait while checking validation status  
    const [isLoading, setIsLoading] = React.useState(true);
    // State variables for selected project, task detail, and suggested task list
    const [selectedProject, setSelectedProject] = React.useState(null);
    const [viewTaskDetailID, setViewTaskDetailID] = React.useState(null);
    const [updateTaskAttrs, setUpdateTaskAttrs] = React.useState(0);
    const [suggestTaskList, setSuggestTaskList] = React.useState(false);


    // Check if the authentication token is still valid
    // when the app is loaded
    React.useEffect(() => {
        const checkToken = async () => {
            const isSignInPages = location.pathname === '/signin' || location.pathname === '/register';
            const authToken = localStorage.getItem('authToken');

            try {
                if (isSignInPages) {
                    if (authToken !== null) {
                        await callAPITemplate(
                            'http://localhost:8000/todolist/api/authentication/status',
                            JSON.stringify({ "authenticationToken": authToken }),
                            (data) => {
                                if (data.status) {
                                    navigate('/', { replace: true });
                                }
                            }
                        );
                    }
                }
                else {
                    if (authToken === null) {
                        navigate('/signin', { replace: true });
                    }
                    else {
                        await callAPITemplate(
                            'http://localhost:8000/todolist/api/authentication/status',
                            JSON.stringify({ "authenticationToken": authToken }),
                            (data) => {
                                if (!data.status) {
                                    localStorage.removeItem('authToken');
                                    navigate('/signin', { replace: true });
                                }
                            }
                        );
                    }
                }
            }
            catch (error) {
                console.error('Error:', error);
                return;
            }

            setTimeout(() => {
                setIsLoading(false);
            }, 0);
        }
        checkToken();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);


    return (isLoading
        ? <div>Loading...</div>
        : <div className={styles.App}>
            <Routes>
                <Route path='/' element={
                    <LayoutWithNavBar
                        selectedProject={selectedProject}
                        setSelectedProject={setSelectedProject}
                        viewTaskDetailID={viewTaskDetailID}
                        setViewTaskDetailID={setViewTaskDetailID}
                        updateTaskAttrs={updateTaskAttrs}
                        setUpdateTaskAttrs={setUpdateTaskAttrs}
                        suggestTaskList={suggestTaskList}
                        setSuggestTaskList={setSuggestTaskList}>
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
                        setUpdateTaskAttrs={setUpdateTaskAttrs}
                        suggestTaskList={suggestTaskList}
                        setSuggestTaskList={setSuggestTaskList}>
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
    updateTaskAttrs, setUpdateTaskAttrs,
    suggestTaskList, setSuggestTaskList
}) {
    return (
        <div className={suggestTaskList || viewTaskDetailID ? styles.container_3Columns : styles.container_2Columns}>
            <SideBar selectedProject={selectedProject} setSelectedProject={setSelectedProject} />
            {children.type === HomePage
                ? React.cloneElement(children, {
                    selectedProject,
                    setViewTaskDetailID,
                    updateTaskAttrs, setUpdateTaskAttrs
                })
                : React.cloneElement(children, {
                    setViewTaskDetailID,
                    updateTaskAttrs, setUpdateTaskAttrs,
                    setSuggestTaskList
                })
            }
            {suggestTaskList ?
                <SuggestTaskBar
                    setUpdateTaskAttrs={setUpdateTaskAttrs}
                    setSuggestTaskList={setSuggestTaskList}
                />
                : viewTaskDetailID && <TaskDetailBar
                    taskID={viewTaskDetailID}
                    setTaskID={setViewTaskDetailID}
                    updateTaskAttrs={updateTaskAttrs}
                    setUpdateTaskAttrs={setUpdateTaskAttrs}
                />}
        </div>
    );
}