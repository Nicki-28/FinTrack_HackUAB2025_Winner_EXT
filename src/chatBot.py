
import requests
import json
from config import API_KEY
from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import base64


app = Flask(__name__)
CORS(app)

url = "https://api.perplexity.ai/chat/completions" 

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def obtener_respuesta(query_str, image_data_uri=None):
    # Construir mensajes
    if image_data_uri:
        print("tengo la imagen ya codificada")
    if image_data_uri:
        messages = [
            {
                "role": "system",
                "content": "Eres un asistente financiero llamado Finn. Analiza los gastos y da consejos de ahorro. No te presentes"
            },
            {
                "role": "user",
                "content": [ 
                    {"type": "text", "text": query_str},
                    {"type": "image_url", "image_url": {"url": image_data_uri}}
                ]
            }
        ]
    else:
        messages = [
            {
                "role": "system",
                "content": "Eres un asistente financiero llamado Finn. Analiza los gastos y da consejos de ahorro."
            },
            {
                "role": "user",
                "content": query_str
            }
        ]

    data = {
        "model": "sonar-pro",
        "messages": messages
    }

    try:
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            parcialResult = response.json()
            parcialResult1 = parcialResult['choices'][0]['message']['content'] #obtenemos respuesta
            
            #limpiamos la respuesta ( NO FUNCIONA =D)
            parcialResult2= re.sub(r'([a-zA-Z])\d+(?=[\s.,;:]|$)', r'\1', parcialResult1) # "ahorrar2." -> "ahorrar."
            parcialResult3 = re.sub(r'(?<=[\s.,;:])\d+([a-zA-Z])', r'\1', parcialResult2) # "123ahorrar" -> "ahorrar"
            result = re.sub(r"[\[\]\*\#]", "-", parcialResult3) # Elimina [ ] *
        else:
            print("Error al llamar a la API:", response.status_code)
            print(response.json())
            return "Lo siento, ha habido un error en tu consulta."
    except requests.exceptions.RequestException as e:
        print("Ha ocurrido un error, por el momento no puedo ayudarte. Inténtalo más tarde", e)
        return "Error de conexión."
    except Exception as e:
        print("Por el momento no tengo consejos financieros para ti", e)
        return "Error inesperado."

    return result


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    query_str = data.get('query', '') #obtenemos la peticioón

    if not query_str:
        return jsonify({"error": "Consulta no proporcionada"}), 400

    respuesta = obtener_respuesta(query_str) #llamamos al bot
    return jsonify({"reply": respuesta})

@app.route('/upload-image',methods=['POST'])
def uploadImage():
    print("estoy aqui")
    data = request.get_json()
    query_str = data.get('query', '') #obtenemos la peticioón
    image_data_uri = data.get('image', '') #obtenemos la petición
    
    if not image_data_uri:
        return jsonify({"error": "Consulta no proporcionada"}), 400
    
    respuesta= obtener_respuesta(query_str,image_data_uri)
    print("recibi la respuesta de la imagen") #debugging prints
    return jsonify ({"reply": respuesta})

if __name__ == '__main__':
    app.run(debug=True)