import styles from './SuggestTaskBar.module.css';

import { callAPITemplate } from '../utils';

import React from 'react';

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
            'http://localhost:8000/todolist/api/task/add_task_today',
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
                'http://localhost:8000/todolist/api/task/suggest_today',
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
                    'http://localhost:8000/todolist/api/task_attributes/update',
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
            <h1>Suggestions</h1>
            <button onClick={() => setSuggestTaskList(false)}>Close</button>
            {/* Render Task List */}
            <ul className={styles.taskList}>
                {taskList.map(task => (
                    <li key={task.itemID} className={styles.taskItem}>
                        {/* Checkbox for Task */}
                        <input
                            type="checkbox"
                            checked={false}
                            onChange={(e) => {
                                if (e.target.checked) {
                                    handleStatusComplete(task.itemID);
                                }
                            }}
                        />
                        {/* Name, Edit button, and Delete button */}
                        <strong>{task.name}</strong>
                        <button onClick={() => addTaskIntoToday(task.itemID)}>+</button>
                    </li>
                ))}
            </ul>
        </div>
    )
}

export default SuggestTaskBar;