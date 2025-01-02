import React from 'react';

import { callAPITemplate } from '../utils';

const WebBlockList = () => {
    const [blockList, setBlockList] = React.useState([]);
    const [newWebsite, setNewWebsite] = React.useState('');

    // Fetch the block list
    const fetchBlockList = async () => {
        const authToken = localStorage.getItem('authToken');
        try {
            console.log("Fetching block list");
            console.log(authToken);
            const dataBlockItems = await callAPITemplate(
                `${process.env.REACT_APP_API_URL}/website_block/get_block_list`,
                JSON.stringify({ authenticationToken: authToken }),
            );
            const blockItems = dataBlockItems.map(item => JSON.parse(item));
            setBlockList(blockItems);
        }
        catch (e) {
            console.error(e);
        }
    };

    // Add a website to the block list
    const addWebsite = async () => {
        const authToken = localStorage.getItem('authToken');
        callAPITemplate(
            `${process.env.REACT_APP_API_URL}/website_block/add_url`,
            JSON.stringify({ authenticationToken: authToken, URL: newWebsite }),
            () => fetchBlockList(),
            setNewWebsite('')
        );
    };

    // Delete a website from the block list
    const deleteWebsite = async (blockID) => {
        const authToken = localStorage.getItem('authToken');
        callAPITemplate(
            `${process.env.REACT_APP_API_URL}/website_block/delete_url`,
            JSON.stringify({ authenticationToken: authToken, blockID: blockID }),
            () => fetchBlockList()
        );
    };

    React.useEffect(() => {
        fetchBlockList();
    }, []);

    return (
        <div>
            <h2>Website Block List</h2>
            <ul>
                {blockList.map((blockItem) => (
                    <li key={blockItem.blockID}>
                        {blockItem.URL}
                        <button onClick={() => deleteWebsite(blockItem.blockID)}>Delete</button>
                    </li>
                ))}
            </ul>
            <input
                type="text"
                value={newWebsite}
                onChange={(e) => setNewWebsite(e.target.value)}
                placeholder="Add a website URL"
            />
            <button onClick={() => addWebsite()}>Add</button>
            <p>Example: facebook.com</p>
        </div>
    );
};

export default WebBlockList;