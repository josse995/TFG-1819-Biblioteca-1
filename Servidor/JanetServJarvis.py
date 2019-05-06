# -*- coding: utf-8 -*-
"""
Servidor de TFG - Proyecto Janet
Versión 1.0

MIT License

Copyright (c) 2019 Mauricio Abbati Loureiro - Jose Luis Moreno Varillas

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from urllib import request, parse, error
import json

class JanetServJarvis():

    def consultar(self, pregunta, id):
        contenido = pregunta
        contenido = contenido[0].lower() + contenido[1:]
        data = {'user_id': id, 'content': contenido}

        try:
            req = request.Request("http://localhost:5000", data=parse.urlencode(data).encode())
            resp = request.urlopen(req)
        except error.URLError as e:
            msg = "Janet se encuentra en mantenimiento en estos momentos. " \
                      "Inténtelo de nuevo más tarde"
            raise error.HTTPError("http://localhost:5000", 400, msg, None, None)

        return json.load(resp)

    def restart(self, id):
        data = {'user_id': id, 'content': '/restart'}

        req = request.Request("http://localhost:5000", data=parse.urlencode(data).encode())
        request.urlopen(req)