import { Box, Typography } from '@mui/material';

export const callAPITemplate = async (
    url = '',
    bodyString = '',
    success = (data) => { },
    error = (message) => { },
    fetchError = (e) => { }
) => {
    if (typeof url !== 'string') {
        throw new TypeError('url must be a string');
    }
    if (typeof bodyString !== 'string') {
        throw new TypeError('bodyString must be a string');
    }
    if (typeof success !== 'function') {
        throw new TypeError('success must be a function');
    }
    if (typeof error !== 'function') {
        throw new TypeError('error must be a function');
    }
    if (typeof fetchError !== 'function') {
        throw new TypeError('fetchError must be a function');
    }

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: bodyString,
        });

        const data = await response.json();
        if (data.status === 'success') {
            success(data.data);
            return data.data;
        }
        else {
            console.error(data.message || 'An error occurred');
            error(data.message);
        }
    }
    catch (e) {
        console.error('There was a problem with the fetch operation:', e);
        fetchError(e);
    }
}

export const getPriorityColor = (priority) => {
    if (priority === 'High') return 'priority.high';
    else if (priority === 'Medium') return 'priority.medium';
    else if (priority === 'Low') return 'priority.low';
    else return 'text.primary';
};


// Convert seconds to display format MM:SS
export const displaySeconds = (seconds) => {
    if (typeof (seconds) !== 'number' || seconds < 0) {
        return "type error";
    }
    // display in format MM:SS
    const minutes = Math.floor(seconds / 60);
    seconds %= 60;
    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
};


// Convert seconds to display format HHhMMm
export const displaySecondsHour = (seconds) => {
    if (typeof (seconds) !== 'number' || seconds < 0) {
        return "type error";
    }
    // display in format HHhMMm
    const hours = Math.floor(seconds / 3600);
    seconds %= 3600;
    const minutes = Math.floor(seconds / 60);
    return `${hours}h${minutes}m`;
};

export const AccordionSectionStyle = {
    border: '1px solid',
    borderColor: 'border.main',
    borderRadius: '5px',
    margin: '15px 0px',
    boxShadow: 'none',
    backgroundColor: 'white',
    '&.MuiAccordion-root.Mui-expanded': {
        margin: '15px 0px',
    }
};

export const AccordionSummaryStyle = {
    margin: '0px',
    fontFamily: 'Plus Jakarta Sans',
    fontWeight: '600',
    color: 'text.primary',
    '.MuiAccordionSummary-content': {
        transition: 'margin 0.3s ease',
    },
    '&.Mui-expanded': {
        minHeight: '30px',
        
        '.MuiAccordionSummary-content': {
            marginBottom: '2px',
            transition: 'margin 0.3s ease',
        } 
    } 
};

export const Priority = ({ priority }) => {
    return (
        <Box sx={{
                display: 'inline-flex',
                padding: '2px 8px',
                margin: '4px',
                justifyContent: 'center',
                alignItems: 'center',
                borderRadius: '100px',
                color: getPriorityColor(priority),
                backgroundColor: priority === 'High' ? 'priority.highBackground' : priority === 'Medium' ? 'priority.mediumBackground' : 'priority.lowBackground',
            }}>
            <Typography variant='taskAttr'>{priority}</Typography>
        </Box>
    );
};

export const TaskBoxStyle = {
    boxSizing: 'border-box',
    border: '1px solid',
    borderColor: 'border.main',
    borderRadius: '5px',
    padding: '2px',
    margin: '5px',
    "&:hover": {
        backgroundColor: 'white',
        boxShadow: '0px 2px 5px 0px rgba(0,0,0,0.2)',
        transition: 'background-color 0.1s ease, box-shadow 0.1s ease',
        "& button": {
            display: 'inline',
        }
    },
    "& button": {
        display: 'none',
    },
    cursor: 'pointer',
};