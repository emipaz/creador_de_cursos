from flask import Flask, request, jsonify
import threading
import webbrowser
import os
from flask_cors import CORS
from flask_talisman import Talisman
from utils import (add_target_blank_to_links,
                   create_logger,
                markdown_to_html_with_math)
from bot import Chatbot

app = Flask(__name__)
CORS(app)
talisman = Talisman(app, content_security_policy=None)

logger = create_logger('api.py')


def wait_for_exit():
    while True:
        command = input("Escribe 'salir' para apagar el servidor: ").strip().lower()
        if command == 'salir':
            print("Apagando el servidor...")
            os._exit(0)  # Forzar la salida completa del script

def open_browser():
    # Ruta local del archivo HTML
    base = os.path.dirname(os.path.abspath(__file__))
    html_file = os.path.join(base, "public_html", "index.html")  # Cambia esto por la ruta real
    webbrowser.open(f"file://{html_file}")


@app.route('/api', methods=['POST'])
def chatbot():
       
    # Obtener la consulta del JSON recibido
     
    data = request.get_json()
    query = data['query']
    history = data['history']
    bot = int(data['bot'])
    
    chatbot = Chatbot(bot)
    # Llamar a la función para obtener la respuesta
    # por defecto tercer parametro usar_funcion = False
    pregunta, prompt, respuesta = chatbot.generar_respuesta_system(
        query, history)  #usar_func=USAR_GOOGLE_SHEET)
    
    # Registrar mensajes a medida que el script va ejecutandose
    logger.info(f"Pregunta bot {bot}: {pregunta} \n" )
    logger.info(f"Prompt bot {bot}:\n {prompt}\n")
    logger.info(f"Respuesta bot {bot}:\n {respuesta} \n")
    
    # Preparar la respuesta en formato JSON
    #response = {'response': make_links_clickable(respuesta)}
    response = {'response': add_target_blank_to_links(markdown_to_html_with_math(respuesta))}
                #"registrado":chatbot.registrado}
    
    # Devolver la respuesta en formato JSON
    return jsonify(response)


if __name__ == '__main__':

    threading.Timer(1, open_browser).start()
    threading.Timer(2, wait_for_exit).start()
    app.run(host="127.0.0.1", port=5002 , debug=True, use_reloader=False)


