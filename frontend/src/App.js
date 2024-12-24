import styles from './App.module.css';

import SideBar from './components/SideBar';
import TaskDetailBar from './components/TaskDetailBar';
import SuggestTaskBar from './components/SuggestTaskBar';

import HomePage from './pages/HomePage';
import TodayPage from './pages/TodayPage';
import PomodoroPage from './pages/PomodoroPage';
import SignInPage from './pages/SignInPage';
import RegisterPage from './pages/RegisterPage';
import NotFoundPage from './pages/NotFoundPage';

import { callAPITemplate } from './utils';

import React from 'react';
import { Routes, Route, useNavigate, useLocation } from 'react-router-dom';
import { CircularProgress, Box } from '@mui/material';

console.log(process.env.REACT_APP_API_URL);

function App() {
    const navigate = useNavigate();
    const location = useLocation();
    // State variable for DOM to wait while checking validation status  
    const [isLoading, setIsLoading] = React.useState(true);
    // State variable for selected project
    const [selectedProject, setSelectedProject] = React.useState('Inbox');
    // State variables for task detail
    const [viewTaskDetailID, setViewTaskDetailID] = React.useState(null);
    const [updateTaskAttrs, setUpdateTaskAttrs] = React.useState(0);
    // State variable for selected suggested task list
    const [suggestTaskList, setSuggestTaskList] = React.useState(false);
    // State variable for PomodoroPage
    const [taskPomodoro, setTaskPomodoro] = React.useState(null);


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
                            `${process.env.REACT_APP_API_URL}/authentication/status`,
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
                            `${process.env.REACT_APP_API_URL}/authentication/status`,
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
        ? <Box justifyContent='center' alignItems='center' display='flex' height='100vh'>
            <CircularProgress />
        </Box>
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
                        setSuggestTaskList={setSuggestTaskList}
                        taskPomodoro={taskPomodoro}
                        setTaskPomodoro={setTaskPomodoro}>
                        <HomePage />
                    </LayoutWithNavBar>
                } />
                <Route path='/today' element={
                    <LayoutWithNavBar
                        selectedProject={'Today'}
                        setSelectedProject={setSelectedProject}
                        viewTaskDetailID={viewTaskDetailID}
                        setViewTaskDetailID={setViewTaskDetailID}
                        updateTaskAttrs={updateTaskAttrs}
                        setUpdateTaskAttrs={setUpdateTaskAttrs}
                        suggestTaskList={suggestTaskList}
                        setSuggestTaskList={setSuggestTaskList}
                        taskPomodoro={taskPomodoro}
                        setTaskPomodoro={setTaskPomodoro}>
                        <TodayPage />
                    </LayoutWithNavBar>
                } />
                <Route path='/pomodoro' element={
                    <LayoutWithNavBar
                        selectedProject={'Pomodoro'}
                        setSelectedProject={setSelectedProject}
                        viewTaskDetailID={viewTaskDetailID}
                        setViewTaskDetailID={setViewTaskDetailID}
                        updateTaskAttrs={updateTaskAttrs}
                        setUpdateTaskAttrs={setUpdateTaskAttrs}
                        suggestTaskList={suggestTaskList}
                        setSuggestTaskList={setSuggestTaskList}
                        taskPomodoro={taskPomodoro}
                        setTaskPomodoro={setTaskPomodoro}>
                        <PomodoroPage />
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
    suggestTaskList, setSuggestTaskList,
    taskPomodoro, setTaskPomodoro
}) {
    const [loading, setLoading] = React.useState(true);


    // Call API functions
    const callGetTodoItemAPI = async (taskID) => {
        const authToken = localStorage.getItem('authToken');
        const data = await callAPITemplate(
            `${process.env.REACT_APP_API_URL}/todo_item/get`,
            JSON.stringify({ "authenticationToken": authToken, "itemID": taskID }),
        );
        return JSON.parse(data);
    }
    // Render children with props
    const renderChildrenWithProps = () => {
        switch (children.type) {
            case HomePage:
                return React.cloneElement(children, {
                    selectedProject,
                    setViewTaskDetailID,
                    updateTaskAttrs, setUpdateTaskAttrs
                });
            case TodayPage:
                return React.cloneElement(children, {
                    setViewTaskDetailID,
                    updateTaskAttrs, setUpdateTaskAttrs,
                    setSuggestTaskList
                });
            case PomodoroPage:
                return React.cloneElement(children, {
                    taskPomodoro,
                });
            default:
                return children;
        }
    }


    // Load the last active pomodoro session
    React.useEffect(() => {
        if (taskPomodoro !== null) {
            return;
        }
        const loadPomodoro = async () => {
            const authToken = localStorage.getItem('authToken');
            const data = JSON.parse(await callAPITemplate(
                `${process.env.REACT_APP_API_URL}/pomodoro/get_last_active_session`,
                JSON.stringify({ "authenticationToken": authToken })
            ));
            if (data.haveActiveSession) {
                const taskData = await callGetTodoItemAPI(data.pomodoro.taskID);
                data.pomodoro.name = taskData.name;
                setTaskPomodoro(data.pomodoro);
            }
            setLoading(false);
        }
        loadPomodoro();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);


    return (loading ? <div>Loading...</div> :
        <div className={suggestTaskList || viewTaskDetailID ? styles.container_3Columns : styles.container_2Columns}>
            <SideBar selectedProject={selectedProject} setSelectedProject={setSelectedProject} />
            {renderChildrenWithProps()}
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
                    setTaskPomodoro={setTaskPomodoro}
                />}
        </div>
    );
}