const getCSRFToken = () => {
    
    const tokenInput = document.querySelector('[name=csrfmiddlewaretoken]');
   
    if (tokenInput) return tokenInput.value;

    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];

    return cookieValue || '';

};

export const loginUser = async (data) => {

    try {

        const response = await fetch('/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok)
            throw new Error(result.err || 'Failed to login user.');
        
        return result;

    } catch (err) {

        console.error('api/auth script loginUser function error: ', err);
        throw err;

    }

};

