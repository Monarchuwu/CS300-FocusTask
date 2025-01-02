import { callAPITemplate } from '../utils';

import React from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';

import { CircularProgress, Box, Typography, 
        Checkbox, Accordion, AccordionDetails, 
        AccordionSummary, 
        IconButton } from '@mui/material';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import DeleteRoundedIcon from '@mui/icons-material/DeleteRounded';
import AddRoundedIcon from '@mui/icons-material/AddRounded';
import { Helmet } from 'react-helmet';
import { Dialog, DialogActions, DialogContent, 
    DialogContentText, DialogTitle, Button, TextField } from '@mui/material';
import { Plus } from 'react-iconly';
import { ClickAwayListener } from '@mui/base/ClickAwayListener';
import dayjs from 'dayjs';

import DateTimePickerButtonDialog from "../components/DateTimePickerButtonDialog";
import { AccordionSectionStyle, AccordionSummaryStyle, Priority, TaskBoxStyle } from "../utils";
import PriorityPicker from "../components/PriorityPicker";
import SectionPicker from "../components/SectionPicker";

function HomePage({ viewTaskDetailID, setViewTaskDetailID, updateTaskAttrs, setUpdateTaskAttrs }) {
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();
    const [selectedProject, setSelectedProject] = React.useState(null);
    // State variables for adding new section
    const [isAddingSection, setIsAddingSection] = React.useState(false);
    const [newSectionName, setNewSectionName] = React.useState("");
    // State variables for adding new task
    const [selectedSection, setSelectedSection] = React.useState(null);
    const [newTaskName, setNewTaskName] = React.useState("");
    const [newTaskDescription, setNewTaskDescription] = React.useState("");
    // State variables for rendering the tree
    const [tree, setTree] = React.useState({}); // Forest of items that will be rendered
    const [taskAttrMap, setTaskAttrMap] = React.useState({}); // Mapping from taskID to task attributes
    const sectionList = React.useRef({}); // Mapping from sectionID to sectionName
    const sectionDefaultID = React.useRef(null); // sectionID of sectionName is '' (default section)
    // State variable for debouncing status (checkbox) changes
    const [debounceStatus, setDebounceStatus] = React.useState({}); // Queue to smoothly change checkbox state
    const newSectionNameRef = React.useRef(null);

    const [selectedDate, setSelectedDate] = React.useState(null);
    const [selectedPriority, setSelectedPriority] = React.useState(null);
    
    const [showTaskDescription, setShowTaskDescription] = React.useState(false);
    const taskDescriptionRef = React.useRef(null);

    const handleKeyPressTaskName = (e) => {
        if (e.shiftKey && e.key === 'Enter') {
            setShowTaskDescription(true);
            setTimeout(() => {
                taskDescriptionRef.current.focus();
            }, 0);
        } else if (e.key === 'Enter') {
            handleAddTask();
        }
    };

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
        // Convert dueDate to ISO string if it's not null
        if (dueDate) {
            dueDate = dayjs(dueDate).toISOString(); // or use .format('YYYY-MM-DDTHH:mm:ssZ') for specific formatting
        }
        console.log('Due Date:', dueDate);
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
            () => {
                setSelectedSection(null);
                setNewTaskName("");
                setNewTaskDescription("");
                setSelectedDate(null);
                setSelectedPriority(null);
                setShowTaskDescription(false);
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
        setDebounceStatus({ ...debounceStatus, [taskID]: status });
        setTaskAttrMap({ ...taskAttrMap, [taskID]: { ...taskAttrMap[taskID], status: status } });
    }
    // Handle adding new section
    const handleCancleAddSection = () => {
        setIsAddingSection(false);
        setNewSectionName("");
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
            const items = dataItem
                .map(item => JSON.parse(item))
                .filter(item => item.itemID !== projectID);
            setTree(buildForest(items, projectID));

            // Fetch checkbox status of tasks
            const taskIDs = items.filter(item => item.itemType === 'Task').map(task => task.itemID);

            const dataAttributes = await callAPITemplate(
                `${process.env.REACT_APP_API_URL}/task_attributes/get_list`,
                JSON.stringify({ "authenticationToken": authToken, "itemIDs": taskIDs }),
            );
            const attrsList = dataAttributes.map(attr => {
                const parsedAttr = JSON.parse(attr);
                return {
                    ...parsedAttr,
                    dueDate: parsedAttr.dueDate ? dayjs(parsedAttr.dueDate).toISOString() : null,
                };
            });
            const taskAttrMap = Object.fromEntries(attrsList.map(attr => [attr.taskID, attr]));
            setTaskAttrMap(taskAttrMap);

            // Fetch section list
            const sectionItems = items.filter(item => item.itemType === 'Section');
            sectionList.current = Object.fromEntries(sectionItems.map(section => [section.itemID, section.name]));
            const defaultSection = sectionItems.find(section => section.name === '');
            sectionDefaultID.current = defaultSection ? defaultSection.itemID : null;
            setSelectedSection(defaultSection);
        }
        catch (e) {
            console.error(e);
        }
    }

    const handleNewSectionClick = () => {
        setIsAddingSection(true);
        setTimeout(() => {
            if (newSectionNameRef.current) {
                newSectionNameRef.current.focus();
            }
        }, 0);
    };

    // if is adding new section, and escape key is pressed, cancel adding section
    // if enter key is pressed, add the section
    React.useEffect(() => {
        const handleKeyDown = (e) => {
            if (isAddingSection) {
                if (e.key === 'Escape') {
                    handleCancleAddSection();
                }
                else if (e.key === 'Enter') {
                    callAddSectionAPI(newSectionName, selectedProject);
                }
            }
        }
        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [isAddingSection, newSectionName]);

    const handleAddTask = () => {
        callAddTaskAPI(newTaskName, selectedSection ? 
                        selectedSection.itemID : sectionDefaultID.current, selectedDate, selectedPriority, undefined, newTaskDescription
                        );
    };


    const Section = ({ section, taskAttrMap }) => {

        return (
            <Accordion sx = {AccordionSectionStyle} defaultExpanded disableGutters={true}>
                {section.name !== '' && 
                    <AccordionSummary expandIcon={<ArrowDropDownIcon size="small" stroke="bold" />} 
                        aria-controls="panel1a-content" id="panel1a-header"
                        alignItems='center'
                        justifyContent='center'
                        sx = {AccordionSummaryStyle}>
                        <Typography variant='section'>{section.name}</Typography>
                    </AccordionSummary>}
                <AccordionDetails disablePadding sx = {{ padding: section.name !== '' ? '0px 10px 10px 10px' : '10px' }}>
                    {/* Render children */}
                    {section.children && section.children.length > 0 && (
                        <Box>
                            {section.children.map(child => renderTree(child, taskAttrMap))}
                        </Box>
                    )}
                </AccordionDetails>
            </Accordion>
        );
    };

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
                    <IconButton onClick={() => handleOpenDialog(task.itemID)} color="danger"
                        size='small' sx={{ width: '34px', height: '34px' }}>
                        <DeleteRoundedIcon/>
                    </IconButton>}
                    {taskAttrMap[task.itemID]?.dueDate && 
                        <Typography variant={'taskAttr'} sx={{ color: 'text.secondary', marginLeft: 'auto', marginRight: '8px' }}>
                            {dayjs(taskAttrMap[task.itemID]?.dueDate).format('HH:mm, DD-MM-YY')}
                        </Typography>}
                    {/* Render children */}
                    {task.children && task.children.length > 0 && (
                        <Box>
                            {task.children.map(child => renderTree(child, taskAttrMap))}
                        </Box>
                    )}
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

    // Render the todoitem tree recursively
    const renderTree = (node, taskAttrMap) => {
        return (
            <Box key={node.itemID}>
                {node.itemType === 'Section' ? (
                    <Section section={node} taskAttrMap={taskAttrMap} />
                ) : (
                    taskAttrMap[node.itemID]?.status === 'Pending' && 
                        <Task task={node} taskAttrMap={taskAttrMap} />
                )}
            </Box>
        );
    };

    // Function to render completed tasks
    const renderCompletedTasks = (tasks, taskAttrMap) => {
        if (tasks.length === 0) return <Box></Box>;
        return (
            <Accordion sx = {AccordionSectionStyle} defaultExpanded disableGutters={true}>
                <AccordionSummary expandIcon={<ArrowDropDownIcon size="small" stroke="bold" />} 
                    aria-controls="panel1a-content" id="panel1a-header"
                    alignItems='center'
                    justifyContent='center'
                    sx = {AccordionSummaryStyle}>
                    <Typography variant='section'>Completed</Typography>
                </AccordionSummary>
                <AccordionDetails disablePadding sx = {{ padding: '0px 10px 10px 10px'}}>
                    {tasks.map(task => (
                        <Box key={task.itemID}>
                            <Task task={task} taskAttrMap={taskAttrMap} />
                        </Box>
                    ))}
                </AccordionDetails>
            </Accordion>
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
        setViewTaskDetailID(null);
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [searchParams]);

    // Cleanup function
    React.useEffect(() => {
        return () => setViewTaskDetailID(null)
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    const taskNameField = () => {
        return (
            <TextField
                type="text"
                size="small"
                variant='standard'
                value={newTaskName}
                placeholder='Task Name'
                onChange={(e) => setNewTaskName(e.target.value)}
                onKeyUp={handleKeyPressTaskName}
                fullWidth
                sx={{marginBottom: '10px', 
                    "& .MuiInputBase-root::before": { borderColor: 'border.main' },
                }}
            />
        );
    };

    const taskDescriptionField = () => {
        return (
            <TextField
                type="text"
                value={newTaskDescription}  
                variant="outlined"
                label='Description'
                onChange={(e) => setNewTaskDescription(e.target.value)}
                slotProps={{ htmlInput: { style: { fontSize: 14 } }, 
                            inputLabel: { style: { fontSize: 14 } }
                        }}
                size="small"
                fullWidth
                multiline={true}
                sx={{
                    "& fieldset": { borderColor: 'border.main' },
                    marginBottom: '10px',
                }}
                inputRef={taskDescriptionRef}
                onKeyUp={(e) => { if (e.key === 'Enter' && e.ctrlKey) handleAddTask(); }}
            />  
        );
    }

    const AddTaskField = () => {
        if (selectedProject === null || selectedSection === null) {
            return (<Box></Box>);
        } else return (
            <Box sx = {{ 
                    border: '1px solid', 
                    borderColor: 'border.main', 
                    borderRadius: '5px', 
                    padding: '15px', 
                    margin: '10px 0px',
                    backgroundColor: 'white', 
            }}>
                {taskNameField()}
                {showTaskDescription && taskDescriptionField()}
                <Box sx={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                    <SectionPicker
                        sectionList={sectionList}
                        selectedSection={selectedSection}
                        setSelectedSection={setSelectedSection}
                    />
                    {/* Due date selection */}
                    <DateTimePickerButtonDialog
                        selectedDate={selectedDate}
                        setSelectedDate={setSelectedDate}
                    />
                    {/* Priority selection */}
                    <PriorityPicker priority={selectedPriority} setPriority={setSelectedPriority} />

                    <Button onClick={() => handleAddTask()} variant="contained" startIcon={<AddRoundedIcon />} size="small"
                            float='right' sx={{ marginLeft: 'auto' }}>
                            Add
                    </Button>
                </Box>
            </Box>
        );
    };

    return (
        <Box sx={{ padding: '15px' }}>
            <Helmet>
                <title>Inbox - FocusTask</title>
            </Helmet>
            {/* Add Task */}
            {AddTaskField()}
            {/* Render the tree */}
            <div>
                {Object.values(tree).length > 0 ? (
                    Object.values(tree).map(root => renderTree(root, taskAttrMap))
                ) : (
                    <Box justifyContent='center' alignItems='center' display='flex' height='100vh'> <CircularProgress /> </Box>
                )}
            </div>
            {/* Add Section */}
            {isAddingSection ? (
                <ClickAwayListener onClickAway={handleCancleAddSection}>
                    <div>
                        <TextField
                            type="text"
                            value={newSectionName}
                            onChange={(e) => setNewSectionName(e.target.value)}
                            fullWidth
                            size='small'
                            label='Section Name'
                            inputRef={newSectionNameRef}
                        />
                    </div>
                </ClickAwayListener>
            ) : (            
                <Button onClick={handleNewSectionClick} 
                    fullWidth startIcon={<Plus set="bulk"/>}>
                    New Section
                </Button>)
            }
            {/* Completed Tasks Section */}
            <div>
                {Object.values(tree).length > 0 ? (
                    renderCompletedTasks(
                        Object.values(tree).flatMap(root => root.children.filter(task => taskAttrMap[task.itemID]?.status === 'Completed')),
                        taskAttrMap
                    )
                ) : (
                    <Box justifyContent='center' alignItems='center' display='flex' height='100vh'> <CircularProgress /> </Box>
                )}
            </div>
        </Box>
    );
}

export default HomePage;