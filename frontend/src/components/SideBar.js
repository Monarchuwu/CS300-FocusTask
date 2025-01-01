import React from 'react';
import { useNavigate, NavLink, useLocation, useSearchParams } from 'react-router-dom';

import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import { IconButton, TextField, Menu, MenuItem } from '@mui/material';
import List from '@mui/material/List';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Avatar from '@mui/material/Avatar';

import {
    Message, Calendar, TimeCircle,
    TickSquare, ArrowRightSquare,
    Plus, Setting, User, Logout, MoreSquare
} from 'react-iconly';

import LogoText from '../components/LogoText';
import { callAPITemplate } from '../utils';

const items = [
    { text: 'Inbox', icon: <Message set="bulk" />, url: '/' },
    { text: 'Today', icon: <Calendar set="bulk" />, url: '/today' },
    { text: 'Upcoming', icon: <ArrowRightSquare set="bulk" />, url: '/upcoming' },
    { text: 'Pomodoro', icon: <TimeCircle set="bulk" />, url: '/pomodoro' },
    { text: 'Completed', icon: <TickSquare set="bulk" />, url: '/completed' },
];

function SideBar() {
    const navigate = useNavigate();
    const location = useLocation();
    const [searchParams] = useSearchParams();
    // State variables for adding new project
    const [isAddingProject, setIsAddingProject] = React.useState(false);
    const [newProjectName, setNewProjectName] = React.useState("");
    // State variable for displaying all projects
    const [projects, setProjects] = React.useState([]);
    const textFieldRef = React.useRef(null);
    const [anchorEl, setAnchorEl] = React.useState(null);
    const open = Boolean(anchorEl);
    // State variable for username
    const [username, setUsername] = React.useState('Username');

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
            `${process.env.REACT_APP_API_URL}/user/signout`,
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
        const items = dataItems
            .map(item => JSON.parse(item))
            .filter(item => item.name !== '');
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

    React.useEffect(() => {
        const loadUsername = async () => {
            const authToken = localStorage.getItem('authToken');
            callAPITemplate(
                `${process.env.REACT_APP_API_URL}/user/get_username`,
                JSON.stringify({ "authenticationToken": authToken }),
            ).then(data => setUsername(data));
        }
        loadUsername();
    }, []);

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };
    const handleClose = (event) => {
        setAnchorEl(null);
        if (event.currentTarget.id === 'logout') {
            callSignOutAPI();
            console.log('Logging out');
        }
    };

    const isSelected = (item) => {
        return location.pathname === item.url && (location.pathname !== '/' || location.search === '');
    }


    return (
        <Drawer
            sx={{
                height: '100vh',
                '& .MuiDrawer-paper': {
                    boxSizing: 'border-box',
                    px: '25px',
                    py: '30px',
                    borderColor: 'border.main',
                    position: 'relative',
                },
            }}
            variant="permanent"
            anchor="left"
        >
            <LogoText style={{ marginBottom: "15px" }} />
            <List component="nav" id="MainList">
                {items.map((item) => (
                    <ListItem key={item.text} disablePadding>
                        <ListItemButton
                            component={NavLink}
                            to={item.url}
                            sx={{
                                backgroundColor: isSelected(item) ? 'primary.main' : 'inherit',
                                color: isSelected(item) ? 'white' : 'text.secondary',
                                '&:hover': {
                                    backgroundColor: isSelected(item) ? 'primary.main' : 'primary.light',
                                    color: isSelected(item) ? 'white' : 'text.secondary',
                                },
                                borderRadius: '10px'
                            }}
                        >
                            <ListItemIcon sx={{ color: isSelected(item) ? 'white' : 'text.secondary' }}>
                                {item.icon}
                            </ListItemIcon>
                            <ListItemText primary={item.text}
                                slotProps={{ primary: { fontWeight: 500, fontSize: '16px' } }}
                            />
                        </ListItemButton>
                    </ListItem>
                ))}
            </List>

            <Divider />

            <Box id="ProjectList">
                <Box flexDirection={'row'} display={'flex'}
                    justifyContent={'space-between'} alignItems={'center'}
                    sx={{ marginTop: '10px' }}>
                    <Typography variant='drawer'>Projects</Typography>

                    {/* add project button and its logic */}
                    <IconButton aria-label="add"
                        color="primary"
                        onClick={() => setIsAddingProject(true)}
                        size="small"
                        float="right"
                        disableFocusRipple={true}>
                        <Plus set="bulk" />
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
                            sx={{ marginTop: '5px' }}
                        />
                    </Box>
                )}

                {/* project list */}
                <List id="ProjectListItems">
                    {projects.map(project => (
                        <ListItem disablePadding key={project.itemID}>
                            <ListItemButton
                                onClick={() => {
                                    navigate({
                                        pathname: '/',
                                        search: `?project=${project.name}`,
                                    });
                                }}
                                sx={{
                                    backgroundColor: searchParams.get('project') === project.name ? 'primary.main' : 'inherit',
                                    color: searchParams.get('project') === project.name ? 'white' : 'text.secondary',
                                    '&:hover': {
                                        backgroundColor: searchParams.get('project') === project.name ? 'primary.main' : 'primary.light',
                                        color: searchParams.get('project') === project.name ? 'white' : 'text.secondary',
                                    },
                                    borderRadius: '10px'
                                }}
                            >
                                <ListItemText primary={project.name} 
                                    slotProps={{ primary: { fontWeight: 500, fontSize: '16px' } }} />
                            </ListItemButton>
                        </ListItem>
                    ))}
                </List>
            </Box>
            <Box flexGrow={1} />
            <Box id="User"
                flexDirection={'row'} display={'flex'}
                justifyContent={'space-between'}
                gap="8px"
                alignItems={'center'}
                sx={{
                    marginTop: '10px',
                    display: 'flex',
                    justifyContent: 'center',
                    borderRadius: '10px',
                    border: '1px solid',
                    borderColor: 'border.main',
                    padding: '8px',
                    marginBottom: 0,
                }}>
                <Avatar sx={{
                    bgcolor: 'primary.light',
                    color: 'primary.main',
                    borderRadius: '5px',
                    width: 48,
                    height: 48
                }}>
                    <User set="bulk" width={30} height={30} />
                </Avatar>
                <Typography variant='body2' id="UserName"
                    flexGrow={1}
                    color="#53515B"
                >{username}</Typography>
                <IconButton onClick={handleClick}
                    float="right"
                    aria-controls={open ? 'account-menu' : undefined}
                    aria-haspopup="true"
                    aria-expanded={open ? 'true' : undefined}
                >
                    <MoreSquare set="bulk" />
                </IconButton>
                <Menu
                    anchorEl={anchorEl}
                    id="account-menu"
                    open={open}
                    onClose={handleClose}
                    onClick={handleClose}
                    transformOrigin={{ horizontal: 'left', vertical: 'bottom' }}
                    anchorOrigin={{ horizontal: 'left', vertical: 'top' }}
                >
                    <MenuItem onClick={handleClose} id="settings">
                        <ListItemIcon><Setting set="bulk" /></ListItemIcon>
                        <Typography variant="body2">
                            Settings
                        </Typography>
                    </MenuItem>
                    <MenuItem onClick={handleClose} id="logout">
                        <ListItemIcon><Logout set="bulk" /></ListItemIcon>
                        <Typography variant="body2">
                            Log out
                        </Typography>
                    </MenuItem>
                </Menu>
            </Box>
        </Drawer>
    );
}

export default SideBar;