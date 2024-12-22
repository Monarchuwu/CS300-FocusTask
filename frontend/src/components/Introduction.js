import styles from './Introduction.module.css';

import React from 'react';

import { Typography, Box } from '@mui/material';

function Introduction() {
    return (
        <div className={styles.introduction}>
            <Typography variant="h1">Welcome to FocusTask</Typography>
            <Typography variant="sh">
                Stay organized and focused with FocusTask, the productivity tool that combines task management with distraction blocking. Unlike other apps, FocusTask automatically blocks distracting websites as deadlines approach, helping you stay on track and meet your goals. Try it today and work smarter!
            </Typography>
            <Box component="img" src={`${process.env.PUBLIC_URL}/preview.png`} 
                alt="Preview UI of FocusTask"
                sx={{
                    width: '100%',
                    borderRadius: '8px',
                    boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.1)',
                    mt: '24px',
                }} />
        </div>
    )
}

export default Introduction;
