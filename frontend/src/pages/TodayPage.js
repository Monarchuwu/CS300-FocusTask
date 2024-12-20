import styles from './TodayPage.module.css';

import { callAPITemplate } from '../utils';

import React from 'react';
import { useNavigate } from 'react-router-dom';

function TodayPage() {
    const navigate = useNavigate();

    return (
        <div>
            <h1>Today</h1>
        </div>
    )
}

export default TodayPage;