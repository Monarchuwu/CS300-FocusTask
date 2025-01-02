import React from 'react';

import { Box, Button, IconButton, Menu, MenuItem, Typography } from '@mui/material';
import { Folder } from 'react-iconly';

const SectionPicker = ({ sectionList, selectedSection, setSelectedSection }) => {
    const [anchorEl, setAnchorEl] = React.useState(null);

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    const handleMenuItemClick = (sectionID) => {
        const sectionName = sectionList.current[sectionID];
        // sectionList.current = Object.fromEntries(sectionItems.map(section => [section.itemID, section.name]));
        setSelectedSection({ itemID: parseInt(sectionID), name: sectionName });
        handleClose();
    };

    return (
        <Box id="sectionSelection">
            {selectedSection?.name === '' || selectedSection?.name === null ? (
                <IconButton onClick={handleClick} size='small' color="text.primary">
                    <Folder set="light" />
                </IconButton>
            ) : (
                <Button onClick={handleClick} startIcon={<Folder set="bulk" />} 
                    variant="outlined" size="small" color="primary">
                    {selectedSection?.name}
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
                            backgroundColor: selectedSection?.itemID === parseInt(sectionID) ? 'lightblue' : 'white',
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
    );
};

export default SectionPicker;