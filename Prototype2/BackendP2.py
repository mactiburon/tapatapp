from datetime import date, time
from flask import Flask, request

class User:
    def __init__(self, id, username, password, email):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
    
    def __str__(self):
        return self.username + ":" + self.password + ":" + self.email

users = [
    User(id=1, username="mare", password="12345", email="prova@gmail.com"),
    User(id=2, username="pare", password="123", email="prova2@gmail.com")
]

class Child:
    def __init__(self, id, child_name, sleep_average, treatment_id, time):
        self.id = id
        self.child_name = child_name
        self.sleep_average = sleep_average
        self.treatment_id = treatment_id
        self.time = time
  
    def __str__(self):
        return self.child_name + ":" + self.sleep_average + ":" + self.treatment_id  + ":" + self.time

class Tap:
    def __init__(self, id, child_id, status_id, user_id, init, end):
        self.id = id
        self.child_id = child_id
        self.status_id = status_id
        self.user_id = user_id
        self.init = init
        self.end = end

    def __str__(self):
        return self.id + ":" + self.child_id + ":" + self.status_id  + ":" + self.user_id + ":" + self.init + ":" + self.end

class Role:
    def __init__(self, id, type_rol):
        self.id = id
        self.type_rol = type_rol

    def __str__(self):
        return self.id + ":" + self.type_rol
    
class Status:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return self.id + ":" + self.name
    
class Treatment:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return self.id + ":" + self.name

class LlistaNens:
    def __init__(self):
        self.nens = []

    def afegirNen(self, nen: Child):
        self.nens.append(nen)

    def eliminarNen(self, nomNen: str):
        self.nens = [nen for nen in self.nens if nen.child_name != nomNen]

    def buscarNen(self, nomNen: str) -> Child:
        for nen in self.nens:
            if nen.child_name == nomNen:
                return nen
        return None


class Perfil:
    def __init__(self, nom: str, cognom: str, email: str, altresDades: str):
        self.nom = nom
        self.cognom = cognom
        self.email = email
        self.altresDades = altresDades

    def veurePerfil(self):
        print(f"Nom: {self.nom}, Cognom: {self.cognom}, Email: {self.email}, Altres dades: {self.altresDades}")

    def actualitzarPerfil(self, nom: str, cognom: str, email: str):
        self.nom = nom
        self.cognom = cognom
        self.email = email
        print("Perfil actualitzat correctament.")


class Nen:
    def __init__(self, nom: str, edat: int, dataNaixement: date, informacioMedica: str):
        self.nom = nom
        self.edat = edat
        self.dataNaixement = dataNaixement
        self.informacioMedica = informacioMedica
        self.historialTapat = LlistaHistorial()

    def afegirHistorial(self, historial: 'HistorialTapat'):
        self.historialTapat.afegirHistorial(historial)


class LlistaHistorial:
    def __init__(self):
        self.historial = []

    def afegirHistorial(self, historial: 'HistorialTapat'):
        self.historial.append(historial)

    def eliminarHistorial(self, data: date):
        self.historial = [h for h in self.historial if h.data != data]

    def buscarHistorial(self, data: date) -> 'HistorialTapat':
        for h in self.historial:
            if h.data == data:
                return h
        return None


class HistorialTapat:
    def __init__(self, data: date, hora: time, estat: str, totalHores: int):
        self.data = data
        self.hora = hora
        self.estat = estat
        self.totalHores = totalHores

    def __str__(self):
        return f"Data: {self.data}, Hora: {self.hora}, Estat: {self.estat}, Total hores: {self.totalHores}"

children = [
    Nen(id=1, child_name="Carol Child", sleep_average=8, treatment_id=1, time=6),
    Nen(id=2, child_name="Jaco Child", sleep_average=10, treatment_id=2, time=6)
]

taps = [
    Tap(id=1, child_id=1, status_id=1, user_id=1, init="2024-12-18T19:42:43", end="2024-12-18T20:42:43"),
    Tap(id=2, child_id=2, status_id=2, user_id=2, init="2024-12-18T21:42:43", end="2024-12-18T22:42:43")
]

relation_user_child = [
    {"user_id": 1, "child_id": 1, "rol_id": 1},
    {"user_id": 1, "child_id": 1, "rol_id": 2},
    {"user_id": 2, "child_id": 2, "rol_id": 1},
    {"user_id": 2, "child_id": 2, "rol_id": 2}
]

roles = [
    Role(id=1, type_rol='Admin'),
    Role(id=2, type_rol='Tutor Mare Pare'),
    Role(id=3, type_rol='Cuidador'),
    Role(id=4, type_rol='Seguiment')
]

statuses = [
    Status(id=1, name="sleep"),
    Status(id=2, name="awake"),
    Status(id=3, name="yes_eyepatch"),
    Status(id=4, name="no_eyepatch")
]

treatments = [
    Treatment(id=1, name='Hour'),
    Treatment(id=2, name='percentage')
]

