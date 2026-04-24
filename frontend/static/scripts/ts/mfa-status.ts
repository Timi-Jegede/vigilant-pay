export interface UrlType {
    url: string
    status: boolean
}

export async function set_mfa_status(config:UrlType) {
    try {
        const csrftoken = document.cookie.split(';').find(row => row.startsWith('csrftoken='))
                            ?.split('=')[1];
        const response = await fetch(config.url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken
            },
            body: new URLSearchParams({
                'mfa_status': config.status.toString()
            })
        });

        if (!response.ok) {
            throw new Error(`Response Status: ${response.status}`)
        }
        
        const result = await response.json();
        return result
        
    } catch (error) {
        throw error;
    }
}