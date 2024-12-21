import styles from './SideBar.module.css';

import { callAPITemplate } from '../utils';

import React from 'react';
import { useNavigate, NavLink } from 'react-router-dom';

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
            'http://localhost:8000/todolist/api/project/add',
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
            'http://localhost:8000/todolist/api/project/get_all',
            JSON.stringify({ "authenticationToken": authToken }),
        );
        const items = dataItems.map(item => JSON.parse(item));
        setProjects(items);
    }
    // handle className for navbar items
    const handleNavLinkClassName = ({ isActive }) => isActive ?
        `${styles.navbarItem} ${styles.navbarItemActive}` : styles.navbarItem


    // Check if the authentication token is still valid
    // navigate to /signin if needed
    React.useEffect(() => {
        const authToken = localStorage.getItem('authToken');
        if (authToken === null) {
            navigate('/signin');
        }
        else {
            callAPITemplate(
                'http://localhost:8000/todolist/api/authentication/status',
                JSON.stringify({ "authenticationToken": authToken }),
                (data) => {
                    if (!data.status) {
                        localStorage.removeItem('authToken');
                        navigate('/signin');
                    }
                },
            );
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);
    // Get all projects
    React.useEffect(() => {
        fetchProjectList();
    }, []);


    return (
        <div className={styles.container}>
            <h1>SideBar</h1>
            <nav className={styles.navbar}>
                <li><NavLink className={handleNavLinkClassName} to='/'>Inbox</NavLink></li>
                <li><NavLink className={handleNavLinkClassName} to='/today'>Today</NavLink></li>
            </nav>
            <p>Pomodoro</p>

            <button onClick={() => callSignOutAPI()}>Sign Out</button>

            <div className={styles.projectContent}>
                <h2 className={styles.projectTitle}>Projects</h2>

                {/* add project button and its logic */}
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

                {/* project list */}
                <div className={styles.projectList}>{
                    projects.map(project =>
                        <button
                            key={project.itemID}
                            className={selectedProject === project.itemID
                                ? `${styles.project} ${styles.projectActive}`
                                : styles.project}
                            onClick={() => setSelectedProject(project.itemID)}
                        >{project.name}</button>
                    )
                }</div>
            </div>
        </div>
    );
}

export default SideBar;