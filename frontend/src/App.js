import './App.css';
import React from 'react';

function App() {
    const [message, setMessage] = React.useState("");
    const [response, setResponse] = React.useState("");

    const callTestAPI = async (message) => {
        try {
            const response = await fetch('http://localhost:8000/todolist/api/test_api', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ "message": message }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            setResponse(data);
        }
        catch (e) {
            console.error('There was a problem with the fetch operation:', e);
            setResponse('Error: ' + e.message);
        }
    }

    return (
        <div className='App'>
            <h1>Send a simple request to the backend via the API</h1>
            <input
                type='text'
                value={message}
                onChange={e => setMessage(e.target.value)}
                placeholder="Enter your text here"
            />
            <button onClick={() => { callTestAPI(message) }}>Send</button>
            <p>Response: {JSON.stringify(response)}</p>
        </div>
    );
}

export default App;
