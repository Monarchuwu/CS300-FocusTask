import styles from './HomePage.module.css';

import { callAPITemplate } from '../utils';

import React from 'react';
import { useNavigate } from 'react-router-dom';

function HomePage() {
    const navigate = useNavigate();
    const [isAddingProject, setIsAddingProject] = React.useState(false);
    const [newProjectName, setNewProjectName] = React.useState("");
    const [tree, setTree] = React.useState({});

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
    const buildForest = (items) => {
        const itemMap = {}; // Map items by itemID for easy access
        const tree = {};

        items.forEach(item => {
            itemMap[item.itemID] = { ...item, children: [] };
        });

        items.forEach(item => {
            if (item.parentID === null) {
                tree[item.itemID] = itemMap[item.itemID];
            }
            else if (itemMap[item.parentID]) {
                itemMap[item.parentID].children.push(itemMap[item.itemID]);
            }
        });

        return tree;
    }
    const renderTree = (node) => {
        return (
            <ul key={node.itemID}>
                <li>
                    <strong>{node.name}</strong> ({node.itemType})
                    {node.children && node.children.length > 0 && (
                        <ul>
                            {node.children.map(child => renderTree(child))}
                        </ul>
                    )}
                </li>
            </ul>
        );
    };
    const fetchTodoList = async () => {
        const authToken = localStorage.getItem('authToken');
        callAPITemplate(
            'http://localhost:8000/todolist/api/todo_item/get_all',
            JSON.stringify({ "authenticationToken": authToken }),
            (data) => {
                const items = data.map(item => JSON.parse(item));
                setTree(buildForest(items));
            }
        )
    }
    const callAddProjectAPI = async (name) => {
        const authToken = localStorage.getItem('authToken');
        callAPITemplate(
            'http://localhost:8000/todolist/api/project/add',
            JSON.stringify({ "authenticationToken": authToken, "name": name }),
            (data) => {
                setIsAddingProject(false);
                setNewProjectName("");
            }
        )
    }

    React.useEffect(() => {
        if (localStorage.getItem('authToken') === null) {
            navigate('/signin');
        }
    }, []);
    React.useEffect(() => {
        fetchTodoList();
    }, []);

    return (
        <div>
            <button onClick={() => callSignOutAPI()}>Sign Out</button>
            <h1>Welcome to the Home Page</h1>

            <button onClick={() => setIsAddingProject(true)}>Add project</button>
            {isAddingProject && (
                <div>
                    <input
                        type="text"
                        value={newProjectName}
                        onChange={(e) => setNewProjectName(e.target.value)}
                    />
                    <button onClick={() => setIsAddingProject(false)}>Cancel</button>
                    <button onClick={() => callAddProjectAPI(newProjectName)}>Add</button>
                </div>
            )}

            <div>
                {Object.values(tree).length > 0 ? (
                    Object.values(tree).map(root => renderTree(root))
                ) : (
                    <p>No data available</p>
                )}
            </div>
        </div>
    );
}

export default HomePage;