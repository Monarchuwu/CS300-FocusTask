import styles from './TodayPage.module.css';

import { callAPITemplate } from '../utils';

import React from 'react';

function TodayPage({ setViewTaskDetailID, updateTaskAttrs, setUpdateTaskAttrs, setSuggestTaskList }) {
    // State variables for rendering the tree
    const [taskList, setTaskList] = React.useState([]); // a list of tasks that will be rendered
    const [taskStatusMap, setTaskStatusMap] = React.useState({}); // Checkbox status of tasks
    // State variable for debouncing status (checkbox) changes
    const [debounceStatus, setDebounceStatus] = React.useState({}); // Queue to smoothly change checkbox state


    // API call functions
    const callDeleteTodoItemAPI = async (itemID) => {
        const authToken = localStorage.getItem('authToken');
        callAPITemplate(
            'http://localhost:8000/todolist/api/todo_item/delete',
            JSON.stringify({ "authenticationToken": authToken, "itemID": itemID }),
            (data) => fetchTodoList()
        )
    }
    // Handle checkbox status change (add to the debounce queue)
    const handleStatusChange = (taskID, status) => {
        setTaskStatusMap((prev) => ({ ...prev, [taskID]: status }));
        setDebounceStatus({ ...debounceStatus, [taskID]: status });
    }
    // Fetch todo list data from the server
    const fetchTodoList = async () => {
        const authToken = localStorage.getItem('authToken');
        try {
            const dataTasks = await callAPITemplate(
                'http://localhost:8000/todolist/api/task/get_today_list',
                JSON.stringify({ "authenticationToken": authToken }),
            );
            const tasks = dataTasks.map(task => JSON.parse(task));
            setTaskList(tasks);

            const taskIDs = tasks.map(task => task.itemID);
            const dataAttributes = await callAPITemplate(
                'http://localhost:8000/todolist/api/task_attributes/get_list',
                JSON.stringify({ "authenticationToken": authToken, "itemIDs": taskIDs }),
            );
            const attrsList = dataAttributes.map(attr => JSON.parse(attr));
            const taskStatusMap = Object.fromEntries(attrsList.map(attr => [attr.taskID, attr.status]));
            setTaskStatusMap(taskStatusMap);
        }
        catch (e) {
            console.error(e);
        }
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
        fetchTodoList();
        setUpdateTaskAttrs(Math.random());
    }


    // Fetch todo list data on page load and when updating a Task Attribute
    React.useEffect(() => {
        fetchTodoList();
    }, [updateTaskAttrs]);
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
        <div>
            <h1>Today</h1>
            <button onClick={() => setSuggestTaskList(true)}>Suggestions</button>
            {/* Render Task List */}
            <ul className={styles.taskList}>
                {taskList.map(task => (
                    <li key={task.itemID} className={styles.taskItem}>
                        {/* Checkbox for Task */}
                        <input
                            type="checkbox"
                            checked={taskStatusMap[task.itemID] === 'Completed'}
                            onChange={(e) => {
                                const status = e.target.checked ? 'Completed' : 'Pending';
                                handleStatusChange(task.itemID, status);
                            }}
                        />
                        {/* Name, Edit button, and Delete button */}
                        <strong>{task.name}</strong> ({task.itemType})
                        <button onClick={() => setViewTaskDetailID(task.itemID)}>Edit</button>
                        <button onClick={() => callDeleteTodoItemAPI(task.itemID)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    )
}

export default TodayPage;