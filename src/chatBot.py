#QUERY
import requests
import json
from config import API_KEY
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

url = "https://api.perplexity.ai/chat/completions" 

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def obtener_respuesta(query_str):
    # Crear los mensajes para la solicitud
    messages = [
        {
            "role": "system",
            "content": "Eres un asistente financiero llamado Finn. Analiza los gastos y da consejos de ahorro. Presentate primero."
        },
        {
            "role": "user",
            "content": f"Gastos del mes: {query_str}"
        }
    ]

    data = {
        "model": "sonar-pro", 
        "messages": messages
    }

    try:
        # Hacer la solicitud a la API
        response = requests.post(url, json=data, headers=headers)

       
        #print(f"Código de respuesta: {response.status_code}")
        #print("Contenido de la respuesta:", response.text)  

        if response.status_code == 200:
            result = response.json()
            print("Análisis Financiero:")
            print(result['choices'][0]['message']['content'])  # Acceder al contenido de la respuesta
        else:
            print("Error al llamar a la API:", response.status_code)
            print(response.json())

    except requests.exceptions.RequestException as e:
        print("Ha ocurrido un error, por el momento no puedo ayudarte. Inténtalo más tarde", e)
    except Exception as e:
        print("Por el momento no tengo consejos financieros para ti", e)

    # Solicitar la consulta al usuario
    query_input = input("Ingresa tu consulta o escribe 'salir' para terminar: ")

    # Crear el query a partir de la entrada del usuario
    query_str = f"Consulta: {query_input}"

    # Llamar a la función para obtener la respuesta del bot
    obtener_respuesta(query_str)


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    query_str = data.get('query', '')

    if not query_str:
        return jsonify({"error": "Consulta no proporcionada"}), 400

    obtener_respuesta(query_str)
    return jsonify({"message": "Consulta procesada"}), 200

if __name__ == '__main__':
    app.run(debug=True)