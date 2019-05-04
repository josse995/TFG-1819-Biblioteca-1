# -*- coding: utf-8 -*-
"""
Servidor de TFG - Proyecto Janet
Versión 0.9.0

@author: Mauricio Abbati Loureiro - Jose Luis Moreno Varillas
© 2018-2019 Mauricio Abbati Loureiro - Jose Luis Moreno Varillas. All rights reserved.
"""

from bottle import request, route, run, response, static_file, error
import JanetServController
import json
import logging


class JanetService:
    def __init__(self):
        # Creacion de logger
        logger = logging.getLogger('janet')
        logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler('janet.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        logger.info("Iniciando módulos.")
        self.controlador = JanetServController.JanetServController(logger)
        logger.info("Preparado.")

        @route('/api', method='POST')
        def do_listen():
            response.content_type = 'application/json'
            response.status = 200

            post_data = {}
            post_data["type"] = request.POST.type
            post_data["content"] = request.POST.content
            post_data["user_id"] = request.POST.user_id
            logger.info("Usuario conectado por POST: " + post_data["user_id"])
            respuesta = self.controlador.procesarDatos_POST(post_data)
            return respuesta

        @route('/', method='GET')
        def do_test():
            HTML = '''<img src="static/icon.png" alt="Logo" width="500" height="500"> <br> <h1> No deberias estar aqui! </h1> <p> Esta direccion es de prueba, conectate con un cliente.</p>'''
            return HTML

        @route('/static/<filepath:path>')
        def server_static(filepath):
            return static_file(filepath, root='./')

        @error(400)
        def custom400(error):
            '''Cuando ocurre un error, bottle no lo convierte en JSON automáticamente,
            así que lo hacemos nosotros. Primero ponemos el `content_type`, y luego
            hacemos el `json.dumps` del diccionario. En el error 400, decimos que ha
            habido un error y en los detalles ponemos la explicación para que el usuario
            sepa qué ha hecho mal.'''
            response.content_type = 'application/json'
            logger.error('Error 400: ' + error.body)
            return json.dumps({
                'errorno': 400,
                'errorMessage': error.body
            })

        @error(404)
        def custom404(error):
            '''El error 404 no necesita demasiada información.'''
            response.content_type = 'application/json'
            logger.error('Error 404: ' + error.body)
            return json.dumps({
                'errorno': 404,
                'errorMessage': 'No existe el recurso solicitado.'
            })

        @error(500)
        def custom500(error):
            '''En el caso del error 500, no le damos información al usuario porque son
            detalles de nuestro servidor y puede ser un fallo de seguridad. Estos
            errores ocurren cuando nuestro código python ha fallado, por lo que habrá
            que mirar la salida de error del programa para verlos.'''
            response.content_type = 'application/json'
            logger.error('Error 500: ' + str(error.exception))
            return json.dumps({
                'errorno': 500,
                'errorMessage': 'Ha habido un problema imprevisto.',
            })


if __name__ == '__main__':
    JanetService()
    run(host='0.0.0.0', port=8080, reloader=True, interval=3600)