import React from 'react';

import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import Dialog from '@mui/material/Dialog';
import TextField from '@mui/material/TextField';
import { Calendar } from 'react-iconly';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';

import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import dayjs from 'dayjs';


const DateTimePickerButtonDialog = ({ 
        selectedDate, setSelectedDate,
    }) => {
    const [dueDateOpen, setDueDateOpen] = React.useState(false);
    const [tempDate, setTempDate] = React.useState(dayjs()); // Holds the temporary date

    const handleDueDateClickOpen = () => {
        setDueDateOpen(true);
        setTempDate(dayjs(selectedDate || dayjs())); // Set the temporary date to the last confirmed date
        // console.log('Temp Due Date:', dayjs(tempDate).format());
    };

    const handleDueDateClose = () => {
        setDueDateOpen(false);
        setTempDate(selectedDate); // Reset tempDate to the last confirmed date
    };

    const handleDateChange = (newDate) => {
        setTempDate(newDate); // Update the temporary date as the user selects a new date
        // console.log('Temp Due Date:', dayjs(tempDate).format());
    };


    const handleSetDueDate = () => {
        setSelectedDate(tempDate); // Confirm the date selection
        console.log('Selected Due Date:', dayjs(tempDate).format());
        handleDueDateClose();
    };

    return (<Box id="dueDateSelection">
        {selectedDate === null ? 
            (<IconButton onClick={handleDueDateClickOpen} size="small">
                <Calendar set="light" />
            </IconButton>) 
            : (
                <Button onClick={handleDueDateClickOpen} startIcon={<Calendar set="bulk" />} 
                    variant="outlined" size="small" color="primary">
                    {dayjs(selectedDate).format('HH:mm, DD-MM-YY')}
                </Button>
            )
        }
        <Dialog open={dueDateOpen} onClose={handleDueDateClose}>
            <DialogTitle>Task Due Date</DialogTitle>
            <DialogContent>
                <LocalizationProvider dateAdapter={AdapterDayjs}>
                    <DateTimePicker
                        renderInput={(props) => <TextField {...props} />}
                        value={tempDate || dayjs()}
                        onChange={handleDateChange}
                    />
                </LocalizationProvider>
            </DialogContent>
            <DialogActions>
                <Button onClick={handleDueDateClose} color="danger" variant="outlined">
                    CANCEL
                </Button>
                <Button onClick={handleSetDueDate} color="primary" autoFocus variant="contained">
                    CONFIRM
                </Button>
            </DialogActions>
        </Dialog>
    </Box>
    );
};

export default DateTimePickerButtonDialog;