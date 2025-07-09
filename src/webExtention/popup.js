document.addEventListener('DOMContentLoaded', function () {
    const button = document.getElementById('checkButton'); 
    const resultDiv = document.getElementById('result');

    button.addEventListener('click', function () {
        // Efecto de clic en el botón
        button.style.transform = "scale(0.95)";
        setTimeout(() => {
            button.style.transform = "scale(1)";
        }, 100);

        // Obtener la URL activa de la pestaña
        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
            const url = tabs[0].url; 
            fetch('http://127.0.0.1:5000/check', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url: url })
            })
            .then(response => response.json())
            .then(data => {
                console.log("Resultado recibido:", data.result); // DEBUG
                const result = data.result;
            
                document.body.style.background = "white";
                button.style.display = "none";
                resultDiv.innerText = result;
                resultDiv.style.display = "block";  
                resultDiv.style.fontSize = "18px";
                resultDiv.style.fontWeight = "bold";
                resultDiv.style.padding = "10px";
                resultDiv.style.borderRadius = "5px";
            
                // Forzar cambio de color con los colores deseados
                setTimeout(() => {
                    if (result.includes("recomiendo")) {
                        resultDiv.style.color ='red'; // Páginas NO seguras
                    } else if (result.includes("segura")) {
                        resultDiv.style.color = 'green'; // Páginas seguras
                    } else {
                        resultDiv.style.color = 'gray'; // Desconocido / Error
                    }
                }, 50);
            })
            .catch(error => {
                console.error('Error al obtener los resultados:', error);
                
                // Ocultar el botón y limpiar el fondo
                document.body.style.background = "white";
                button.style.display = "none";

                // Mostrar mensaje de error
                resultDiv.innerText = 'Error al obtener los resultados.';
                resultDiv.style.color = 'red';
                resultDiv.style.display = "block";
            });
        });
    });
});
