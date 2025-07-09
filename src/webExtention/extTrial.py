from flask import Flask, request, jsonify
from flask_cors import CORS  
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
from webdriver_manager.chrome import ChromeDriverManager
import time

app = Flask(__name__)
CORS(app)

def get_trustpilot_url(page_url):
    """Extrae el dominio de la URL y construye la URL de Trustpilot"""
    parsed_url = urlparse(page_url)
    domain = parsed_url.netloc.replace("www.", "")  # Quitamos "www."
    trustpilot_url = f"https://www.trustpilot.com/review/{domain}"
    return trustpilot_url

def check_rating(page_url):
    """Busca el rating en Trustpilot usando Selenium"""
    trustpilot_url = get_trustpilot_url(page_url)  # URL de Trustpilot
    print(f"Analizando: {trustpilot_url}")

    # Configuración de Selenium (Modo headless)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Modo sin interfaz gráfica
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(trustpilot_url)
        time.sleep(3)  # Espera general por si la página tarda en cargar

        # Esperar explícitamente hasta que aparezca el rating, importante para poder agarrar el html
        try:
            rating_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h4.typography_heading-xxs__UmE9o"))
            )
            rating_text = rating_element.text.strip()
            print(f"Rating encontrado: {rating_text}")

            if rating_text in ["Bad", "Poor"]:
                return "No te recomiendo seguir, esta página no es segura"
            elif rating_text in ["Average", "Great", "Excellent"]:
                return "No te preocupes, la página que visitas es segura"
            else:
                return "No he podido analizar esta web, mejor no la uses para compras"

        except Exception:
            print("No se encontró la calificación en Trustpilot.")
            return "No he podido analizar esta web, mejor no la uses"

    except Exception as e:
        print("Error al cargar Trustpilot:", e)
        return "No puedo analizar la seguridad de tu página. Es mejor no arriesgarse!"

    finally:
        driver.quit()

@app.route('/check', methods=['POST'])
def check_reputation():
    data = request.get_json()
    url = data.get('url')
    print(f"URL recibida: {url}")

    result = check_rating(url)
    print(f"Resultado del análisis: {result}")

    return jsonify({'result': result})

if __name__ == "__main__":
    #test_url = "https://www.mercadolibre.com.pe"
    #print(f"Prueba con {test_url}: {check_rating(test_url)}")  # TEST
    app.run(debug=True, host="0.0.0.0", port=5000)
