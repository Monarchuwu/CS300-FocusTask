import styles from './SideBar.module.css';

import React, { useState } from 'react';
import { useNavigate, NavLink } from 'react-router-dom';

import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import { IconButton } from '@mui/material';
import List from '@mui/material/List';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';

import { Home, Calendar, TimeCircle, TickSquare, Delete, Plus } from 'react-iconly';

import LogoText from '../components/LogoText';
import { callAPITemplate } from '../utils'; 

const drawerWidth = 260;

const items = [
    { text: 'Inbox', icon: <Home set="bulk" />, url: '/' },
    { text: 'Today', icon: <Calendar set="bulk" />, url: '/today' },
    { text: 'Pomodoro', icon: <TimeCircle set="bulk" />, url: '/pomodoro' },
    { text: 'Completed', icon: <TickSquare set="bulk" />, url: '/completed' },
    { text: 'Trash', icon: <Delete set="bulk" />, url: '/trash' },
];

function SideBar({ selectedProject, setSelectedProject}) {
    const navigate = useNavigate();
    // State variables for adding new project
    const [isAddingProject, setIsAddingProject] = React.useState(false);
    const [newProjectName, setNewProjectName] = React.useState("");
    // State variable for displaying all projects
    const [projects, setProjects] = React.useState([]);

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
            <LogoText />
            {/* <nav className={styles.navbar}>
                <li><NavLink className={handleNavLinkClassName} to='/'>Inbox</NavLink></li>
                <li><NavLink className={handleNavLinkClassName} to='/today'>Today</NavLink></li>
                <li><NavLink className={handleNavLinkClassName} to='/pomodoro'>Pomodoro</NavLink></li>
            </nav> */}
            <List component="nav" aria-label="main mailbox folders">
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
                                    color: 'white',
                                },
                                borderRadius: '10px',
                                marginBottom: '5px',
                            }}
                        >
                            <ListItemIcon sx={{ color: selectedProject === item.text ? 'white' : 'gray.main' }}>
                                {item.icon}
                            </ListItemIcon>
                            <ListItemText primary={item.text} 
                                slotProps={{ primary: {
                                    color: selectedProject === item.text ? 'white' : 'gray.main', 
                                    fontWeight: 500} 
                                }} 
                            />
                        </ListItemButton>
                    </ListItem>
                ))}
            </List>

            <Divider />

            <Box className={styles.projectContent}>
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

                {/* project list */}
                <div className={styles.projectList}>{
                    projects.map(project =>
                        <button
                            key={project.itemID}
                            className={selectedProject === project.itemID
                                ? `${styles.project} ${styles.projectActive}`
                                : styles.project}
                            onClick={() => { setSelectedProject(project.itemID); navigate('/'); }}
                        >{project.name}</button>
                    )
                }</div>
            </Box>
            <button onClick={() => callSignOutAPI()} className={styles.user}>Sign Out</button>
        </Drawer>
    );
}

export default SideBar;