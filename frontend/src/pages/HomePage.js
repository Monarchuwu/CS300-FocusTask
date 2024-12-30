import { callAPITemplate } from '../utils';

import React from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';

import { CircularProgress, Box, Typography, 
        Checkbox, Accordion, AccordionDetails, 
        AccordionSummary, 
        IconButton, Menu, MenuItem} from '@mui/material';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import ReadMoreRoundedIcon from '@mui/icons-material/ReadMoreRounded';
import DeleteRoundedIcon from '@mui/icons-material/DeleteRounded';
import AddRoundedIcon from '@mui/icons-material/AddRounded';
import { Helmet } from 'react-helmet';
import { Dialog, DialogActions, DialogContent, 
    DialogContentText, DialogTitle, Button, TextField } from '@mui/material';
import { Plus, Folder, Calendar } from 'react-iconly';
import { ClickAwayListener } from '@mui/base/ClickAwayListener';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import dayjs from 'dayjs';


function HomePage({ viewTaskDetailID, setViewTaskDetailID, updateTaskAttrs, setUpdateTaskAttrs }) {
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();
    const [selectedProject, setSelectedProject] = React.useState(null);
    // State variables for adding new section
    const [isAddingSection, setIsAddingSection] = React.useState(false);
    const [newSectionName, setNewSectionName] = React.useState("");
    // State variables for adding new task
    const [addingSectionID, setAddingSectionID] = React.useState(null);
    const [selectedSectionName, setSelectedSectionName] = React.useState(null);
    const [newTaskName, setNewTaskName] = React.useState("");
    const [newTaskDescription, setNewTaskDescription] = React.useState("");
    // State variables for rendering the tree
    const [tree, setTree] = React.useState({}); // Forest of items that will be rendered
    const [taskAttrMap, setTaskAttrMap] = React.useState({}); // Mapping from taskID to task attributes
    const sectionList = React.useRef({}); // Mapping from sectionID to sectionName
    const sectionDefaultID = React.useRef(null); // sectionID of sectionName is '' (default section)
    // State variable for debouncing status (checkbox) changes
    const [debounceStatus, setDebounceStatus] = React.useState({}); // Queue to smoothly change checkbox state
    const [openDialog, setOpenDialog] = React.useState(false);
    const [taskToDelete, setTaskToDelete] = React.useState(null);
    const newSectionNameRef = React.useRef(null);
    const [anchorEl, setAnchorEl] = React.useState(null);

    const [dueDateOpen, setDueDateOpen] = React.useState(false);
    const [selectedDate, setSelectedDate] = React.useState(null);
    const [tempDate, setTempDate] = React.useState(dayjs()); // Holds the temporary date

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    const handleDueDateClickOpen = () => {
        setDueDateOpen(true);
    };

    const handleDueDateClose = () => {
        setDueDateOpen(false);
        setTempDate(selectedDate); // Reset tempDate to the last confirmed date
    };

    const handleDateChange = (newDate) => {
        setTempDate(newDate); // Update the temporary date as the user selects a new date
        console.log('Temp Due Date:', dayjs(tempDate).format());
    };


    const handleSetDueDate = () => {
        setSelectedDate(tempDate); // Confirm the date selection
        console.log('Selected Due Date:', dayjs(selectedDate).format());
        handleDueDateClose();
    };

    const handleMenuItemClick = (sectionID) => {
        const sectionName = sectionList.current[sectionID];
        setAddingSectionID(parseInt(sectionID));
        setSelectedSectionName(sectionName);
        handleClose();
    };


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
        handleCloseDialog();
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
            const items = dataItem.map(item => JSON.parse(item)).filter(item => item.itemID !== projectID);
            setTree(buildForest(items, projectID));

            // Fetch checkbox status of tasks
            const taskIDs = items.filter(item => item.itemType === 'Task').map(task => task.itemID);
            const dataAttributes = await callAPITemplate(
                `${process.env.REACT_APP_API_URL}/task_attributes/get_list`,
                JSON.stringify({ "authenticationToken": authToken, "itemIDs": taskIDs }),
            );
            const attrsList = dataAttributes.map(attr => JSON.parse(attr));
            const taskAttrMap = Object.fromEntries(attrsList.map(attr => [attr.taskID, attr]));
            setTaskAttrMap(taskAttrMap);

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
    const Priority = ({ priority }) => {
        return (
            <Box sx={{
                    display: 'inline-flex',
                    padding: '2px 8px',
                    margin: '4px',
                    justifyContent: 'center',
                    alignItems: 'center',
                    borderRadius: '100px',
                    color: priority === 'High' ? 'priority.high' : priority === 'Medium' ? 'priority.medium' : 'priority.low',
                    backgroundColor: priority === 'High' ? 'priority.highBackground' : priority === 'Medium' ? 'priority.mediumBackground' : 'priority.lowBackground',
                }}>
                <Typography variant='taskAttr'>{priority}</Typography>
            </Box>
        );
    };

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
        callAddTaskAPI(newTaskName, addingSectionID ? 
                        addingSectionID : sectionDefaultID.current, selectedDate, undefined, undefined, newTaskDescription
                        );
        setAddingSectionID(null);
        setNewTaskName("");
        setNewTaskDescription("");
        setSelectedDate(null);
        setSelectedSectionName(null);
        setTempDate(dayjs());
    };


    const Section = ({ section, taskAttrMap }) => {
        return (
            <Accordion sx = {{
                    border: '1px solid',
                    borderColor: 'border.main',
                    borderRadius: '5px',
                    margin: '15px 0px',
                    boxShadow: 'none',
                    backgroundColor: 'white',
                    '&.MuiAccordion-root.Mui-expanded': {
                        margin: '15px 0px',
                    }
                }} defaultExpanded disableGutters={true}>
                {section.name !== '' && 
                    <AccordionSummary expandIcon={<ArrowDropDownIcon size="small" stroke="bold" />} 
                        aria-controls="panel1a-content" id="panel1a-header"
                        alignItems='center'
                        justifyContent='center'
                        sx = {{ 
                            margin: '0px',
                            fontFamily: 'Plus Jakarta Sans',
                            fontWeight: '600',
                            color: 'text.primary',
                            '.MuiAccordionSummary-content': {
                                transition: 'margin 0.3s ease',
                            },
                            '&.Mui-expanded': {
                                minHeight: '30px',
                                
                                '.MuiAccordionSummary-content': {
                                    marginBottom: '2px',
                                    transition: 'margin 0.3s ease',
                                } 
                            } 
                        }}>
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
        return (
            <React.Fragment>
            <Box key={task.itemID}
                sx = {{
                    boxSizing: 'border-box',
                    border: '1px solid',
                    borderColor: 'border.main',
                    borderRadius: '5px',
                    padding: '2px',
                    margin: '5px',
                    backgroundColor: task.itemID === viewTaskDetailID ? 'white' : 'gray.light',
                    boxShadow: task.itemID === viewTaskDetailID ? '0px 2px 5px 0px rgba(0,0,0,0.2)' : 'none',
                    "&:hover": {
                        backgroundColor: 'white',
                        boxShadow: '0px 2px 5px 0px rgba(0,0,0,0.2)',
                        transition: 'background-color 0.1s ease, box-shadow 0.1s ease',
                        "& button": {
                            display: 'inline',
                        }
                    },
                    "& button": {
                        display: task.itemID === viewTaskDetailID ? 'inline' : 'none',
                    }
                }}>
                <Box alignItems='center' display={'block'}>
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
                    <IconButton onClick={() => setViewTaskDetailID(task.itemID)} 
                        size='small' color="text.secondary" sx={{ width: '34px', height: '34px' }}>
                        <ReadMoreRoundedIcon />
                    </IconButton>
                    {task.name !== '' &&                 
                    <IconButton onClick={() => handleOpenDialog(task.itemID)} color="danger"
                        size='small' sx={{ width: '34px', height: '34px' }}>
                        <DeleteRoundedIcon/>
                    </IconButton>}
                    {taskAttrMap[task.itemID]?.dueDate && 
                        <Typography variant={'taskAttr'} sx={{ color: 'text.secondary' }}>
                            {taskAttrMap[task.itemID]?.dueDate}
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
                    <Task task={node} taskAttrMap={taskAttrMap} />
                )}
            </Box>
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

    const taskNameField = () => {
        return (
            <TextField
                type="text"
                size="small"
                variant='standard'
                value={newTaskName}
                placeholder='Task Name'
                onChange={(e) => setNewTaskName(e.target.value)}
                fullWidth
                sx={{marginBottom: '10px'}}
            />
        );
    }

    const taskDescriptionField = () => {
        return (
            <TextField
                type="text"
                value={newTaskDescription}  
                variant='outlined'
                label='Description'
                onChange={(e) => setNewTaskDescription(e.target.value)}
                slotProps={{ htmlInput: { style: { fontSize: 14 } }, 
                            inputLabel: { style: { fontSize: 14 } }
                        }}
                size="small"
                multilines
                fullWidth
            />  
        );
    }

    const AddTaskField = (selectedProject, addingSectionID) => {
        if (selectedProject === null || addingSectionID === null) {
            return (<Box></Box>);
        } else return (
            <Box sx = {{ 
                    border: '2px solid', 
                    borderColor: 'border.main', 
                    borderRadius: '5px', 
                    padding: '15px', 
                    margin: '10px 0px',
                    backgroundColor: 'white', 
            }}>
                {taskNameField()}
                {taskDescriptionField()}
                {/* Section selection */}
                <Box sx={{ display: 'flex', marginTop: '10px', alignItems: 'center', gap: '5px' }}>
                    <Box id="sectionSelection">
                        {selectedSectionName === '' || selectedSectionName === null ? (
                            <IconButton onClick={handleClick} size='small' color="text.primary">
                                <Folder set="light" />
                            </IconButton>
                        ) : (
                            <Button onClick={handleClick} startIcon={<Folder set="bulk" />} 
                                variant="outlined" size="small" color="primary">
                                {selectedSectionName}
                            </Button>
                        )}
                        <Menu
                            anchorEl={anchorEl}
                            open={Boolean(anchorEl)}
                            onClose={handleClose}
                        >
                            {Object.entries(sectionList.current).map(([sectionID, sectionName]) => (
                                <MenuItem
                                    key={sectionID}
                                    onClick={() => handleMenuItemClick(sectionID)}
                                    style={{
                                        backgroundColor: addingSectionID === parseInt(sectionID) ? 'lightblue' : 'white',
                                        color: sectionName === '' ? 'default' : 'primary'
                                    }}
                                >
                                    <Typography variant="body2" color={'text.primary'}>
                                        {sectionName === '' ? '---' : sectionName}
                                    </Typography>
                                </MenuItem>
                            ))}
                        </Menu>
                    </Box>
                    {/* Due date selection */}
                    <Box id="dueDateSelection">
                        {selectedDate === null ? 
                            (<IconButton onClick={handleDueDateClickOpen} size="small">
                                <Calendar set="light" />
                            </IconButton>) 
                            : (
                                <Button onClick={handleDueDateClickOpen} startIcon={<Calendar set="bulk" />} 
                                    variant="outlined" size="small" color="primary">
                                    {dayjs(selectedDate).format('DD-MM-YYYY HH:mm')}
                                </Button>
                            )
                        }
                        <Dialog open={dueDateOpen} onClose={handleDueDateClose}>
                            <DialogTitle>Task Due Date</DialogTitle>
                            <DialogContent>
                                <LocalizationProvider dateAdapter={AdapterDayjs}>
                                    <DateTimePicker
                                        renderInput={(props) => <TextField {...props} />}
                                        value={tempDate || dayjs()}
                                        onChange={handleDateChange}
                                    />
                                </LocalizationProvider>
                            </DialogContent>
                            <DialogActions>
                                <Button onClick={handleDueDateClose} color="danger" variant="outlined">
                                    CANCEL
                                </Button>
                                <Button onClick={handleSetDueDate} color="primary" autoFocus variant="contained">
                                    CONFIRM
                                </Button>
                            </DialogActions>
                        </Dialog>
                    </Box>
                
                    {/* <button onClick={() => { setAddingSectionID(sectionDefaultID.current); 
                        setNewTaskName(""); setNewTaskDescription(""); }}>
                        Cancel
                    </button> */}
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
            {AddTaskField(selectedProject, addingSectionID)}
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
        </Box>
    );
}

export default HomePage;