import 'package:flutter/material.dart';

class SleepManagementApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'TapatApp - Gestión de Sueño Infantil',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: LoginScreen(),
    );
  }
}

class LoginScreen extends StatelessWidget {
  final TextEditingController emailController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();

  void login(BuildContext context) {
    final email = emailController.text;
    final password = passwordController.text;

    if (email.isEmpty || password.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Por favor ingrese email y contraseña')),
      );
      return;
    }

    // Simulate login logic
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => MainMenuScreen()),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Iniciar Sesión'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: emailController,
              decoration: InputDecoration(labelText: 'Email'),
            ),
            TextField(
              controller: passwordController,
              decoration: InputDecoration(labelText: 'Contraseña'),
              obscureText: true,
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () => login(context),
              child: Text('Iniciar Sesión'),
            ),
          ],
        ),
      ),
    );
  }
}

class MainMenuScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Menú Principal'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: () {
                // Navigate to child management
              },
              child: Text('Gestión de Niños'),
            ),
            ElevatedButton(
              onPressed: () {
                // Navigate to user management
              },
              child: Text('Gestión de Usuarios'),
            ),
            ElevatedButton(
              onPressed: () {
                // Navigate to sleep history
              },
              child: Text('Registrar Historial'),
            ),
            ElevatedButton(
              onPressed: () {
                // Navigate to settings
              },
              child: Text('Configuración'),
            ),
          ],
        ),
      ),
    );
  }
}

void main() {
  runApp(SleepManagementApp());
}