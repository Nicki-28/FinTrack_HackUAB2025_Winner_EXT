	

chrome.action.onClicked.addListener((tab) => {
    console.log('URL de la pestaña:', tab.url);

    if (!tab.url) {
        console.error('No se pudo obtener la URL de la pestaña.');
        return;
    }

     // Enviar la URL al servidor Flask para analizarla
    fetch('http://127.0.0.1:5000/check', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: tab.url })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Respuesta del servidor:', data);
        if (data && data.result) {
            const result = data.result;
            chrome.notifications.create('', {
                type: 'basic',
                iconUrl: 'icon4.png',
                title: 'Análisis de página',
                message: result
            });
        } else {
            console.error('No se recibió la respuesta esperada', data);
        }
    })
    .catch(error => {
        console.error('Error en la solicitud:', error);
    });
});
