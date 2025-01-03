import styles from './SuggestTaskBar.module.css';

import { callAPITemplate } from '../utils';

import React from 'react';
import { Checkbox, Divider, Typography } from '@mui/material';
import { List, ListItem, ListItemText, IconButton } from '@mui/material';
import AddRoundedIcon from '@mui/icons-material/AddRounded';

function SuggestTaskBar({ setUpdateTaskAttrs, setSuggestTaskList }) {
    // State variable for rendering the tree
    const [taskList, setTaskList] = React.useState([]); // a list of tasks that will be rendered
    // State variable for debouncing status (checkbox) changes
    const [debounceStatus, setDebounceStatus] = React.useState([]); // Queue to smoothly change checkbox state


    // Remove a task from the suggested task list locally
    const removeTaskFromTaskList = (taskID) => {
        setTaskList((prev) => prev.filter(task => task.itemID !== taskID));
    }
    // Update the status of the task (remove locally + update on the server)
    const handleStatusComplete = (taskID) => {
        removeTaskFromTaskList(taskID);
        setDebounceStatus((prev) => {
            if (!prev.includes(taskID)) {
                return [...prev, taskID];
            }
            return prev;
        });
    }
    // Add a task to the today list on the server and make a request (a task attrs was updated)
    const addTaskIntoToday = (taskID) => {
        const authToken = localStorage.getItem('authToken');
        callAPITemplate(
            `${process.env.REACT_APP_API_URL}/task/add_task_today`,
            JSON.stringify({ "authenticationToken": authToken, "taskID": taskID }),
        )
            .then(() => {
                removeTaskFromTaskList(taskID);
                setUpdateTaskAttrs(Math.random());
            })
            .catch((e) => console.error(e));
    }


    // Fetch todo list data from the server
    const fetchTodoList = async () => {
        const authToken = localStorage.getItem('authToken');
        try {
            const dataTasks = await callAPITemplate(
                `${process.env.REACT_APP_API_URL}/task/suggest_today`,
                JSON.stringify({ "authenticationToken": authToken }),
            );
            const tasks = dataTasks.map(task => JSON.parse(task));
            setTaskList(tasks);
        }
        catch (e) {
            console.error(e);
        }
    }
    // Apply the debounced status changes to the server
    const applyDebounceStatus = async (debounceStatus) => {
        const authToken = localStorage.getItem('authToken');
        for (const taskID of debounceStatus) {
            try {
                await callAPITemplate(
                    `${process.env.REACT_APP_API_URL}/task_attributes/update`,
                    JSON.stringify({ "authenticationToken": authToken, "taskID": Number(taskID), "status": 'Completed' })
                );
            }
            catch (e) {
                console.error(e);
            }
        };
        setUpdateTaskAttrs(Math.random());
    }


    // Fetch todo list data on page load and when updating a Task Attribute
    React.useEffect(() => {
        fetchTodoList();
    }, []);
    // Update checkbox status smoothly with debouncing (50ms)
    React.useEffect(() => {
        const timeout = setTimeout(() => {
            if (Object.keys(debounceStatus).length > 0) {
                applyDebounceStatus(debounceStatus);
                setDebounceStatus([]);
            }
        }, 50);
        return () => clearTimeout(timeout);
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [debounceStatus]);


    return (
        <div>
            <Typography variant='h6'>Suggestions</Typography>
            <Divider />
            {/* <button onClick={() => setSuggestTaskList(false)}>Close</button> */}
            {/* Render Task List */}
            <List>
                {taskList.map(task => (
                    <ListItem key={task.itemID} className={styles.taskItem}
                        secondaryAction={
                            <IconButton edge="end" aria-label="delete" onClick={() => addTaskIntoToday(task.itemID)}>
                                <AddRoundedIcon />
                            </IconButton>
                        }
                        sx={{
                            "&:hover": {
                                backgroundColor: 'gray.light',
                            }
                        }}>
                        {/* Checkbox for Task */}
                        <Checkbox
                            checked={false}
                            onChange={(e) => {
                                if (e.target.checked) {
                                    handleStatusComplete(task.itemID);
                                }
                            }}
                        />
                        {/* Name, Edit button, and Delete button */}
                        <ListItemText>{task.name}</ListItemText>
                    </ListItem>
                ))}
            </List>
        </div>
    )
}

export default SuggestTaskBar;