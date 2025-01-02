import React from 'react';

import { callAPITemplate } from '../utils';
import { Divider, Typography, Box, TextField } from '@mui/material';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import { IconButton } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';

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
        <Box>
            <Typography variant='h6'>Website Block List</Typography>
            <Divider sx={{ mb: 1 }}/>
            <TextField
                type="text"
                value={newWebsite}
                onChange={(e) => setNewWebsite(e.target.value)}
                label="Website URL"
                size='small'
                onKeyUp = {(e) => {
                    if (e.key === 'Enter') {
                        addWebsite();
                    }
                }}
                helperText="Ex: facebook.com; Press Enter to add"
            />
            <List sx={{
                    height: '300px',
                    overflow: 'auto',
                }}>
                {blockList.map((blockItem) => (
                    <ListItem key={blockItem.blockID} secondaryAction={
                        <IconButton edge="end" aria-label="delete"
                            onClick={() => deleteWebsite(blockItem.blockID)}
                            sx={{
                                '&:hover': {
                                    color: 'red',
                                }
                            }}>
                            <DeleteIcon />
                        </IconButton>
                    }>
                        <ListItemText>
                            {blockItem.URL}
                        </ListItemText>
                        {/* <button onClick={() => deleteWebsite(blockItem.blockID)}>Delete</button> */}
                    </ListItem>
                ))}
            </List>
        </Box>
    );
};

export default WebBlockList;