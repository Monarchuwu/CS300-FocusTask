import styles from './TodayPage.module.css';

import { callAPITemplate } from '../utils';

import React from 'react';

function TodayPage({ setViewTaskDetailID, updateTaskAttrs, setUpdateTaskAttrs, setSuggestTaskList }) {
    // State variables for adding new task
    const [newTaskName, setNewTaskName] = React.useState("");
    const [newTaskDescription, setNewTaskDescription] = React.useState("");
    const [projectDefaultID, setProjectDefaultID] = React.useState(null); // projectID of projectName is '' (default project)
    const [sectionDefaultID, setSectionDefaultID] = React.useState(null); // sectionID of sectionName is '' (default section)
    // State variables for rendering the tree
    const [taskList, setTaskList] = React.useState([]); // a list of tasks that will be rendered
    const [taskStatusMap, setTaskStatusMap] = React.useState({}); // Checkbox status of tasks
    // State variable for debouncing status (checkbox) changes
    const [debounceStatus, setDebounceStatus] = React.useState({}); // Queue to smoothly change checkbox state


    // API call functions
    const callGetProjectByNameAPI = async (name) => {
        const authToken = localStorage.getItem('authToken');
        return await callAPITemplate(
            `${process.env.REACT_APP_API_URL}/project/get_by_name`,
            JSON.stringify({ "authenticationToken": authToken, "projectName": name }),
        )
    };
    const callGetSectionByNameAPI = async (projectID, name) => {
        const authToken = localStorage.getItem('authToken');
        return await callAPITemplate(
            `${process.env.REACT_APP_API_URL}/section/get_by_name`,
            JSON.stringify({ "authenticationToken": authToken, "projectID": projectID, "sectionName": name }),
        )
    };
    const callAddTaskAPI = async (name, parentID, dueDate = null, priority = null, status = null, description = null, inTodayDate = new Date().toISOString()) => {
        const authToken = localStorage.getItem('authToken');
        var payload = {
            "authenticationToken": authToken,
            "name": name,
            "parentID": parentID,
            "dueDate": dueDate,
            "priority": priority,
            "status": status,
            "description": description,
            "inTodayDate": inTodayDate,
        }
        payload = Object.fromEntries(
            Object.entries(payload).filter(([_, value]) => value !== null)
        );
        callAPITemplate(
            `${process.env.REACT_APP_API_URL}/task/add`,
            JSON.stringify(payload),
            (data) => {
                setNewTaskName("");
                setNewTaskDescription("");
                fetchTodoList();
            }
        )
    }
    const callDeleteTodoItemAPI = async (itemID) => {
        const authToken = localStorage.getItem('authToken');
        callAPITemplate(
            `${process.env.REACT_APP_API_URL}/todo_item/delete`,
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
                `${process.env.REACT_APP_API_URL}/task/get_today_list`,
                JSON.stringify({ "authenticationToken": authToken }),
            );
            const tasks = dataTasks.map(task => JSON.parse(task));
            setTaskList(tasks);

            const taskIDs = tasks.map(task => task.itemID);
            const dataAttributes = await callAPITemplate(
                `${process.env.REACT_APP_API_URL}/task_attributes/get_list`,
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
                    `${process.env.REACT_APP_API_URL}/task_attributes/update`,
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

    // Cleanup function
    React.useEffect(() => {
        return () => {
            setViewTaskDetailID(null);
            setSuggestTaskList(false);
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    // Get the default project and section IDs
    React.useEffect(() => {
        const loadDefaultProjectSection = async () => {
            const projectItem = JSON.parse(await callGetProjectByNameAPI(''));
            setProjectDefaultID(projectItem.itemID);
            const sectionItem = JSON.parse(await callGetSectionByNameAPI(projectItem.itemID, ''));
            setSectionDefaultID(sectionItem.itemID);
        }
        loadDefaultProjectSection();
    }, [taskList]);


    return (
        <div>
            <h1>Today</h1>
            {/* Add Task */}
            {projectDefaultID && sectionDefaultID && (
                <div>
                    <label>Name</label>
                    <input
                        type="text"
                        value={newTaskName}
                        onChange={(e) => setNewTaskName(e.target.value)}
                    />
                    <br />
                    <label>Description</label>
                    <input
                        type="text"
                        value={newTaskDescription}
                        onChange={(e) => setNewTaskDescription(e.target.value)}
                    />
                    <button onClick={() => { setNewTaskName(""); setNewTaskDescription(""); }}>Cancel</button>
                    <button onClick={() => callAddTaskAPI(newTaskName, sectionDefaultID, undefined, undefined, undefined, newTaskDescription)}>Add</button>
                </div>
            )}
            {/* Suggest Task List button */}
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
                        <button onClick={() => {
                            setViewTaskDetailID(task.itemID);
                            setSuggestTaskList(false);
                        }}>Edit</button>
                        <button onClick={() => callDeleteTodoItemAPI(task.itemID)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    )
}

export default TodayPage;