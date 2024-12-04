from flask import Flask, request, jsonify
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

    # app.run(host="127.0.0.1", port=5002 , debug=True)
    app.run(debug=True, host='0.0.0.0', port=5002)


