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

### Descripció: 

HOST: Domain port

End-point (URL): [http://0.0.0.0:10050//tapatappV1/Username](http://127.0.0.1:10050/tapatappV1/Username)

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

### Descripció: 

HOST: Domain port

End-point (URL): [http://0.0.0.0:10050/tapatappV1/register](http://127.0.0.1:10050/tapatappV1/register)

Method: POST

Tipus de petició (headers): 

Content-Type: application/json.

Parametres que necessita la petició:

-username = String username

-password = String password

-email = String email

Resposta:

"error": "Username already exists"}), 400

"message": "User registered successfully", 201

### Descripció: 

HOST: Domain port

End-point (URL): [http://0.0.0.0:10050/tapatappV1/validate_parameters](http://127.0.0.1:10050/tapatappV1/validate_parameters)

Method: GET

Tipus de petició (headers): 

Content-Type: application/json.

Parametres que necessita la petició:

-username = String username

Resposta:

{
"errors": [
"Username parameter is missing.",
"Email parameter is missing."
]
}

"errors": errors, 400

"message": "Parameters are valid.", 200

## Prototip 2

## Wireframes

[Diagrama](https://github.com/mactiburon/tapatapp/blob/main/Prototype2/DiagramaVistaP2.mermaid)

## Descripció del prototip 2

### Funcionalidades Principales
### Gestión de Usuarios:

Los usuarios pueden registrarse y acceder a la aplicación mediante un sistema de login.
La aplicación gestiona diferentes tipos de usuarios, como Administradores, Tutores, Cuidadores y Seguimiento Médico.
El acceso a las funcionalidades de la aplicación está restringido según el rol de cada usuario.

### Gestión de Niños:

Los tutores y cuidadores pueden registrar información sobre los niños, incluyendo su nombre, edad, fecha de nacimiento y cualquier información médica relevante.
Los registros también incluyen un historial de sueño, donde se almacena información detallada sobre el sueño de cada niño, como las fechas, las horas de inicio y fin, y el estado del sueño (por ejemplo, si están dormidos, despiertos, etc.).
Esta información se organiza en un formato de fácil acceso y consulta para el personal autorizado.

### Seguimiento del Sueño:

Cada niño tiene un historial de sueño asociado con fechas específicas, donde se pueden registrar las horas de sueño y la calidad del descanso.
Este seguimiento es útil para los profesionales médicos que deseen realizar un seguimiento de los hábitos de sueño de los niños, detectando posibles irregularidades o patrones que requieran atención.

### Interacción con la API:

La aplicación se comunica con un servidor para gestionar el login, el registro de usuarios y la obtención de datos de los niños.
Los usuarios pueden interactuar con el sistema mediante solicitudes HTTP, como el login, el registro de nuevos niños y la obtención de información sobre el historial médico de los niños.

### Interfaz de Consola:

La aplicación cuenta con una interfaz de consola amigable que permite a los usuarios interactuar con el sistema a través de un menú con opciones como Login, Registro de Usuario, Ver Información de Niños, y Salir.
Esta interfaz facilita la consulta y actualización de datos médicos de manera intuitiva.
Componentes del Proyecto

### Clases Principales:

Usuario: Representa a los usuarios del sistema con sus atributos como nombre, apellido, email y contraseña.
Nen: Representa a los niños, con datos como nombre, edad, fecha de nacimiento, información médica y su historial de sueño.
UsuarioDAO: Contiene métodos para interactuar con el servidor y gestionar el login y registro de usuarios.
NenDAO: Se encarga de obtener la información de los niños desde la base de datos del servidor.
ViewConsole: Proporciona una interfaz de consola para interactuar con el usuario, permitiéndole ingresar datos y mostrar información.

### Interacción con el Servidor:

La aplicación realiza solicitudes HTTP POST y GET al servidor para gestionar la autenticación de usuarios y recuperar los datos de los niños.
En el caso de un login o registro, el sistema envía las credenciales al servidor y recibe una respuesta con el estado de la operación.

## Diagrama de Arquitectura 

## Diagrama de Backend

## Diagrama de Frontend
