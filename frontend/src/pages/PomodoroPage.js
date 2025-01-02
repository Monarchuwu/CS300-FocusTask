import styles from './PomodoroPage.module.css';

import { callAPITemplate } from '../utils';

import React from 'react';
import { Typography, Box, Button, CircularProgress } from '@mui/material';
import { displaySeconds } from '../utils';

import AddRoundedIcon from '@mui/icons-material/AddRounded';
import RemoveRoundedIcon from '@mui/icons-material/RemoveRounded';

function PomodoroPage({ taskPomodoro, setTaskPomodoro }) {
    // State variable to edit the length of the pomodoro
    const [pomodoroLength, setPomodoroLength] = React.useState(taskPomodoro && taskPomodoro.duration ? taskPomodoro.duration : 25*60);
    // State variable to store the status of the pomodoro
    const [pomodoroStatus, setPomodoroStatus] = React.useState(taskPomodoro && taskPomodoro.status ? taskPomodoro.status : "Canceled");
    // Variables to store the timer ID (running state)
    const timerID = React.useRef(null);
    const [remainingTime, setRemainingTime] = React.useState(25 * 60);


    // API call functions
    const callStartPomodoroAPI = async () => {
        const authToken = localStorage.getItem('authToken');
        await callAPITemplate(
            `${process.env.REACT_APP_API_URL}/pomodoro/start`,
            JSON.stringify({ "authenticationToken": authToken, "pomodoroID": taskPomodoro.pomodoroID })
        )
    }
    const callPausePomodoroAPI = async () => {
        const authToken = localStorage.getItem('authToken');
        await callAPITemplate(
            `${process.env.REACT_APP_API_URL}/pomodoro/pause`,
            JSON.stringify({ "authenticationToken": authToken, "pomodoroID": taskPomodoro.pomodoroID })
        )
    }
    const callContinuePomodoroAPI = async () => {
        const authToken = localStorage.getItem('authToken');
        await callAPITemplate(
            `${process.env.REACT_APP_API_URL}/pomodoro/continue`,
            JSON.stringify({ "authenticationToken": authToken, "pomodoroID": taskPomodoro.pomodoroID })
        )
    }
    const callEndPomodoroAPI = async () => {
        const authToken = localStorage.getItem('authToken');
        await callAPITemplate(
            `${process.env.REACT_APP_API_URL}/pomodoro/end`,
            JSON.stringify({ "authenticationToken": authToken, "pomodoroID": taskPomodoro.pomodoroID })
        )
    }
    const callSetPomodoroLengthAPI = async (pomodoroID, length) => {
        const authToken = localStorage.getItem('authToken');
        await callAPITemplate(
            `${process.env.REACT_APP_API_URL}/pomodoro/set_length`,
            JSON.stringify({ "authenticationToken": authToken, "pomodoroID": pomodoroID, "length": length }),
            (data) => setPomodoroLength(length)
        )
    }
    const callGetRemainingTimeAPI = async () => {
        const authToken = localStorage.getItem('authToken');
        const currentTime = await callAPITemplate(
            `${process.env.REACT_APP_API_URL}/pomodoro/get_time`,
            JSON.stringify({ "authenticationToken": authToken, "pomodoroID": taskPomodoro.pomodoroID }),
        )
        return parseInt(currentTime);
    }
    // Update the remaining time
    const fetchRemainingTime = async () => {
        const remainingTime = await callGetRemainingTimeAPI();
        setRemainingTime(remainingTime);
        return remainingTime;
    }
    // Create a timer to update the remaining time
    const createTimer = () => {
        if (timerID.current) {
            return timerID.current;
        }
        return setInterval(async () => {
            setRemainingTime((prev) => {
                const remainingTime = prev - 1;
                if (remainingTime <= 0) {
                    endPomodoro();
                }
                return remainingTime;
            });
        }, 1000);
    }
    // handle pomodoro functions
    const startPomodoro = async () => {
        await callStartPomodoroAPI();
        setPomodoroStatus("Running");
        taskPomodoro.status = "Running";
        setRemainingTime(pomodoroLength);
        timerID.current = createTimer();
    }
    const pausePomodoro = async () => {
        await callPausePomodoroAPI();
        setPomodoroStatus("Paused");
        taskPomodoro.status = "Paused";
        clearInterval(timerID.current);
        timerID.current = null;
        fetchRemainingTime();
    }
    const continuePomodoro = async () => {
        await callContinuePomodoroAPI();
        setPomodoroStatus("Running");
        taskPomodoro.status = "Running";
        timerID.current = createTimer();
    }
    const endPomodoro = async () => {
        await callEndPomodoroAPI();
        setPomodoroStatus("Completed");
        taskPomodoro.status = "Completed";
        clearInterval(timerID.current);
        timerID.current = null;
        // fetchStatistic();
        createNewPomodoroSession(taskPomodoro.taskID, taskPomodoro.name);
        setRemainingTime(pomodoroLength);
    }
    // Start Pomodoro function
    const createNewPomodoroSession = (taskID, taskName) => {
        const authToken = localStorage.getItem('authToken');
        callAPITemplate(
            `${process.env.REACT_APP_API_URL}/pomodoro/set_task`,
            JSON.stringify({ "authenticationToken": authToken, "taskID": taskID }),
            (data) => {
                setTaskPomodoro({ ...JSON.parse(data), name: taskName });
                callSetPomodoroLengthAPI(JSON.parse(data).pomodoroID, pomodoroLength);
            }
        );
    }

    // Update the timer based on the state of the pomodoro on page load
    React.useEffect(() => {
        if (pomodoroStatus === "Running") {
            const fetching = async () => {
                await fetchRemainingTime();
                timerID.current = createTimer();
            }
            fetching();
        }
        else if (pomodoroStatus === "Paused") {
            fetchRemainingTime();
        }
        return () => {
            clearInterval(timerID.current);
            timerID.current = null;
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    // Update the pomodoro status when the taskPomodoro changes
    React.useEffect(() => {
        if (taskPomodoro === null) {
            setPomodoroStatus("Canceled");
        }
        else {
            setPomodoroStatus(taskPomodoro.status);
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [taskPomodoro?.status]);

    const increasePomodoroLength = () => {
        if (pomodoroLength < 90 * 60) {
            setPomodoroLength(pomodoroLength + 5 * 60);
            setRemainingTime(pomodoroLength + 5 * 60);
        }
    };

    const decreasePomodoroLength = () => {
        if (pomodoroLength > 5 * 60) {
            setPomodoroLength(pomodoroLength - 5 * 60);
            setRemainingTime(pomodoroLength - 5 * 60);
        }
    };

    const PomodoroMenu = ({pomodoroStatus}) => {
        const POMO_CIRCLE_SIZE = 350;

        const pomoButtonProps = {
            variant: 'contained',
            size: 'large',
            sx: { width: "230px", borderRadius: "8px", height: "55px" }
        };

        const StartButton = () => {
            return (
                <Button onClick={() => { startPomodoro() }}
                    color='primary' {...pomoButtonProps}>
                    Start
                </Button>
            );
        };

        const PauseButton = () => {
            return (
                <Button onClick={() => { pausePomodoro() }} color="pausebutton"
                    {...pomoButtonProps}>
                    Pause
                </Button>
            );
        };

        const EndButton = () => {
            return (
                <Button onClick={() => { endPomodoro() }} color="endbutton" 
                    {...pomoButtonProps}>
                    End
                </Button>
            );
        };

        const ContinueButton = () => {
            return (
                <Button onClick={() => { continuePomodoro() }}
                    {...pomoButtonProps}>
                    Continue
                </Button>
            );
        };

        const PomodoroClock = () => {
            const progress = ((pomodoroLength - remainingTime) / pomodoroLength) * 100;

            return (
                <Box sx={{ display: "flex", justifyContent: "center", alignItems: "center", transition: "all 0.5s ease" }}>
                    <Box sx={{ position: "relative", display: "inline-flex" }}>
                        <Box sx={{ backgroundColor: "#E6E4F0", borderRadius: POMO_CIRCLE_SIZE/2, 
                                    width: POMO_CIRCLE_SIZE, height: POMO_CIRCLE_SIZE, 
                                    justifyContent: "center", display: "flex", 
                                    alignItems: "center"}}>
                            <CircularProgress variant="determinate" value={progress} size={POMO_CIRCLE_SIZE} />
                            <Box sx={{ backgroundColor: "#F9F8FF", borderRadius: POMO_CIRCLE_SIZE/2 - 20, 
                                        width: POMO_CIRCLE_SIZE - 40, height: POMO_CIRCLE_SIZE - 40, 
                                        justifyContent: "center", display: "flex", 
                                        flexDirection: "column",
                                        alignItems: "center", position: "absolute"}}>
                                {pomodoroStatus === "Canceled" && <Button onClick={increasePomodoroLength}><AddRoundedIcon/></Button>}
                                <Typography variant="pomo">
                                    {pomodoroStatus === "Canceled" ? displaySeconds(pomodoroLength) : displaySeconds(remainingTime)}
                                </Typography>
                                {pomodoroStatus === "Canceled" && <Button onClick={decreasePomodoroLength}><RemoveRoundedIcon/></Button>}
                            </Box>
                        </Box>
                    </Box>
                </Box>
            );
        }

        return (
            <Box sx={{ 
                    display: "flex", 
                    flexDirection: "column", 
                    alignItems: "center", 
                    justifyContent: "center",
                    gap: "20px", 
                    height: "100vh" }}>
                <Typography variant="h5">{taskPomodoro?.name || "Choose a Task in Project Lists"}</Typography>
                <PomodoroClock />
                {taskPomodoro && (
                    pomodoroStatus === "Canceled" ? 
                    <StartButton />
                    : pomodoroStatus === "Running" ? 
                    <Box display="flex" justifyContent="center" sx={{ gap: "10px" }}>
                        <PauseButton />
                        <EndButton />
                    </Box>
                    : (
                        pomodoroStatus === "Paused" && <ContinueButton />
                    )
                )}
            </Box>
        );
    };


    return (
        <PomodoroMenu pomodoroStatus={pomodoroStatus} />
    );
}

export default PomodoroPage;