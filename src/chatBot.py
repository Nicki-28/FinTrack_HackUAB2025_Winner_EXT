
import requests
import json
from config import API_KEY
from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import base64
from chatbot_memory.memoriaChat import cargar_memoria, guardar_memoria



app = Flask(__name__)
CORS(app)

url = "https://api.perplexity.ai/chat/completions" 

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def obtener_respuesta(query_str, image_data_uri=None):
    # Cargar memoria del historial
    historial = cargar_memoria()

    # Base del mensaje: sistema
    messages = [
        {
            "role": "system",
            "content": "Eres un asistente financiero llamado Finn. Analiza los gastos y da consejos de ahorro. No te presentes"
        }
    ]

    # Agregar últimos intercambios del historial (máx 6)
    for mensaje in historial[-6:]:
        if "user" in mensaje:
            messages.append({"role": "user", "content": mensaje["user"]})
        elif "bot" in mensaje:
            messages.append({"role": "assistant", "content": mensaje["bot"]})

    # Agregar el nuevo input en caso de IMAGEN
    if image_data_uri:
        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": query_str},
                {"type": "image_url", "image_url": {"url": image_data_uri}}
            ]
        })
    else:
        messages.append({"role": "user", "content": query_str})

    # Preparar payload
    data = {
        "model": "sonar-pro",
        "messages": messages
    }

    try:
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            parcialResult = response.json()
            parcialResult1 = parcialResult['choices'][0]['message']['content'] #obtenemos respuesta
            
            #limpiamos la respuesta ( NO FUNCIONA =D al 100%)
            parcialResult2= re.sub(r'([a-zA-Z])\d+(?=[\s.,;:]|$)', r'\1', parcialResult1) # "ahorrar2." -> "ahorrar."
            parcialResult3 = re.sub(r'(?<=[\s.,;:])\d+([a-zA-Z])', r'\1', parcialResult2) # "123ahorrar" -> "ahorrar"
            result = re.sub(r"[\[\]\*\#]", "", parcialResult3) # Elimina [ ] *
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

    historial = cargar_memoria ()

    #guardo también el historial de consulta del usuario
    historial.append ({"user": query_str})

    #guardamos también la respuesta
    respuesta = obtener_respuesta(query_str) 

    historial.append({"bot": respuesta})
    guardar_memoria(historial)
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
    app.run(host="0.0.0.0", port=5000,debug=True)