import React from "react";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import Menu from "@mui/material/Menu";
import { Tooltip } from "@mui/material";
import { MenuItem, Typography } from "@mui/material";
import { InfoSquare } from "react-iconly";

import { getPriorityColor } from "../utils";

const PriorityPickerMenu = ({ setSelectedPriority, priorityAnchorEl, setPriorityAnchorEl }) => {

    const handlePriorityClose = () => {
        setPriorityAnchorEl(null);
    };

    const handlePriorityMenuItemClick = (priority) => {
        setSelectedPriority(priority);
        handlePriorityClose();
    };

    return (
        <Menu
            anchorEl={priorityAnchorEl}
            open={Boolean(priorityAnchorEl)}
            onClose={handlePriorityClose}
        >
            {['High', 'Medium', 'Low'].map((priority) => (
                <MenuItem
                    key={priority}
                    onClick={() => handlePriorityMenuItemClick(priority)}
                >
                    <Typography variant="body2" color={getPriorityColor(priority)}>
                        {priority}
                    </Typography>
                </MenuItem>
            ))}
        </Menu>
    );
};

const PriorityPicker = ({ priority, setPriority }) => {
    const [priorityAnchorEl, setPriorityAnchorEl] = React.useState(null);

    const handlePriorityClick = (e) => {
        setPriorityAnchorEl(e.currentTarget);
    };
    
    return (
        <Box id="prioritySelection">
            <Tooltip title="Priority">
                {priority === null ? (
                    <IconButton onClick={handlePriorityClick} size="small">
                        {/* rotate the icon 180 degree */}
                        <InfoSquare set="light" style={{ transform: 'rotate(180deg)' }} />
                    </IconButton>
                ) : (
                    <Button onClick={handlePriorityClick} 
                        startIcon={<InfoSquare set="bulk" style={{ transform: 'rotate(180deg)' }}/>} 
                        variant="outlined" size="small" sx={{ 
                            color: getPriorityColor(priority), 
                            borderColor: getPriorityColor(priority),
                        }}>
                        {priority}
                    </Button>
                )}
            </Tooltip>
            <PriorityPickerMenu
                setSelectedPriority={setPriority}
                priorityAnchorEl={priorityAnchorEl}
                setPriorityAnchorEl={setPriorityAnchorEl}
            />
        </Box>
    );
}

export default PriorityPicker;