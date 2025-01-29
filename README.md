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

End-point (URL): [http://0.0.0.0:10050//tapatappV1/Username](http://127.0.0.1:10050//tapatappV1/Username)

Method: GET

Tipus de petició (headers): 

Content-Type: application/json.

Parametres que necessita la petició:

-username = String username

Resposta:

{
  "email": "usuari1@gmail.com",
  "id": 1,
  "username": "usuari1" 
} 200

"error": "User not found", 404
"error": "Username not provided", 400
