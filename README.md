# Tapatapp
Proyecto de entornos donde dasarollaremos el aplicativo tapatapp

## Descripció

[Descripció](Descripció.md)

## Requisits

[Requisits](Requisits.md)

Model E/R

![image](https://github.com/user-attachments/assets/c1178d92-1b17-4b45-9505-0a5871406751)

## Prototip 1

![image](https://github.com/user-attachments/assets/e178af31-c711-4232-817c-3bf618896f1e)


## HTTP Request / Response

[HTTP Request](HttpRequest.md)

[HTTP Response](HttpResponse.md)

# Definició dels EndPoints del WebService

## Definició dels EndPoints del Servei Web:

Què necessitem per cada End-point

Descripció: 

HOST: Domain port

End-point (URL): https://api.tapatapp.com/users/get/recurs

Method: GET

Tipus de petició (headers): 

Content-Type: application/json.

Authorization: Bearer <token>.

Parametres que necessita la petició:

-id = id
-username = username
-password = password
-email = email

Resposta:

200 OK: si la petició es processa correctament.
404 Not Found: si no es troba el recurs.

{
  "id": 123,
  "nom": "Exemple",
  "actiu": true
}
