# Http Response
Una HTTP Response (Resposta HTTP) és la resposta que el servidor envia al client després d'una petició HTTP (com ara una petició GET o POST).

La resposta inclou informació sobre si la petició va ser procesada correctament o si va ocórrer un error.

## Components d'una HTTP request en el HTML

Status Line (Inicia la respuesta, indicando la versión del protocolo, el código de estado y el mensaje asociado).

Response Headers (Proporcionan información sobre la respuesta y el servidor).

Encabezados de Contenido (Especifican el tipo de medio y el tamaño del cuerpo de la respuesta).

Response Body (Contiene los datos que el servidor envía al cliente, como HTML, JSON, o imágenes).

## 1. Codi d'estat 1xx - Informatius

Descripció: Indiquen que el servidor ha rebut la petició i que s'està processant.

Exemples:

100 Continue: El servidor ha rebut la primera part de la petició i el client pot continuar enviant la resta.

101 Switching Protocols: Accepta canviar el protocol segons la petició del client.

## 2. Codi d'estat 2xx - OK

Descripció: Indiquen que la petició s'ha processat correctament.

Exemples:

200 OK: La petició ha estat exitosa; el cos conté els resultats sol·licitats.

201 Created: S'ha creat un nou recurs.

202 Accepted: La petició ha estat acceptada però no processada encara.

204 No Content: La petició ha estat processada amb èxit, però no hi ha contingut per retornar.

## 3. Codi d'estat 3xx - Redirecció

Descripció: Indiquen que el client ha de realitzar una altra acció per completar la petició.

Exemples:

301 Moved Permanently: El recurs ha estat mogut permanentment a una nova URL.

302 Found: El recurs es troba temporalment en una URL diferent.

303 See Other: El client ha de fer una petició GET a una altra URL.

304 Not Modified: El recurs no s'ha modificat des de l'última sol·licitud.

## 4.Codi d'estat 4xx - Errors del client

Descripció: Problemes amb la petició del client.

Exemples:

400 Bad Request: La petició és mal formada.

401 Unauthorized: Falta de credencials.

403 Forbidden: Accés denegat.

404 Not Found: Recurso no trobat.

## 5.Codi d'estat 5xx - Errors del servido

Descripció: Problemes amb el servidor que impedeixen processar la petició.

Exemples:

500 Internal Server Error: Error general del servidor.

501 Not Implemented: Funció no suportada.

502 Bad Gateway: Resposta no vàlida d'un servidor ascendent.

503 Service Unavailable: Servei temporalment no disponible.
