import styles from './HomePage.module.css';

import { callAPITemplate } from '../utils';

import React from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';

import { CircularProgress, Box } from '@mui/material';

function HomePage({ setViewTaskDetailID, updateTaskAttrs, setUpdateTaskAttrs }) {
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();
    const [selectedProject, setSelectedProject] = React.useState(null);
    // State variables for adding new section
    const [isAddingSection, setIsAddingSection] = React.useState(false);
    const [newSectionName, setNewSectionName] = React.useState("");
    // State variables for adding new task
    const [addingSectionID, setAddingSectionID] = React.useState(null);
    const [newTaskName, setNewTaskName] = React.useState("");
    const [newTaskDescription, setNewTaskDescription] = React.useState("");
    // State variables for rendering the tree
    const [tree, setTree] = React.useState({}); // Forest of items that will be rendered
    const [taskStatusMap, setTaskStatusMap] = React.useState({}); // Checkbox status of tasks
    const sectionList = React.useRef({}); // Mapping from sectionID to sectionName
    const sectionDefaultID = React.useRef(null); // sectionID of sectionName is '' (default section)
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
    const callAddSectionAPI = async (name, parentID) => {
        const authToken = localStorage.getItem('authToken');
        callAPITemplate(
            `${process.env.REACT_APP_API_URL}/section/add`,
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
            `${process.env.REACT_APP_API_URL}/task/add`,
            JSON.stringify(payload),
            (data) => {
                setAddingSectionID(null);
                setNewTaskName("");
                setNewTaskDescription("");
                fetchTodoList(selectedProject);
            }
        )
    }
    const callDeleteTodoItemAPI = async (itemID) => {
        const authToken = localStorage.getItem('authToken');
        callAPITemplate(
            `${process.env.REACT_APP_API_URL}/todo_item/delete`,
            JSON.stringify({ "authenticationToken": authToken, "itemID": itemID }),
            (data) => fetchTodoList(selectedProject)
        )
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
        if (!projectID) return;
        const authToken = localStorage.getItem('authToken');
        try {
            // Fetch todo items and task attributes
            const dataItem = await callAPITemplate(
                `${process.env.REACT_APP_API_URL}/todo_item/get_list`,
                JSON.stringify({ "authenticationToken": authToken, "itemID": projectID }),
            );
            const items = dataItem.map(item => JSON.parse(item)).filter(item => item.itemID !== projectID);
            setTree(buildForest(items, projectID));

            // Fetch checkbox status of tasks
            const taskIDs = items.filter(item => item.itemType === 'Task').map(task => task.itemID);
            const dataAttributes = await callAPITemplate(
                `${process.env.REACT_APP_API_URL}/task_attributes/get_list`,
                JSON.stringify({ "authenticationToken": authToken, "itemIDs": taskIDs }),
            );
            const attrsList = dataAttributes.map(attr => JSON.parse(attr));
            const taskStatusMap = Object.fromEntries(attrsList.map(attr => [attr.taskID, attr.status]));
            setTaskStatusMap(taskStatusMap);

            // Fetch section list
            const sectionItems = items.filter(item => item.itemType === 'Section');
            sectionList.current = Object.fromEntries(sectionItems.map(section => [section.itemID, section.name]));
            const defaultSection = sectionItems.find(section => section.name === '');
            sectionDefaultID.current = defaultSection ? defaultSection.itemID : null;
            setAddingSectionID(sectionDefaultID.current);
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
                    {/* Name, Edit button (Task only), and Delete button */}
                    <strong>{node.name}</strong> ({node.itemType})
                    {node.itemType === 'Task' &&
                        <button onClick={() => setViewTaskDetailID(node.itemID)}>Edit</button>
                    }
                    {node.name !== '' &&
                        <button onClick={() => callDeleteTodoItemAPI(node.itemID)}>Delete</button>
                    }
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
        fetchTodoList(selectedProject);
        setUpdateTaskAttrs(Math.random());
    }


    // Fetch todo list data on page load
    React.useEffect(() => {
        fetchTodoList(selectedProject);
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [selectedProject, updateTaskAttrs]);

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

    // Update when searchParams changes
    React.useEffect(() => {
        const projectName = searchParams.get('project') ?? '';
        callGetProjectByNameAPI(projectName)
            .then(data => setSelectedProject(JSON.parse(data).itemID))
            .catch(e => navigate('/'));
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [searchParams]);

    // Cleanup function
    React.useEffect(() => {
        return () => setViewTaskDetailID(null)
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);


    return (
        <div>
            <h1>Welcome to the Home Page</h1>
            {/* Add Task and add Section */}
            {selectedProject &&
                <>
                    {/* Add Task */}
                    {addingSectionID && (
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
                            <div>
                                <label>Choose Section</label>
                                {
                                    Object.entries(sectionList.current).map(([sectionID, sectionName]) => (
                                        <button
                                            key={sectionID}
                                            onClick={() => setAddingSectionID(parseInt(sectionID))}
                                            style={{ backgroundColor: addingSectionID === parseInt(sectionID) ? 'lightblue' : 'white' }}
                                        >{sectionName === '' ? '---' : sectionName}</button>
                                    ))
                                }
                            </div>
                            <button onClick={() => { setAddingSectionID(sectionDefaultID.current); setNewTaskName(""); setNewTaskDescription(""); }}>Cancel</button>
                            <button onClick={() => callAddTaskAPI(newTaskName, addingSectionID ? addingSectionID : sectionDefaultID.current, undefined, undefined, undefined, newTaskDescription)}>Add</button>
                        </div>
                    )}
                    {/* Add Section */}
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
            }
            {/* Render the tree */}
            <div className={styles.treeItems}>
                {Object.values(tree).length > 0 ? (
                    Object.values(tree).map(root => renderTree(root, taskStatusMap))
                ) : (
                    <Box justifyContent='center' alignItems='center' display='flex' height='100vh'> <CircularProgress /> </Box>
                )}
            </div>
        </div>
    );
}

export default HomePage;