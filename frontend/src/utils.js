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