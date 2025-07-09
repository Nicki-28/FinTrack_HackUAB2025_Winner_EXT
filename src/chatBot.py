
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
            return "Lo siento, ha habido un error en tu consulta."
    except requests.exceptions.RequestException as e:
        print("Ha ocurrido un error, por el momento no puedo ayudarte. Inténtalo más tarde", e)
    except Exception as e:
        print("Por el momento no tengo consejos financieros para ti", e)


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    query_str = data.get('query', '')

    if not query_str:
        return jsonify({"error": "Consulta no proporcionada"}), 400

    respuesta = obtener_respuesta(query_str) 
    return jsonify({"reply": respuesta})

if __name__ == '__main__':
    app.run(debug=True)