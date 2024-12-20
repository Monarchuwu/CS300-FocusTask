import styles from './TodayPage.module.css';

import { callAPITemplate } from '../utils';

import React from 'react';

function TodayPage() {
    // State variables for viewing task details
    const [viewTaskDetailID, setViewTaskDetailID] = React.useState(null);
    const [updateTaskDetail, setUpdateTaskDetail] = React.useState(0);
    const [taskDetails, setTaskDetails] = React.useState(null);
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
        setUpdateTaskDetail(updateTaskDetail + 1);
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


    // Fetch todo list data on page load
    React.useEffect(() => {
        fetchTodoList();
    }, []);
    // Fetch task details when viewTaskDetailID changes
    React.useEffect(() => {
        if (viewTaskDetailID) {
            callGetTaskAttributesAPI(viewTaskDetailID)
                .then(data => setTaskDetails(data))
                .catch(e => {
                    console.error('Failed to fetch task attributes:', e);
                    setTaskDetails(null);
                });
        }
    }, [viewTaskDetailID, updateTaskDetail]);
    // Update checkbox status smoothly with debouncing (300ms)
    React.useEffect(() => {
        const timeout = setTimeout(() => {
            if (Object.keys(debounceStatus).length > 0) {
                const authToken = localStorage.getItem('authToken');
                Object.entries(debounceStatus).forEach(([taskID, status]) => {
                    callAPITemplate(
                        'http://localhost:8000/todolist/api/task_attributes/update',
                        JSON.stringify({ "authenticationToken": authToken, "taskID": Number(taskID), "status": status })
                    );
                });
                fetchTodoList();
                setDebounceStatus({});
            }
        }, 300);
        return () => clearTimeout(timeout);
    }, [debounceStatus]);


    return (
        <div>
            <h1>Today</h1>
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
                        <button onClick={() => console.log(task)}>Edit</button>
                        <button onClick={() => callDeleteTodoItemAPI(task.itemID)}>Delete</button>
                        {/* View Task Detail */}
                        <>
                            <button onClick={() => setViewTaskDetailID(task.itemID)}>View Detail</button>
                            {viewTaskDetailID === task.itemID && taskDetails && (
                                <div>
                                    <p><strong>Task Details:</strong></p>
                                    <p>Due Date: {taskDetails.dueDate || 'N/A'}</p>
                                    <p>Priority: {taskDetails.priority || 'N/A'}</p>
                                    <p>Status: {taskDetails.status || 'N/A'}</p>
                                    <p>Description: {taskDetails.description || 'N/A'}</p>
                                    <p>In Today Date: {taskDetails.inTodayDate || 'N/A'}</p>
                                    <button onClick={() => setViewTaskDetailID(null)}>Close</button>
                                    {isToday(taskDetails.inTodayDate) ? (
                                        <button onClick={() => {
                                            callUpdateInTodayDateAPI(task.itemID, '2100-01-01T00:00:00+00:00');
                                        }}>Remove From Today's Task</button>
                                    ) : (
                                        <button onClick={() => {
                                            callUpdateInTodayDateAPI(task.itemID, new Date().toISOString().replace('Z', '+00:00'));
                                        }}>Add To Today's Task</button>
                                    )}
                                </div>
                            )}
                        </>
                    </li>
                ))}
            </ul>
        </div>
    )
}

export default TodayPage;