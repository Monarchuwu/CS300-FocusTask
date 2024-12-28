import styles from './PomodoroPage.module.css';

import BarChart24 from '../components/BarChart24';

import { callAPITemplate } from '../utils';

import React from 'react';

function PomodoroPage({ taskPomodoro }) {
    // statistic pomodoro
    const [statistic, setStatistic] = React.useState(null);
    const total = React.useMemo(() => {
        if (!statistic) return 0;
        return parseInt(statistic.reduce((acc, cur) => acc + cur[0], 0));
    }, [statistic]);
    // State variable to edit the length of the pomodoro
    const [pomodoroLength, setPomodoroLength] = React.useState(taskPomodoro && taskPomodoro.duration ? taskPomodoro.duration : 0);
    const [inputPomodoroLength, setInputPomodoroLength] = React.useState(taskPomodoro && taskPomodoro.duration ? taskPomodoro.duration : 0);
    // State variable to store the status of the pomodoro
    const [pomodoroStatus, setPomodoroStatus] = React.useState(taskPomodoro && taskPomodoro.status ? taskPomodoro.status : "Canceled");
    // Variables to store the timer ID (running state)
    const timerID = React.useRef(null);
    const [remainingTime, setRemainingTime] = React.useState(0);
    const [blockList, setBlockList] = React.useState([]);
    const [newWebsite, setNewWebsite] = React.useState('');


    // API call functions
    const callStartPomodoroAPI = () => {
        const authToken = localStorage.getItem('authToken');
        callAPITemplate(
            'http://localhost:8000/todolist/api/pomodoro/start',
            JSON.stringify({ "authenticationToken": authToken, "pomodoroID": taskPomodoro.pomodoroID })
        )
    }
    const callPausePomodoroAPI = () => {
        const authToken = localStorage.getItem('authToken');
        callAPITemplate(
            'http://localhost:8000/todolist/api/pomodoro/pause',
            JSON.stringify({ "authenticationToken": authToken, "pomodoroID": taskPomodoro.pomodoroID })
        )
    }
    const callContinuePomodoroAPI = () => {
        const authToken = localStorage.getItem('authToken');
        callAPITemplate(
            'http://localhost:8000/todolist/api/pomodoro/continue',
            JSON.stringify({ "authenticationToken": authToken, "pomodoroID": taskPomodoro.pomodoroID })
        )
    }
    const callEndPomodoroAPI = () => {
        const authToken = localStorage.getItem('authToken');
        callAPITemplate(
            'http://localhost:8000/todolist/api/pomodoro/end',
            JSON.stringify({ "authenticationToken": authToken, "pomodoroID": taskPomodoro.pomodoroID })
        )
    }
    const callSetPomodoroLengthAPI = (length) => {
        const authToken = localStorage.getItem('authToken');
        callAPITemplate(
            'http://localhost:8000/todolist/api/pomodoro/set_length',
            JSON.stringify({ "authenticationToken": authToken, "pomodoroID": taskPomodoro.pomodoroID, "length": length }),
            (data) => setPomodoroLength(length)
        )
    }
    const callGetRemainingTimeAPI = async () => {
        const authToken = localStorage.getItem('authToken');
        const currentTime = await callAPITemplate(
            'http://localhost:8000/todolist/api/pomodoro/get_time',
            JSON.stringify({ "authenticationToken": authToken, "pomodoroID": taskPomodoro.pomodoroID }),
        )
        return parseInt(currentTime);
    }
    // Convert seconds to display format H:MM:SS
    const displaySeconds = (seconds) => {
        if (typeof (seconds) !== 'number' || seconds < 0) {
            return "type error";
        }
        // display in format H:MM:SS
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        seconds %= 60;
        return `${hours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
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
    }

    // Fetch statistic
    const fetchStatistic = async () => {
        const authToken = localStorage.getItem('authToken');
        callAPITemplate(
            'http://localhost:8000/todolist/api/pomodoro/get_history_hour_fullday',
            JSON.stringify({ "authenticationToken": authToken, "date": new Date().toISOString() }),
            (data) => setStatistic(data)
        )
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
    // Fetch statistic on page load
    React.useEffect(() => {
        fetchStatistic();
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
    React.useEffect(() => {
        fetchBlockList();
    }, []);

    // Fetch the block list
    const fetchBlockList = async () => {
        const authToken = localStorage.getItem('authToken');
        try {
            console.log("Fetching block list");
            console.log(authToken);
            const dataBlockItems = await callAPITemplate(
                'http://localhost:8000/todolist/api/website_block/get_block_list',
                JSON.stringify({ authenticationToken: authToken }),
            );
            const blockItems = dataBlockItems.map(item => JSON.parse(item));
            setBlockList(blockItems);
        }
        catch (e) {
            console.error(e);
        }
    };

    // Add a website to the block list
    const addWebsite = async () => {
        const authToken = localStorage.getItem('authToken');
        callAPITemplate(
            'http://localhost:8000/todolist/api/website_block/add_url',
            JSON.stringify({ authenticationToken: authToken, URL: newWebsite }),
            () => fetchBlockList(),
            setNewWebsite('')
        );
    };

    // Delete a website from the block list
    const deleteWebsite = async (blockID) => {
        const authToken = localStorage.getItem('authToken');
        callAPITemplate(
            'http://localhost:8000/todolist/api/website_block/delete_url',
            JSON.stringify({ authenticationToken: authToken, blockID: blockID }),
            () => fetchBlockList()
        );
    };


    return (
        <div>
            <h1>Pomodoro Page</h1>
            <div className={styles.container}>
                {!taskPomodoro
                    ? <div>No Pomodoro</div>
                    : <div className={styles.pomodoro}>
                        {/* Name of task */}
                        <h2 className={styles.pomodoroTitle}>{taskPomodoro.name}</h2>
                        {/* Set a new length for the pomodoro session */}
                        {pomodoroStatus === "Canceled" &&
                            <>
                                <p>Set Length (seconds): </p>
                                <input type="number"
                                    value={inputPomodoroLength.toString()}
                                    onChange={(e) => {
                                        const value = Math.max(0, Math.min(10800, Number(e.target.value)));
                                        setInputPomodoroLength(value);
                                    }}
                                    max={10800} min={0} maxLength={5} />
                                <button onClick={() => { callSetPomodoroLengthAPI(inputPomodoroLength) }}>Set</button>
                            </>
                        }
                        {/* Display the pomodoro session */}
                        <div>
                            { /* Status: Before running */
                                pomodoroStatus === "Canceled" &&
                                <>
                                    <p>{displaySeconds(pomodoroLength)}</p>
                                    <button onClick={() => { startPomodoro() }}>Start</button>
                                </>
                            }
                            {
                                pomodoroStatus === "Running" &&
                                <>
                                    <p>Time Remaining: {displaySeconds(remainingTime)}</p>
                                    <button onClick={() => { pausePomodoro() }}>Pause</button>
                                    <button onClick={() => { endPomodoro() }}>End</button>
                                </>
                            }
                            {
                                pomodoroStatus === "Paused" &&
                                <>
                                    <p>Time Remaining: {displaySeconds(remainingTime)}</p>
                                    <button onClick={() => { continuePomodoro() }}>Continue</button>
                                </>
                            }
                            {
                                pomodoroStatus === "Completed" &&
                                <p>Completed</p>
                            }
                        </div>
                    </div>
                }
                <div className={styles.statistic}>
                    <button onClick={() => fetchStatistic()}>Load Statistic</button>
                    {!statistic
                        ? <div>No Statistic</div>
                        : <div>
                            <BarChart24 data={statistic} />
                        </div>
                    }
                    <p>Today's focus: {displaySeconds(total)}</p>
                </div>
                <div className={styles.blockList}>
                    <h2>Website Block List</h2>
                    <ul>
                        {blockList.map((blockItem) => (
                            <li key={blockItem.blockID}>
                                {blockItem.URL}
                                <button onClick={() => deleteWebsite(blockItem.blockID)}>Delete</button>
                            </li>
                        ))}
                    </ul>
                    <input
                        type="text"
                        value={newWebsite}
                        onChange={(e) => setNewWebsite(e.target.value)}
                        placeholder="Add a website URL"
                    />
                    <button onClick={() => addWebsite()}>Add</button>
                </div>
            </div>
        </div>
    );
}

export default PomodoroPage;