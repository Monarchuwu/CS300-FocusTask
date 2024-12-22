import styles from './TaskDetailBar.module.css';

import { callAPITemplate } from '../utils';

import React from 'react';
import { useNavigate } from 'react-router-dom';

function TaskDetailBar({ taskID, setTaskID, updateTaskAttrs, setUpdateTaskAttrs, setTaskPomodoro }) {
    const navigate = useNavigate();
    // State variable for viewing task details
    const [taskDetails, setTaskDetails] = React.useState(null);
    // State variable for debouncing status (checkbox) changes
    const [debounceStatus, setDebounceStatus] = React.useState({}); // Queue to smoothly change checkbox state
    const [checkboxStatus, setCheckboxStatus] = React.useState('Pending');


    // API call functions
    const callGetTaskAttributesAPI = async (taskID) => {
        const authToken = localStorage.getItem('authToken');
        try {
            const data = await callAPITemplate(
                'http://localhost:8000/todolist/api/task_attributes/get',
                JSON.stringify({ "authenticationToken": authToken, "taskID": taskID }),
            );
            return JSON.parse(data);
        }
        catch (e) {
            console.error(e);
        }
    }
    const callUpdateInTodayDateAPI = async (taskID, inTodayDate) => {
        const authToken = localStorage.getItem('authToken');
        await callAPITemplate(
            'http://localhost:8000/todolist/api/task_attributes/update',
            JSON.stringify({ "authenticationToken": authToken, "taskID": taskID, "inTodayDate": inTodayDate }),
        )
        setUpdateTaskAttrs(Math.random());
    }
    const callGetTodoItemAPI = async (taskID) => {
        const authToken = localStorage.getItem('authToken');
        try {
            const data = await callAPITemplate(
                'http://localhost:8000/todolist/api/todo_item/get',
                JSON.stringify({ "authenticationToken": authToken, "itemID": taskID }),
            );
            return JSON.parse(data);
        }
        catch (e) {
            console.error(e);
        }
    }
    // Helper function to check if a date string is today
    const isToday = (stringDate) => {
        if (!stringDate) return false; // null or undefined
        const today = new Date();
        const dateToCheck = new Date(stringDate);
        return today.getDate() === dateToCheck.getDate() &&
            today.getMonth() === dateToCheck.getMonth() &&
            today.getFullYear() === dateToCheck.getFullYear()
    }
    // Handle checkbox status change (add to the debounce queue)
    const handleStatusChange = (taskID, status) => {
        setCheckboxStatus(status);
        setDebounceStatus({ ...debounceStatus, [taskID]: status });
    }
    // Fetch task details function
    const fetchTaskDetails = async () => {
        if (taskID) {
            try {
                const attrs = await callGetTaskAttributesAPI(taskID);
                const todoItem = await callGetTodoItemAPI(taskID);
                const data = { ...attrs, name: todoItem.name, labelID: todoItem.labelID };
                setTaskDetails(data);
                setCheckboxStatus(data.status);
            }
            catch (e) {
                console.error('Failed to fetch task attributes:', e);
                setTaskDetails(null);
            };
        }
        else setTaskDetails(null);
    }
    // Apply the debounced status changes to the server
    const applyDebounceStatus = async (debounceStatus) => {
        const authToken = localStorage.getItem('authToken');
        for (const [taskID, status] of Object.entries(debounceStatus)) {
            try {
                await callAPITemplate(
                    'http://localhost:8000/todolist/api/task_attributes/update',
                    JSON.stringify({ "authenticationToken": authToken, "taskID": Number(taskID), "status": status })
                );
            }
            catch (e) {
                console.error(e);
            }
        };
        setUpdateTaskAttrs(Math.random());
    }
    // Start Pomodoro function
    const startPomodoro = () => {
        const authToken = localStorage.getItem('authToken');
        callAPITemplate(
            'http://localhost:8000/todolist/api/pomodoro/set_task',
            JSON.stringify({ "authenticationToken": authToken, "taskID": taskID }),
            (data) => {
                setTaskPomodoro({ ...data, name: taskDetails.name });
                navigate('/pomodoro');
            },
            () => { },
            (e) => {
                // test pomodoro data
                console.log('Failed to start pomodoro:', e);
                setTaskPomodoro({
                    pomodoroID: 1,
                    itemID: 1,
                    startTime: new Date().toISOString(),
                    duration: 60,
                    status: "Running",
                    name: "test"
                });
                navigate('/pomodoro');
            }
        );
    }


    // Fetch task details when taskID changes
    React.useEffect(() => {
        fetchTaskDetails();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [taskID, updateTaskAttrs]);
    // Update checkbox status smoothly with debouncing (50ms)
    React.useEffect(() => {
        const timeout = setTimeout(() => {
            if (Object.keys(debounceStatus).length > 0) {
                applyDebounceStatus(debounceStatus);
                setDebounceStatus({});
            }
        }, 50);
        return () => clearTimeout(timeout);
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [debounceStatus]);


    return (
        <div className={styles.container}>
            <h1>TaskDetail</h1>
            <button onClick={() => setTaskID(null)}>Close</button>
            <button onClick={() => startPomodoro()}>Start Pomodoro</button>

            {/* View Task Detail */}
            {taskDetails && (
                <div>
                    <h2>{taskDetails.name}</h2>
                    {/* Checkbox for Task */}
                    <input
                        type="checkbox"
                        checked={checkboxStatus === 'Completed'}
                        onChange={(e) => {
                            const status = e.target.checked ? 'Completed' : 'Pending';
                            handleStatusChange(taskDetails.taskID, status);
                        }}
                    />
                    <p>Due Date: {taskDetails.dueDate || 'N/A'}</p>
                    <p>Priority: {taskDetails.priority || 'N/A'}</p>
                    <p>Description: {taskDetails.description || 'N/A'}</p>
                    {isToday(taskDetails.inTodayDate) ? (
                        <button onClick={() => {
                            callUpdateInTodayDateAPI(taskID, '2100-01-01T00:00:00+00:00');
                        }}>Remove From Today's Task</button>
                    ) : (
                        <button onClick={() => {
                            callUpdateInTodayDateAPI(taskID, new Date().toISOString().replace('Z', '+00:00'));
                        }}>Add To Today's Task</button>
                    )}
                </div>
            )}
        </div>
    )
}

export default TaskDetailBar;