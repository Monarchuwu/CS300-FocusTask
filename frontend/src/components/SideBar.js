import styles from './SideBar.module.css';

import { callAPITemplate } from '../utils';

import React from 'react';
import { useLocation, useNavigate, NavLink } from 'react-router-dom';

function SideBar() {
    const navigate = useNavigate();
    const location = useLocation();


    // API call functions
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
        </div>
    );
}

export default SideBar;