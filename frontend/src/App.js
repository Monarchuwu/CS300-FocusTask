import styles from './App.module.css';

import SideBar from './components/SideBar';
import TaskDetailBar from './components/TaskDetailBar';
import SuggestTaskBar from './components/SuggestTaskBar';

import HomePage from './pages/HomePage';
import TodayPage from './pages/TodayPage';
import PomodoroPage from './pages/PomodoroPage';
import SignInPage from './pages/SignInPage';
import RegisterPage from './pages/RegisterPage';

import { callAPITemplate } from './utils';

import React from 'react';
import { Routes, Route, useNavigate, useLocation, Navigate } from 'react-router-dom';
import { CircularProgress, Box, Grid2 as Grid } from '@mui/material';

console.log(process.env.REACT_APP_API_URL);

function App() {
    const navigate = useNavigate();
    const location = useLocation();
    // State variable for DOM to wait while checking validation status  
    const [isLoading, setIsLoading] = React.useState(true);
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
        if (!isLoading) {
            return;
        }
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
            }, 1000);
        }
        checkToken();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [isLoading]);


    return (isLoading
        ? <Box justifyContent='center' alignItems='center' display='flex' height='100vh'>
            <CircularProgress />
        </Box>
        : <div className={styles.App}>
            <Routes>
                <Route path='/' element={
                    <LayoutWithNavBar
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
                <Route path="/*" element={<Navigate to="/" replace />} />
            </Routes>
        </div>
    );
}

export default App;

function LayoutWithNavBar({
    children,
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
                    viewTaskDetailID,
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
            setLoading(false);
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


    return (loading ? <Box justifyContent='center' alignItems='center' display='flex' height='100vh'> <CircularProgress /> </Box> :
        <Grid container spacing={0} sx={{ height: '100vh' }}>
            <Grid item size={{ xs: 12, sm: 2.5 }} sx={{ overflowY: 'auto' }}>
                <SideBar />
            </Grid>
            <Grid item size={{ xs: 12, sm: 6 }} sx={{ overflowY: 'auto', height: '100vh' }}>
                {renderChildrenWithProps()}
            </Grid>
            <Grid item size={{ xs: 12, sm: 3.5 }} sx={{
                padding: '30px 25px',
                borderLeft: '1px solid',
                borderColor: 'border.main',
                backgroundColor: 'white',
                overflowY: 'auto',
                height: '100vh'
            }}> 
                {suggestTaskList ?
                    <SuggestTaskBar
                        setUpdateTaskAttrs={setUpdateTaskAttrs}
                        setSuggestTaskList={setSuggestTaskList}
                    />
                    : viewTaskDetailID && <TaskDetailBar
                        taskID={viewTaskDetailID}
                        updateTaskAttrs={updateTaskAttrs}
                        setUpdateTaskAttrs={setUpdateTaskAttrs}
                        setTaskPomodoro={setTaskPomodoro}
                    />}
            </Grid>
        </Grid>
    );
}