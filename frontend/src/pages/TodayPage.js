import styles from './TodayPage.module.css';

import { callAPITemplate } from '../utils';

import React from 'react';
import { useNavigate } from 'react-router-dom';

import { CircularProgress, Box } from '@mui/material';
import { getPriorityColor, AccordionSectionStyle, AccordionSummaryStyle, TaskBoxStyle, Priority } from "../utils";
import { Accordion, AccordionSummary, AccordionDetails } from '@mui/material';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import Typography from '@mui/material/Typography';
import Checkbox from '@mui/material/Checkbox';
import IconButton from '@mui/material/IconButton';
import DeleteRoundedIcon from '@mui/icons-material/DeleteRounded';
import { Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle } from '@mui/material';
import dayjs from 'dayjs';
import KeyboardReturnIcon from '@mui/icons-material/KeyboardReturn';
import { Tooltip } from '@mui/material';


function TodayPage({ viewTaskDetailID, setViewTaskDetailID, updateTaskAttrs, setUpdateTaskAttrs, setSuggestTaskList }) {
    const navigate = useNavigate();
    // State variables for adding new task
    const [newTaskName, setNewTaskName] = React.useState("");
    const [newTaskDescription, setNewTaskDescription] = React.useState("");
    const [projectDefaultID, setProjectDefaultID] = React.useState(null); // projectID of projectName is '' (default project)
    const [sectionDefaultID, setSectionDefaultID] = React.useState(null); // sectionID of sectionName is '' (default section)
    // State variables for rendering the tree
    const [taskList, setTaskList] = React.useState(null); // a list of tasks that will be rendered
    const [taskAttrMap, setTaskAttrMap] = React.useState({}); // Checkbox status of tasks
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
        setTaskAttrMap({ ...taskAttrMap, [taskID]: status });
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
            const taskAttrMap = Object.fromEntries(attrsList.map(attr => [attr.taskID, attr]));
            setTaskAttrMap(taskAttrMap);
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
    // Navigate to the original project of the task
    const navigateToOriginalProject = async (taskID) => {
        const authToken = localStorage.getItem('authToken');
        const data = await callAPITemplate(
            `${process.env.REACT_APP_API_URL}/todo_item/get_project`,
            JSON.stringify({ "authenticationToken": authToken, "itemID": taskID }),
        );
        const projectName = JSON.parse(data).name;
        navigate({
            pathname: '/',
            search: `?project=${projectName}`,
        });
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


    const Task = ({ task, taskAttrMap }) => {
        const [openDialog, setOpenDialog] = React.useState(false);
        const [taskToDelete, setTaskToDelete] = React.useState(null);

        const handleOpenDialog = (taskID) => {
            setTaskToDelete(taskID);
            setOpenDialog(true);
        };

        const handleCloseDialog = () => {
            setOpenDialog(false);
            setTaskToDelete(null);
        };

        const handleConfirmDelete = () => {
            callDeleteTodoItemAPI(taskToDelete);
            setViewTaskDetailID(null);
            handleCloseDialog();
        };
        return (
            <React.Fragment>
            <Box key={task.itemID}
                sx = {{
                    ...TaskBoxStyle,     
                    backgroundColor: task.itemID === viewTaskDetailID ? 'white' : 'gray.light',
                    boxShadow: task.itemID === viewTaskDetailID ? '0px 2px 5px 0px rgba(0,0,0,0.2)' : 'none'
                }}
                onClick={() => setViewTaskDetailID(task.itemID)} 
                >
                <Box alignItems='center' display='flex'>
                    {/* Checkbox for Task */}
                    <Checkbox
                        checked={taskAttrMap[task.itemID]?.status === 'Completed'}
                        onChange={(e) => {
                            const status = e.target.checked ? 'Completed' : 'Pending';
                            handleStatusChange(task.itemID, status);
                        }}
                        sx={{
                            color: "#BBBBBE",
                            '&.Mui-checked': {
                                color: "primary.main",
                            },
                        }}
                        size="small"
                    />
                    {/* Name, Edit button (Task only), and Delete button */}
                    <Typography variant={'task'}>{task.name}</Typography>
                    <Priority priority={taskAttrMap[task.itemID]?.priority} />
                    {task.name !== '' &&     
                    <Tooltip title="Delete Task">            
                        <IconButton onClick={() => handleOpenDialog(task.itemID)} color="danger"
                            size='small' sx={{ width: '34px', height: '34px' }}>
                            <DeleteRoundedIcon/>
                        </IconButton>
                    </Tooltip>}
                    <Tooltip title="Go to parent Project">
                        <IconButton onClick={() => navigateToOriginalProject(task.itemID)} 
                            size='small' sx={{ width: '34px', height: '34px' }}>
                            <KeyboardReturnIcon/>
                        </IconButton>
                    </Tooltip>
                    {taskAttrMap[task.itemID]?.dueDate && 
                        <Typography variant={'taskAttr'} sx={{ color: 'text.secondary', marginLeft: 'auto', marginRight: '8px' }}>
                            {dayjs(taskAttrMap[task.itemID]?.dueDate).format('HH:mm, DD-MM-YY')}
                        </Typography>}
                </Box>
            </Box>
            <Dialog
                open={openDialog}
                onClose={handleCloseDialog}
                aria-labelledby="alert-dialog-title"
                aria-describedby="alert-dialog-description"
            >
                <DialogTitle id="alert-dialog-title">{"Confirm Delete"}</DialogTitle>
                <DialogContent>
                    <DialogContentText id="alert-dialog-description">
                        Are you sure you want to delete this task?
                    </DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCloseDialog} color="primary" variant="outlined">
                        CANCEL
                    </Button>
                    <Button onClick={handleConfirmDelete} color="danger" autoFocus variant='contained'>
                        CONFIRM
                    </Button>
                </DialogActions>
            </Dialog>
            </React.Fragment>
        );
    };


    const Section = ({ taskList, taskAttrMap, targetStatus, title }) => {
        const tasks = taskList.filter(task => taskAttrMap[task.itemID]?.status === targetStatus);
        return (
             <Accordion sx = {AccordionSectionStyle} defaultExpanded disableGutters={true}>
                <AccordionSummary expandIcon={<ArrowDropDownIcon size="small" stroke="bold" />} 
                        aria-controls="panel1a-content" id="panel1a-header"
                        alignItems='center'
                        justifyContent='center'
                        sx = {AccordionSummaryStyle}>
                    <Typography variant='section'>{title} ({tasks.length})</Typography>
                </AccordionSummary>
                <AccordionDetails disablePadding sx = {{ padding: '0px 10px 10px 10px'}}>
                    {tasks.map(task => (
                        <Box key={task.itemID}>
                            <Task task={task} taskAttrMap={taskAttrMap} />
                        </Box>
                    ))}
                </AccordionDetails>
            </Accordion>
        )
    }


    return (
        <Box sx={{ padding: '15px' }}>
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
            {!taskList ? <Box justifyContent='center' alignItems='center' display='flex' height='25vh'> <CircularProgress /> </Box> :
                // <ul className={styles.taskList}>
                //     {taskList.map(task => (
                //         <li key={task.itemID} className={styles.taskItem}>
                //             {/* Checkbox for Task */}
                //             <input
                //                 type="checkbox"
                //                 checked={taskStatusMap[task.itemID] === 'Completed'}
                //                 onChange={(e) => {
                //                     const status = e.target.checked ? 'Completed' : 'Pending';
                //                     handleStatusChange(task.itemID, status);
                //                 }}
                //             />
                //             {/* Name, Edit button, and Delete button */}
                //             <strong>{task.name}</strong> ({task.itemType})
                //             <button onClick={() => {
                //                 setViewTaskDetailID(task.itemID);
                //                 setSuggestTaskList(false);
                //             }}>Edit</button>
                //             <button onClick={() => navigateToOriginalProject(task.itemID)}>Show location</button>
                //             <button onClick={() => callDeleteTodoItemAPI(task.itemID)}>Delete</button>
                //         </li>
                //     ))}
                // </ul>
                <Box>
                    <Section taskList={taskList} taskAttrMap={taskAttrMap} targetStatus='Pending' title='To-do' />
                    <Section taskList={taskList} taskAttrMap={taskAttrMap} targetStatus='Completed' title='Completed'/>
                </Box>
            }
        </Box>
    )
}

export default TodayPage;