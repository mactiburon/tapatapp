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
    if (email == 'admin@example.com' && password == 'password') {
      Navigator.push(
        context,
        MaterialPageRoute(builder: (context) => MainMenuScreen()),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Credenciales inválidas')),
      );
    }
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
        child: Text('Bienvenido al Menú Principal'),
      ),
    );
  }
}

void main() {
  runApp(SleepManagementApp());
}

class AppConstants {
  static const String appName = 'TapatApp';
  static const String appVersion = '1.0.0';
  
  // Tiempos
  static const int splashDelay = 2; // segundos
  static const int apiTimeout = 30; // segundos
  
  // Estilos
  static const double defaultPadding = 16.0;
  static const double defaultBorderRadius = 12.0;
}