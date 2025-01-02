import styles from './PomodoroPage.module.css';

import { callAPITemplate } from '../utils';

import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Typography, Box, Button } from '@mui/material';
import { displaySeconds } from '../utils';

function PomodoroPage({ taskPomodoro }) {
    const navigate = useNavigate();
    // State variable to edit the length of the pomodoro
    const [pomodoroLength, setPomodoroLength] = React.useState(taskPomodoro && taskPomodoro.duration ? taskPomodoro.duration : 0);
    const [inputPomodoroLength, setInputPomodoroLength] = React.useState(taskPomodoro && taskPomodoro.duration ? taskPomodoro.duration : 0);
    // State variable to store the status of the pomodoro
    const [pomodoroStatus, setPomodoroStatus] = React.useState(taskPomodoro && taskPomodoro.status ? taskPomodoro.status : "Canceled");
    // Variables to store the timer ID (running state)
    const timerID = React.useRef(null);
    const [remainingTime, setRemainingTime] = React.useState(0);


    // API call functions
    const callStartPomodoroAPI = () => {
        const authToken = localStorage.getItem('authToken');
        callAPITemplate(
            `${process.env.REACT_APP_API_URL}/pomodoro/start`,
            JSON.stringify({ "authenticationToken": authToken, "pomodoroID": taskPomodoro.pomodoroID })
        )
    }
    const callPausePomodoroAPI = () => {
        const authToken = localStorage.getItem('authToken');
        callAPITemplate(
            `${process.env.REACT_APP_API_URL}/pomodoro/pause`,
            JSON.stringify({ "authenticationToken": authToken, "pomodoroID": taskPomodoro.pomodoroID })
        )
    }
    const callContinuePomodoroAPI = () => {
        const authToken = localStorage.getItem('authToken');
        callAPITemplate(
            `${process.env.REACT_APP_API_URL}/pomodoro/continue`,
            JSON.stringify({ "authenticationToken": authToken, "pomodoroID": taskPomodoro.pomodoroID })
        )
    }
    const callEndPomodoroAPI = () => {
        const authToken = localStorage.getItem('authToken');
        callAPITemplate(
            `${process.env.REACT_APP_API_URL}/pomodoro/end`,
            JSON.stringify({ "authenticationToken": authToken, "pomodoroID": taskPomodoro.pomodoroID })
        )
    }
    const callSetPomodoroLengthAPI = (length) => {
        const authToken = localStorage.getItem('authToken');
        callAPITemplate(
            `${process.env.REACT_APP_API_URL}/pomodoro/set_length`,
            JSON.stringify({ "authenticationToken": authToken, "pomodoroID": taskPomodoro.pomodoroID, "length": length }),
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
                if (remainingTime - 1 <= 0) {
                    endPomodoro();
                }
                return remainingTime;
            });
        }, 1000);
    }
    // handle pomodoro functions
    const startPomodoro = () => {
        callStartPomodoroAPI();
        setPomodoroStatus("Running");
        taskPomodoro.status = "Running";
        setRemainingTime(pomodoroLength);
        timerID.current = createTimer();
    }
    const pausePomodoro = () => {
        callPausePomodoroAPI();
        setPomodoroStatus("Paused");
        taskPomodoro.status = "Paused";
        clearInterval(timerID.current);
        timerID.current = null;
    }
    const continuePomodoro = () => {
        callContinuePomodoroAPI();
        setPomodoroStatus("Running");
        taskPomodoro.status = "Running";
        timerID.current = createTimer();
    }
    const endPomodoro = () => {
        callEndPomodoroAPI();
        setPomodoroStatus("Completed");
        taskPomodoro.status = "Completed";
        clearInterval(timerID.current);
        timerID.current = null;
        console.log(taskPomodoro);
        navigateToOriginalProject(taskPomodoro.taskID);
    }
    // Navigate to the original project of the task
    const navigateToOriginalProject = async (taskID) => {
        const authToken = localStorage.getItem('authToken');
        const data = await callAPITemplate(
            `${process.env.REACT_APP_API_URL}/todo_item/get_project`,
            JSON.stringify({ "authenticationToken": authToken, "itemID": taskID }),
        );
        const projectName = JSON.parse(data).name;
        navigate({
            pathname: '/',
            search: `?project=${projectName}`,
        });
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
            return (
                <Box sx={{ backgroundColor: "#E6E4F0", borderRadius: POMO_CIRCLE_SIZE/2, 
                            width: POMO_CIRCLE_SIZE, height: POMO_CIRCLE_SIZE, justifyContent: "center", display: "flex", alignItems: "center" }}>
                    <Box sx={{ backgroundColor: "#F9F8FF", borderRadius: POMO_CIRCLE_SIZE/2 - 20, 
                            width: POMO_CIRCLE_SIZE - 40, height: POMO_CIRCLE_SIZE - 40, justifyContent: "center", display: "flex", alignItems: "center" }}>
                    <Typography variant="pomo">
                        {pomodoroStatus === "Canceled" ? displaySeconds(pomodoroLength) : displaySeconds(remainingTime)}
                    </Typography>
                    </Box>
                </Box>
            );
        }

        return (
            <Box sx={{ display: "flex", flexDirection: "column", alignItems: "center", gap: "20px" }}>
                <Typography variant="h5">{taskPomodoro.name}</Typography>

                {pomodoroStatus === "Canceled" &&
                    <Box>
                        <p>Set Length (seconds): </p>
                        <input type="number"
                            value={inputPomodoroLength.toString()}
                            onChange={(e) => {
                                const value = Math.max(0, Math.min(10800, Number(e.target.value)));
                                setInputPomodoroLength(value);
                            }}
                            max={10800} min={0} maxLength={5} />
                        <button onClick={() => { callSetPomodoroLengthAPI(inputPomodoroLength) }}>Set</button>
                    </Box>
                }
                <PomodoroClock />
                {
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
                }
            </Box>
        );
    };


    return (
        <div className={styles.container}>
            {!taskPomodoro
                ? <Box sx={{ height: "100vh", justifyContent: "center"}} >No Pomodoro</Box>
                : <PomodoroMenu pomodoroStatus={pomodoroStatus} />
            }
        </div>
    );
}

export default PomodoroPage;