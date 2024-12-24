import styles from './BarChart24.module.css';

import React from 'react';

function BarChart24({ data }) {
    return (
        <div>
            <p>BarChart24</p>
            <div className={styles.chart}>
                {data.map((item, index) => {
                    // Calculate the width of each bar
                    const barHeight = (item[0] / 3600) * 100 + 1;
                    return (
                        <div key={index} className={styles.barContainer}>
                            <span className={styles.labelHour}>{index}</span>
                            <div className={styles.bar} style={{ height: `${barHeight}px` }} />
                            <span className={styles.label}>{parseInt(item[0] / 60)}</span>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}

export default BarChart24;