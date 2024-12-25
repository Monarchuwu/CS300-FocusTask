import styles from './SideBar.module.css';

import React, {useRef} from 'react';
import { useNavigate, NavLink } from 'react-router-dom';

import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import { IconButton, TextField } from '@mui/material';
import List from '@mui/material/List';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';

import { Home, Calendar, TimeCircle, TickSquare, ArrowRightSquare, Plus } from 'react-iconly';

import LogoText from '../components/LogoText';
import { callAPITemplate } from '../utils'; 

const drawerWidth = 260;

const items = [
    { text: 'Inbox', icon: <Home set="bulk" />, url: '/' },
    { text: 'Today', icon: <Calendar set="bulk" />, url: '/today' },
    { text: 'Upcoming', icon: <ArrowRightSquare set="bulk" />, url: '/upcoming' },
    { text: 'Pomodoro', icon: <TimeCircle set="bulk" />, url: '/pomodoro' },
    { text: 'Completed', icon: <TickSquare set="bulk" />, url: '/completed' }, 
];

function SideBar({ selectedProject, setSelectedProject}) {
    const navigate = useNavigate();
    // State variables for adding new project
    const [isAddingProject, setIsAddingProject] = React.useState(false);
    const [newProjectName, setNewProjectName] = React.useState("");
    // State variable for displaying all projects
    const [projects, setProjects] = React.useState([]);
    const textFieldRef = useRef(null);

    // API call functions
    const callAddProjectAPI = async (name) => {
        const authToken = localStorage.getItem('authToken');
        callAPITemplate(
            `${process.env.REACT_APP_API_URL}/project/add`,
            JSON.stringify({ "authenticationToken": authToken, "name": name }),
            (data) => {
                setIsAddingProject(false);
                setNewProjectName("");
                fetchProjectList();
            }
        )
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
    // Fetch all projects and rerender
    const fetchProjectList = async () => {
        const authToken = localStorage.getItem('authToken');
        const dataItems = await callAPITemplate(
            `${process.env.REACT_APP_API_URL}/project/get_all`,
            JSON.stringify({ "authenticationToken": authToken }),
        );
        const items = dataItems.map(item => JSON.parse(item));
        setProjects(items);
    }


    // Get all projects
    React.useEffect(() => {
        fetchProjectList();
    }, []);

    React.useEffect(() => {
        if (isAddingProject && textFieldRef.current) {
            textFieldRef.current.focus();
        }

        const handleClickOutside = (event) => {
            if (textFieldRef.current && !textFieldRef.current.contains(event.target)) {
                setIsAddingProject(false);
                setNewProjectName('');
            }
        };

        if (isAddingProject) {
            document.addEventListener('mousedown', handleClickOutside);
        } else {
            document.removeEventListener('mousedown', handleClickOutside);
        }

        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [isAddingProject]);


    return (
        <Drawer 
            sx={{
                width: drawerWidth,
                flexShrink: 0,
                '& .MuiDrawer-paper': {
                    width: drawerWidth,
                    boxSizing: 'border-box',
                    px: '25px',
                    py: '30px',
                },
            }}
            variant="permanent"
            anchor="left"
        >
            <LogoText style={{ marginBottom: "15px" }}/>
            <List component="nav">
                {items.map((item) => (
                    <ListItem key={item.text} disablePadding>
                        <ListItemButton
                            component={NavLink}
                            to={item.url}
                            onClick={() => setSelectedProject(item.text)}
                            sx={{
                                backgroundColor: selectedProject === item.text ? 'primary.main' : 'inherit',
                                color: selectedProject === item.text ? 'white' : 'gray.main',
                                '&:hover': {
                                    backgroundColor: selectedProject === item.text ? 'primary.main' : 'primary.light',
                                    color: selectedProject === item.text ? 'white' : 'gray.main',
                                },
                                borderRadius: '10px',
                                marginBottom: '2px',
                            }}
                        >
                            <ListItemIcon sx={{ color: selectedProject === item.text ? 'white' : 'gray.main' }}>
                                {item.icon}
                            </ListItemIcon>
                            <ListItemText primary={item.text} 
                                slotProps={{ primary: {fontWeight: 500} }} 
                            />
                        </ListItemButton>
                    </ListItem>
                ))}
            </List>

            <Divider />

            <Box id="ProjectList">
                <Box flexDirection={'row'} display={'flex'} justifyContent={'space-between'} alignItems={'center'}>
                    <Typography variant='drawer'>Projects</Typography>

                    {/* add project button and its logic */}
                    <IconButton aria-label="add"
                            color="primary"
                            onClick={() => setIsAddingProject(true)}
                            size="small"
                            float="right"
                            disableFocusRipple={true}>
                        <Plus set="bulk"/>
                    </IconButton>
                </Box>
                {isAddingProject && (
                    <Box>
                        <TextField
                            label="Project name" 
                            variant="outlined"
                            size="small"
                            type="text"
                            value={newProjectName}
                            onChange={(e) => setNewProjectName(e.target.value)}
                            onKeyUp={(e) => {
                                if (e.key === 'Enter' && newProjectName.trim() !== '') {
                                    callAddProjectAPI(newProjectName);
                                } else if (e.key === 'Escape') {
                                    setIsAddingProject(false);
                                    setNewProjectName("");
                                }
                            }}
                            inputRef={textFieldRef}
                            sx = {{ marginTop: '5px'}}
                        />
                    </Box>
                )}

                {/* project list */}
                <List className={styles.projectList}>
                    {projects.map(project => (
                        <ListItem
                            key={project.itemID}
                            button
                            selected={selectedProject === project.itemID}
                            onClick={() => { setSelectedProject(project.itemID); navigate('/'); }}
                            sx={{
                                backgroundColor: selectedProject === project.itemID ? 'primary.main' : 'inherit',
                                color: selectedProject === project.itemID ? 'white' : 'gray.main',
                                '&:hover': {
                                    backgroundColor: selectedProject === project.itemID ? 'primary.main' : 'primary.light',
                                    color: selectedProject === project.itemID ? 'white' : 'gray.main',
                                },
                                borderRadius: '10px',
                                marginBottom: '2px',
                                cursor: 'pointer',
                            }}
                        >
                            <ListItemText primary={project.name} slotProps={{ primary: {fontWeight: 500} }} />
                        </ListItem>
                    ))}
                </List>
            </Box>
            <button onClick={() => callSignOutAPI()} className={styles.user}>Sign Out</button>
        </Drawer>
    );
}

export default SideBar;