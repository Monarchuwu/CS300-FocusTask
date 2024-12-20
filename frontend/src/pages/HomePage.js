import styles from './HomePage.module.css';

import { callAPITemplate } from '../utils';

import React from 'react';

function HomePage({ selectedProject }) {
    // State variables for adding new section, task
    const [isAddingSection, setIsAddingSection] = React.useState(false);
    const [newSectionName, setNewSectionName] = React.useState("");
    const [addingTaskID, setAddingTaskID] = React.useState(null);
    const [newTaskName, setNewTaskName] = React.useState("");
    const [newTaskDescription, setNewTaskDescription] = React.useState("");
    // State variables for viewing task details
    const [viewTaskDetailID, setViewTaskDetailID] = React.useState(null);
    const [updateTaskDetail, setUpdateTaskDetail] = React.useState(0);
    const [taskDetails, setTaskDetails] = React.useState(null);
    // State variables for rendering the tree
    const [tree, setTree] = React.useState({}); // Forest of items that will be rendered
    const [taskStatusMap, setTaskStatusMap] = React.useState({}); // Checkbox status of tasks
    // State variable for debouncing status (checkbox) changes
    const [debounceStatus, setDebounceStatus] = React.useState({}); // Queue to smoothly change checkbox state


    // API call functions
    const callAddSectionAPI = async (name, parentID) => {
        const authToken = localStorage.getItem('authToken');
        callAPITemplate(
            'http://localhost:8000/todolist/api/section/add',
            JSON.stringify({ "authenticationToken": authToken, "name": name, "parentID": parentID }),
            (data) => {
                setIsAddingSection(false);
                setNewSectionName("");
                fetchTodoList(selectedProject);
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
                fetchTodoList(selectedProject);
            }
        )
    }
    const callDeleteTodoItemAPI = async (itemID) => {
        const authToken = localStorage.getItem('authToken');
        callAPITemplate(
            'http://localhost:8000/todolist/api/todo_item/delete',
            JSON.stringify({ "authenticationToken": authToken, "itemID": itemID }),
            (data) => fetchTodoList(selectedProject)
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
    // Called by fetchTodoList to build the tree structure (prepare for rendering)
    const buildForest = (items, projectID) => {
        const itemMap = {}; // Map items by itemID for easy access
        const tree = {};

        items.forEach(item => {
            itemMap[item.itemID] = { ...item, children: [] };
        });

        items.forEach(item => {
            if (item.parentID === projectID) {
                tree[item.itemID] = itemMap[item.itemID];
            }
            else if (itemMap[item.parentID]) {
                itemMap[item.parentID].children.push(itemMap[item.itemID]);
            }
        });

        return tree;
    }
    // Fetch todo list data from the server
    const fetchTodoList = async (projectID) => {
        const authToken = localStorage.getItem('authToken');
        try {
            const dataItem = await callAPITemplate(
                'http://localhost:8000/todolist/api/todo_item/get_list',
                JSON.stringify({ "authenticationToken": authToken, "itemID": projectID }),
            );
            const items = dataItem.map(item => JSON.parse(item)).filter(item => item.itemID !== projectID);
            setTree(buildForest(items, projectID));

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
    // Render the todoitem tree recursively
    const renderTree = (node, taskStatusMap) => {
        return (
            <ul key={node.itemID}>
                <li>
                    {/* Checkbox for Task */}
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
                    {/* Name, Edit button, and Delete button */}
                    <strong>{node.name}</strong> ({node.itemType})
                    <button onClick={() => console.log(node)}>Edit</button>
                    <button onClick={() => callDeleteTodoItemAPI(node.itemID)}>Delete</button>
                    {/* Add Task button and input boxes */}
                    {node.itemType === 'Section' &&
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
                    }
                    {/* View Task Detail */}
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
                    {/* Render children */}
                    {node.children && node.children.length > 0 && (
                        <ul>
                            {node.children.map(child => renderTree(child, taskStatusMap))}
                        </ul>
                    )}
                </li>
            </ul>
        );
    };


    // Fetch todo list data on page load
    React.useEffect(() => {
        fetchTodoList(selectedProject);
    }, [selectedProject]);
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
                fetchTodoList(selectedProject);
                setDebounceStatus({});
            }
        }, 300);
        return () => clearTimeout(timeout);
    }, [debounceStatus]);


    return (
        <div>
            <h1>Welcome to the Home Page</h1>
            {/* Add Section */}
            <>
                <button onClick={() => setIsAddingSection(true)}>Add Section</button>
                {isAddingSection && (
                    <div>
                        <input
                            type="text"
                            value={newSectionName}
                            onChange={(e) => setNewSectionName(e.target.value)}
                        />
                        <button onClick={() => { setIsAddingSection(false); setNewSectionName(""); }}>Cancel</button>
                        <button onClick={() => callAddSectionAPI(newSectionName, selectedProject)}>Add</button>
                    </div>
                )}
            </>
            {/* Render the tree */}
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