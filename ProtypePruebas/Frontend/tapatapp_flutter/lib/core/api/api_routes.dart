import 'package:flutter/material.dart';

class LoginScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Login'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextField(
              decoration: InputDecoration(
                labelText: 'Email',
                border: OutlineInputBorder(),
              ),
            ),
            SizedBox(height: 16.0),
            TextField(
              decoration: InputDecoration(
                labelText: 'Password',
                border: OutlineInputBorder(),
              ),
              obscureText: true,
            ),
            SizedBox(height: 16.0),
            ElevatedButton(
              onPressed: () {
                // Handle login logic
              },
              child: Text('Login'),
            ),
          ],
        ),
      ),
    );
  }
}

class ApiRoutes {
  static const String baseUrl = 'http://tu-backend.com/api';

  // Autenticación
  static const String login = '/login';
  static const String refresh = '/refresh';
  static const String recoverPassword = '/recuperar-contrasena';

  // Usuarios
  static const String users = '/users';
  static String userById(int id) => '/users/$id';
  static const String cuidadores = '/medico/cuidadores';
  static const String tutores = '/admin/tutores';
  static const String adminUsers = '/admin/usuarios';
  static String adminUserById(int id) => '/admin/usuarios/$id';

  // Niños
  static const String children = '/children';
  static String childById(int id) => '/child/$id';
  static String childByName(String name) => '/children/$name';
  static String childrenByTutor(int tutorId) => '/tutor/$tutorId/children';
  static String childrenByCuidador(int cuidadorId) => '/cuidador/$cuidadorId/children';

  // Taps
  static const String taps = '/taps';
  static String tapById(int id) => '/taps/$id';
  static const String tutorTaps = '/tutores/taps';
  static const String medicoTaps = '/medicos/taps';

  // Comentarios
  static const String comments = '/comentarios';
  static String commentsByChild(int childId) => '/comentarios/$childId';
  static String commentById(int id) => '/comentarios/$id';

  // Historial
  static const String historial = '/historial';
  static String historialByChild(int childId) => '/historial/$childId';
  static String historialByChildAndDate(int childId, String date) => '/historial/$childId/$date';
  static const String tutorHistorial = '/tutores/historial';
  static const String medicoHistorial = '/medicos/historial';

  // Metadata
  static const String roles = '/roles';
  static const String statuses = '/statuses';
  static const String treatments = '/treatments';

  // Búsqueda
  static const String search = '/search';
}