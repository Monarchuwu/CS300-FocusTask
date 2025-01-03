import React from 'react';
import { BarChart } from '@mui/x-charts/BarChart';
import { displaySecondsHour } from '../utils';
import { Box, Divider, Typography } from '@mui/material';
import { callAPITemplate } from '../utils';

const FocusStatistics = () => {
    const [statistic, setStatistic] = React.useState(null);
    const total = React.useMemo(() => {
        if (!statistic) return 0;
        // Calculate total focus time in seconds
        return parseInt(statistic.reduce((acc, cur) => acc + cur.minutes * 60, 0));
    }, [statistic]);

    const format = (data) => {
        const result = [];
        data.forEach((element, index) => {
            const hour = index % 24;
            result.push({ hour: hour, minutes: element[0]/60 });
        });
        return result;
    }

    // Fetch statistic
    const fetchStatistic = async () => {
        const authToken = localStorage.getItem('authToken');
        callAPITemplate(
            `${process.env.REACT_APP_API_URL}/pomodoro/get_history_hour_fullday`,
            JSON.stringify({ "authenticationToken": authToken, "date": new Date().toISOString() }),
            (data) => {setStatistic(format(data));},
        )
    }

    // Fetch statistic on page load
    React.useEffect(() => {
        fetchStatistic();
    });

    const chartSetting = {
        yAxis: [
            {
                label: 'Minutes',
            },
        ],
        width: 300,
        height: 200,
    };

    return (
        <Box>
            <Typography variant="h6">Focus Statistics</Typography>
            <Divider />
            <Box display="flex" 
                sx={{
                    justifyContent: 'center',
                    alignItems: 'center',
                    flexDirection: 'column',
                    gap: 2,
                }}>
                {
                    !statistic ? 
                    <div>No Statistic</div> :
                    <BarChart
                        dataset={statistic}
                        xAxis={[{ 
                            dataKey: 'hour', 
                            scaleType: 'band', 
                            label: 'Hour',
                        }]}
                        series={[{ dataKey: 'minutes' }]}
                        {...chartSetting}
                    />
                }
                <Box display="flex" flexDirection="column" justifyContent={'center'} alignItems={'center'}>
                    <Typography variant="body1">Today's focus</Typography> 
                    <Typography variant="num_data" color='primary.main'>{displaySecondsHour(total)}</Typography>
                </Box>
            </Box>
        </Box>
    );
};

export default FocusStatistics;