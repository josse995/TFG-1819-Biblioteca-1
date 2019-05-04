# -*- coding: utf-8 -*-
"""
Servidor de TFG - Proyecto Janet
Versión 0.9.0

@author: Mauricio Abbati Loureiro - Jose Luis Moreno Varillas
© 2018-2019 Mauricio Abbati Loureiro - Jose Luis Moreno Varillas. All rights reserved.
"""

from ActionsController import Action


class ActionTitle(Action):

    def __init__(self, mongo, wms):
        Action.__init__(self, mongo, wms)

    def accion(self, intent, entities, response, uid):
        respuesta = response

        hayEntitie = False
        for ent in entities:
            if 'libro' in ent:
                hayEntitie = True
        if hayEntitie:
            respuesta['books'] = self.wms.buscarLibro(entities['libro'], None, entities['searchindex'], 'title')
            if not respuesta['books']:
                del respuesta['books']
                respuesta['content-type'] = 'text'
                respuesta['response'] = 'Vaya, parece que no hay libros relacionados con esta consulta'
            else:
                if len(respuesta['books']) == 1:
                    respuesta.update(self.wms.cargarInformacionLibro(respuesta['books'][0]['oclc']))
                    del respuesta['books']
                    respuesta['content-type'] = 'single-book'
                    self.mongo.guardar_consulta(uid, respuesta, 'consulta_libros_titulo')
                    return respuesta

                if intent == 'consulta_libros_titulo':
                    respuesta['content-type'] = 'list-books'
                else:
                    respuesta.update(self.wms.cargarInformacionLibro(respuesta['books'][0]['oclc']))
                    del respuesta['books']
                    respuesta['content-type'] = 'single-book'
                self.mongo.guardar_consulta(uid, respuesta, intent)

        return respuesta