import logofile from '../assets/images/logo-text.png';

import React from 'react';

const LogoText = (props) => {
    return (
        <img src={logofile} alt="FocusTask Logo" {...props} />
    );
}

export default LogoText;