import styles from './PomodoroPage.module.css';

import { callAPITemplate } from '../utils';

import React from 'react';

function PomodoroPage({ taskPomodoro }) {
    // test pomodoro data
    const [statistic, setStatistic] = React.useState([
        {
            "usetime": 1000,
            "pausetime": 60,
        }
    ]);
    const total = React.useMemo(() => {
        return 10000;
    }, [statistic]);


    // Convert seconds to display format H:MM:SS
    const displaySeconds = (seconds) => {
        // display in format H:MM:SS
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        seconds %= 60;

        if (hours > 0) {
            return `${hours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }
        if (minutes > 0) {
            return `${minutes}:${seconds.toString().padStart(2, '0')}`;
        }
        return `${seconds}`;
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


    return (
        <div>
            <h1>Pomodoro Page</h1>
            {!taskPomodoro
                ? <div>No Pomodoro</div>
                : <div className={styles.container}>
                    <div className={styles.pomodoro}>
                        <h2 className={styles.pomodoroTitle}>{taskPomodoro.name}</h2>
                        <p>Set Length: </p>
                        <input type="number" value={taskPomodoro.duration} />
                        <div>
                            <p>Duration: {displaySeconds(taskPomodoro.duration)}</p>
                            {
                                taskPomodoro.status === "Running" &&
                                <>
                                    <p>Time Remaining: {displaySeconds(taskPomodoro.duration - Math.floor((new Date() - new Date(taskPomodoro.startTime)) / 1000))}</p>
                                    <button>Pause</button>
                                    <button>End</button>
                                </>
                            }
                            {
                                taskPomodoro.status === "Paused" &&
                                <>
                                    <p>Time Remaining: {displaySeconds(taskPomodoro.duration - taskPomodoro.pauseTime)}</p>
                                    <button>Continue</button>
                                </>
                            }
                            {
                                taskPomodoro.status === "Cancelled" &&
                                <>
                                    <p>Time Remaining: {displaySeconds(taskPomodoro.duration - Math.floor((new Date() - new Date(taskPomodoro.startTime)) / 1000))}</p>
                                    <button>Start</button>
                                </>
                            }
                            {
                                taskPomodoro.status === "Completed" &&
                                <p>Completed</p>
                            }
                        </div>
                    </div>
                    <div className={styles.statistic}>
                        <button onClick={() => fetchStatistic()}>Load Statistic</button>
                        {!statistic
                            ? <div>No Statistic</div>
                            : <div>
                                <h2>Statistic</h2>
                            </div>
                        }
                        <p>Today's focus: {displaySeconds(total)}</p>
                    </div>
                </div>
            }
        </div>
    );
}

export default PomodoroPage;