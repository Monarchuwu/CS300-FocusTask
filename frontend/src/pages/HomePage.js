import styles from './HomePage.module.css';

import { callAPITemplate } from '../utils';

import React from 'react';
import { useNavigate } from 'react-router-dom';

function HomePage() {
    const navigate = useNavigate();
    const [isAddingProject, setIsAddingProject] = React.useState(false);
    const [newProjectName, setNewProjectName] = React.useState("");
    const [addingSectionID, setAddingSectionID] = React.useState(null);
    const [newSectionName, setNewSectionName] = React.useState("");
    const [addingTaskID, setAddingTaskID] = React.useState(null);
    const [newTaskName, setNewTaskName] = React.useState("");
    const [newTaskDescription, setNewTaskDescription] = React.useState("");
    const [viewTaskDetailID, setViewTaskDetailID] = React.useState(null);
    const [updateTaskDetail, setUpdateTaskDetail] = React.useState(0);
    const [taskDetails, setTaskDetails] = React.useState(null);
    const [tree, setTree] = React.useState({});
    const [taskStatusMap, setTaskStatusMap] = React.useState({});
    const [debounceStatus, setDebounceStatus] = React.useState({});

    const isToday = (stringDate) => {
        if (!stringDate) return false; // null or undefined
        const today = new Date();
        const dateToCheck = new Date(stringDate);
        return today.getDate() === dateToCheck.getDate() &&
            today.getMonth() === dateToCheck.getMonth() &&
            today.getFullYear() === dateToCheck.getFullYear()
    }
    const callSignOutAPI = async () => {
        const authToken = localStorage.getItem('authToken');
        callAPITemplate(
            'http://localhost:8000/todolist/api/user/signout',
            JSON.stringify({ "authenticationToken": authToken }),
            (data) => {
                localStorage.removeItem('authToken');
                navigate('/signin');
            }
        )
    }
    const callDeleteTodoItemAPI = async (itemID) => {
        const authToken = localStorage.getItem('authToken');
        callAPITemplate(
            'http://localhost:8000/todolist/api/todo_item/delete',
            JSON.stringify({ "authenticationToken": authToken, "itemID": itemID }),
            (data) => fetchTodoList()
        )
    }
    const handleStatusChange = (taskID, status) => {
        setTaskStatusMap((prev) => ({ ...prev, [taskID]: status }));
        setDebounceStatus({ ...debounceStatus, [taskID]: status });
    }
    const buildForest = (items) => {
        const itemMap = {}; // Map items by itemID for easy access
        const tree = {};

        items.forEach(item => {
            itemMap[item.itemID] = { ...item, children: [] };
        });

        items.forEach(item => {
            if (item.parentID === null) {
                tree[item.itemID] = itemMap[item.itemID];
            }
            else if (itemMap[item.parentID]) {
                itemMap[item.parentID].children.push(itemMap[item.itemID]);
            }
        });

        return tree;
    }
    const renderTree = (node, taskStatusMap) => {
        return (
            <ul key={node.itemID}>
                <li>
                    {node.itemType === 'Task' && (
                        <input
                            type="checkbox"
                            checked={taskStatusMap[node.itemID] === 'Completed'}
                            onChange={(e) => {
                                const status = e.target.checked ? 'Completed' : 'Pending';
                                handleStatusChange(node.itemID, status);
                            }}
                        />
                    )}
                    <strong>{node.name}</strong> ({node.itemType})
                    <button onClick={() => console.log(node)}>Edit</button>
                    <button onClick={() => callDeleteTodoItemAPI(node.itemID)}>Delete</button>
                    {node.itemType === 'Project' ? (
                        <>
                            <button onClick={() => setAddingSectionID(node.itemID)}>Add Section</button>
                            {addingSectionID === node.itemID && (
                                <div>
                                    <input
                                        type="text"
                                        value={newSectionName}
                                        onChange={(e) => setNewSectionName(e.target.value)}
                                    />
                                    <button onClick={() => { setAddingSectionID(null); setNewSectionName(""); }}>Cancel</button>
                                    <button onClick={() => callAddSectionAPI(newSectionName, node.itemID)}>Add</button>
                                </div>
                            )}
                        </>
                    ) : (
                        <>
                            <button onClick={() => setAddingTaskID(node.itemID)}>Add Task</button>
                            {addingTaskID === node.itemID && (
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
                                    <br />
                                    <button onClick={() => { setAddingTaskID(null); setNewTaskName(""); setNewTaskDescription(""); }}>Cancel</button>
                                    <button onClick={() => callAddTaskAPI(newTaskName, node.itemID, undefined, undefined, undefined, newTaskDescription)}>Add</button>
                                </div>
                            )}
                        </>
                    )}
                    {node.itemType === 'Task' && (
                        <>
                            <button onClick={() => setViewTaskDetailID(node.itemID)}>View Detail</button>
                            {viewTaskDetailID === node.itemID && taskDetails && (
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
                                            callUpdateInTodayDateAPI(node.itemID, '2100-01-01T00:00:00+00:00');
                                        }}>Remove From Today's Task</button>
                                    ) : (
                                        <button onClick={() => {
                                            callUpdateInTodayDateAPI(node.itemID, new Date().toISOString().replace('Z', '+00:00'));
                                        }}>Add To Today's Task</button>
                                    )}
                                </div>
                            )}
                        </>
                    )}
                    {node.children && node.children.length > 0 && (
                        <ul>
                            {node.children.map(child => renderTree(child, taskStatusMap))}
                        </ul>
                    )}
                </li>
            </ul>
        );
    };
    const fetchTodoList = async () => {
        const authToken = localStorage.getItem('authToken');
        try {
            const dataItem = await callAPITemplate(
                'http://localhost:8000/todolist/api/todo_item/get_all',
                JSON.stringify({ "authenticationToken": authToken }),
            );
            const items = dataItem.map(item => JSON.parse(item));
            setTree(buildForest(items));

            const taskIDs = items.filter(item => item.itemType === 'Task').map(task => task.itemID);
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
    const callAddProjectAPI = async (name) => {
        const authToken = localStorage.getItem('authToken');
        callAPITemplate(
            'http://localhost:8000/todolist/api/project/add',
            JSON.stringify({ "authenticationToken": authToken, "name": name }),
            (data) => {
                setIsAddingProject(false);
                setNewProjectName("");
                fetchTodoList();
            }
        )
    }
    const callAddSectionAPI = async (name, parentID) => {
        const authToken = localStorage.getItem('authToken');
        callAPITemplate(
            'http://localhost:8000/todolist/api/section/add',
            JSON.stringify({ "authenticationToken": authToken, "name": name, "parentID": parentID }),
            (data) => {
                setAddingSectionID(null);
                setNewSectionName("");
                fetchTodoList();
            }
        )
    }
    const callAddTaskAPI = async (name, parentID, dueDate = null, priority = null, status = null, description = null, inTodayDate = null) => {
        const authToken = localStorage.getItem('authToken');
        var payload = {
            "authenticationToken": authToken,
            "name": name,
            "parentID": parentID,
            "dueDate": dueDate,
            "priority": priority,
            "status": status,
            "description": description,
            "inTodayDate": inTodayDate
        }
        payload = Object.fromEntries(
            Object.entries(payload).filter(([_, value]) => value !== null)
        );
        callAPITemplate(
            'http://localhost:8000/todolist/api/task/add',
            JSON.stringify(payload),
            (data) => {
                setAddingTaskID(null);
                setNewTaskName("");
                setNewTaskDescription("");
                fetchTodoList();
            }
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

    React.useEffect(() => {
        if (localStorage.getItem('authToken') === null) {
            navigate('/signin');
        }
    }, []);
    React.useEffect(() => {
        fetchTodoList();
    }, []);
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
            <button onClick={() => callSignOutAPI()}>Sign Out</button>
            <h1>Welcome to the Home Page</h1>

            <button onClick={() => setIsAddingProject(true)}>Add project</button>
            {isAddingProject && (
                <div>
                    <input
                        type="text"
                        value={newProjectName}
                        onChange={(e) => setNewProjectName(e.target.value)}
                    />
                    <button onClick={() => { setIsAddingProject(false); setNewProjectName(""); }}>Cancel</button>
                    <button onClick={() => callAddProjectAPI(newProjectName)}>Add</button>
                </div>
            )}

            <div>
                {Object.values(tree).length > 0 ? (
                    Object.values(tree).map(root => renderTree(root, taskStatusMap))
                ) : (
                    <p>No data available</p>
                )}
            </div>
        </div>
    );
}

export default HomePage;