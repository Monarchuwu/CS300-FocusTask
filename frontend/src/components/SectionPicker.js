import React from 'react';

import { Box, Button, IconButton, Menu, MenuItem, Typography } from '@mui/material';
import { Folder } from 'react-iconly';

const SectionPicker = ({ sectionList, selectedSectionName, setSelectedSectionName, addingSectionID, setAddingSectionID }) => {
    const [anchorEl, setAnchorEl] = React.useState(null);

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    const handleMenuItemClick = (sectionID) => {
        const sectionName = sectionList.current[sectionID];
        setAddingSectionID(parseInt(sectionID));
        setSelectedSectionName(sectionName);
        handleClose();
    };

    return (
        <Box id="sectionSelection">
            {selectedSectionName === '' || selectedSectionName === null ? (
                <IconButton onClick={handleClick} size='small' color="text.primary">
                    <Folder set="light" />
                </IconButton>
            ) : (
                <Button onClick={handleClick} startIcon={<Folder set="bulk" />} 
                    variant="outlined" size="small" color="primary">
                    {selectedSectionName}
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
                            backgroundColor: addingSectionID === parseInt(sectionID) ? 'lightblue' : 'white',
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