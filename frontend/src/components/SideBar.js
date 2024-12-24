import styles from './SideBar.module.css';

import React from 'react';
import { useNavigate, NavLink, UNSAFE_decodeViaTurboStream } from 'react-router-dom';

import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import { Button, Fab } from '@mui/material';
import List from '@mui/material/List';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import InboxIcon from '@mui/icons-material/MoveToInbox';
import MailIcon from '@mui/icons-material/Mail';
import AddIcon from '@mui/icons-material/Add';

import LogoText from '../components/LogoText';
import { callAPITemplate } from '../utils'; 

const drawerWidth = 260;


function SideBar({ selectedProject, setSelectedProject }) {
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
    // handle className for navbar items
    const handleNavLinkClassName = ({ isActive }) => isActive ?
        `${styles.navbarItem} ${styles.navbarItemActive}` : styles.navbarItem


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
            <List>
                {['Inbox', 'Today', 'Pomodoro', 'Completed', 'Trash'].map((text, index) => (
                    <ListItem key={text} disablePadding>
                        <ListItemButton>
                            <ListItemIcon>
                                {index % 2 === 0 ? <InboxIcon /> : <MailIcon />}
                            </ListItemIcon>
                            <ListItemText primary={text} />
                        </ListItemButton>
                    </ListItem>
                ))}
            </List>

            <Divider />

            <Box className={styles.projectContent}>
                <Box flexDirection={'row'} display={'flex'} justifyContent={'space-between'} alignItems={'center'}>
                    <Typography variant='drawer'>Projects</Typography>

                    {/* add project button and its logic */}
                    <Fab aria-label="add"
                            color="primary_fade"
                            onClick={() => setIsAddingProject(true)}
                            size="small"
                            float="right" style={{ transform: 'scale(0.5)' }}
                            variant="extended"
                            sx={{ boxShadow: 0 }}>
                        <AddIcon/>
                    </Fab>
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