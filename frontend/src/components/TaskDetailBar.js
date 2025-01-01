import styles from './TaskDetailBar.module.css';

import { callAPITemplate } from '../utils';

import React from 'react';
import { useNavigate } from 'react-router-dom';

import Box from '@mui/material/Box';
import Checkbox from '@mui/material/Checkbox';
import Input from '@mui/material/Input';
import TextField from '@mui/material/TextField';
import dayjs from 'dayjs';


const DEBOUNCE_DELAY = 700;

// Title of the task detail
const TaskDetailTitle = ({ taskDetails, handleFieldChange }) => {
    return (
        <Box display="flex" sx={{ alignItems: 'center' }}>
            <Checkbox
                checked={taskDetails?.status === 'Completed'}
                onChange={handleFieldChange('status')}
            />  
            <Input
                value={taskDetails?.name || ''}
                onChange={handleFieldChange('name')}
            />
        </Box>
    );
};

const TaskDetailDescription = ({ taskDetails, handleFieldChange }) => {
    return (
        <TextField
            value={taskDetails?.description || ''}
            onChange={handleFieldChange('description')}
            variant="outlined"
            multiline
            fullWidth
        />
    );
}


// Debounce hook
const useDebounce = (func, delay) => {
    const timer = React.useRef(null);

    React.useEffect(() => {
        // Clean up the timer when the component unmounts
        return () => {
            if (timer.current) {
                clearTimeout(timer.current);
            }
        };
    }, []);

    const debouncedFunction = (...args) => {
        if (timer.current) {
            clearTimeout(timer.current);
        }
        timer.current = setTimeout(() => {
            func(...args);
        }, delay);
    };

    return debouncedFunction;
};

function TaskDetailBar({ taskID, setTaskID, updateTaskAttrs, setUpdateTaskAttrs, setTaskPomodoro }) {
    const navigate = useNavigate();
    // State variable for viewing task details
    const [taskDetails, setTaskDetails] = React.useState(null);
    // State variable for debouncing status (checkbox) changes

    // API call functions
    const callGetTaskAttributesAPI = async (taskID) => {
        const authToken = localStorage.getItem('authToken');
        try {
            const data = await callAPITemplate(
                `${process.env.REACT_APP_API_URL}/task_attributes/get`,
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
            `${process.env.REACT_APP_API_URL}/task_attributes/update`,
            JSON.stringify({ "authenticationToken": authToken, "taskID": taskID, "inTodayDate": inTodayDate }),
        )
        setUpdateTaskAttrs(Math.random());
    }
    const callGetTodoItemAPI = async (taskID) => {
        const authToken = localStorage.getItem('authToken');
        try {
            const data = await callAPITemplate(
                `${process.env.REACT_APP_API_URL}/todo_item/get`,
                JSON.stringify({ "authenticationToken": authToken, "itemID": taskID }),
            );
            // convert dueDate to serializable format before parse to JSON
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

    // Fetch task details function
    const fetchTaskDetails = async () => {
        if (taskID) {
            try {
                const attrs = await callGetTaskAttributesAPI(taskID);
                const todoItem = await callGetTodoItemAPI(taskID);
                const data = { ...attrs, name: todoItem.name, labelID: todoItem.labelID };
                setTaskDetails(data);   
            }
            catch (e) {
                console.error('Failed to fetch task attributes:', e);
                setTaskDetails(null);
            };
        }
        else setTaskDetails(null);
    }

    // Start Pomodoro function
    const startPomodoro = () => {
        const authToken = localStorage.getItem('authToken');
        callAPITemplate(
            `${process.env.REACT_APP_API_URL}/pomodoro/set_task`,
            JSON.stringify({ "authenticationToken": authToken, "taskID": taskID }),
            (data) => {
                setTaskPomodoro({ ...JSON.parse(data), name: taskDetails.name });
                navigate('/pomodoro');
            }
        );
    }


    // Fetch task details when taskID changes
    React.useEffect(() => {
        fetchTaskDetails();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [taskID, updateTaskAttrs]);

    const debounce = (func, delay) => {
        let timer;
        return (...args) => {
            if (timer) clearTimeout(timer);
            timer = setTimeout(() => func(...args), delay);
        };
    };

    const updateTaskField = async (field, value) => {
        try {
            const authToken = localStorage.getItem('authToken');
            if (field === 'name') {
                await callAPITemplate(
                    `${process.env.REACT_APP_API_URL}/todo_item/update`,
                    JSON.stringify({ "authenticationToken": authToken, "itemID": Number(taskID), "name": value })
                );
            } else {
                await callAPITemplate(
                    `${process.env.REACT_APP_API_URL}/task_attributes/update`,
                    JSON.stringify({ "authenticationToken": authToken, "taskID": taskID, [field]: value })
                );
            }
            setUpdateTaskAttrs(Math.random());
            console.log(`Field "${field}" updated in database:`, value);
        } catch (e) {
            console.error(`Failed to update field "${field}":`, e);
        }
    };

    const debouncedUpdateTaskField = useDebounce(updateTaskField, DEBOUNCE_DELAY);

    const handleFieldChange = (field) => (event) => {
        const value = event.target.type === 'checkbox' ? 
                        (event.target.checked ? 'Completed' : 'Pending')
                        : event.target.value;

        // Update local state immediately
        setTaskDetails((prevDetails) => ({
            ...prevDetails,
            [field]: value,
        }));

        // Update the backend with debounce
        debouncedUpdateTaskField(field, value);
    };


    return (
        <Box className={styles.container}>
            {/* View Task Detail */}
            {taskDetails && (
                <div>
                    <TaskDetailTitle 
                        taskDetails={{ name: taskDetails?.name, status: taskDetails?.status }} 
                        handleFieldChange={handleFieldChange} 
                    />
                    {/* Checkbox for Task */}
                    <button onClick={() => startPomodoro()}>Start Pomodoro</button>
                    <p>Due Date: {taskDetails.dueDate ? dayjs(taskDetails.dueDate).format('HH:mm, DD-MM-YY') : 'N/A'}</p>
                    <p>Priority: {taskDetails.priority || 'N/A'}</p>
                    <TaskDetailDescription 
                        taskDetails={{ description: taskDetails?.description }} 
                        handleFieldChange={handleFieldChange}
                    />
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
        </Box>
    )
}

export default TaskDetailBar;