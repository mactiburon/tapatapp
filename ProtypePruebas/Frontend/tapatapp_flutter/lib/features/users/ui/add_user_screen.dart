import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:tapatapp/core/models/user.dart';
import 'package:tapatapp/core/widgets/custom_text_field.dart';
import 'package:tapatapp/features/users/bloc/users_bloc.dart';

class AddUserScreen extends StatefulWidget {
  const AddUserScreen({super.key});

  @override
  State<AddUserScreen> createState() => _AddUserScreenState();
}

class _AddUserScreenState extends State<AddUserScreen> {
  final _formKey = GlobalKey<FormState>();
  final _usernameController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  int _selectedRole = RoleConstants.tutor;
  bool _isCuidador = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Agregar Usuario')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: ListView(
            children: [
              CustomTextField(
                controller: _usernameController,
                label: 'Nombre de usuario',
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Ingrese un nombre de usuario';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),
              CustomTextField(
                controller: _emailController,
                label: 'Email',
                keyboardType: TextInputType.emailAddress,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Ingrese un email';
                  }
                  if (!value.contains('@')) {
                    return 'Ingrese un email válido';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),
              CustomTextField(
                controller: _passwordController,
                label: 'Contraseña',
                obscureText: true,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Ingrese una contraseña';
                  }
                  if (value.length < 6) {
                    return 'Mínimo 6 caracteres';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),
              CheckboxListTile(
                title: const Text('Es Cuidador'),
                value: _isCuidador,
                onChanged: (value) {
                  setState(() {
                    _isCuidador = value ?? false;
                    if (_isCuidador) {
                      _selectedRole = RoleConstants.cuidador;
                    }
                  });
                },
              ),
              if (!_isCuidador) ...[
                const SizedBox(height: 8),
                DropdownButtonFormField<int>(
                  value: _selectedRole,
                  items: const [
                    DropdownMenuItem(
                      value: RoleConstants.admin,
                      child: Text('Administrador'),
                    ),
                    DropdownMenuItem(
                      value: RoleConstants.medico,
                      child: Text('Médico'),
                    ),
                    DropdownMenuItem(
                      value: RoleConstants.tutor,
                      child: Text('Tutor'),
                    ),
                  ],
                  onChanged: (value) {
                    setState(() {
                      _selectedRole = value ?? RoleConstants.tutor;
                    });
                  },
                  decoration: const InputDecoration(
                    labelText: 'Rol',
                    border: OutlineInputBorder(),
                  ),
                ),
              ],
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: () {
                  if (_formKey.currentState!.validate()) {
                    final newUser = User(
                      id: 0,
                      username: _usernameController.text,
                      email: _emailController.text,
                      roleId: _selectedRole,
                      password: _passwordController.text,
                    );

                    context.read<UsersBloc>().add(
                          AddUser(
                            user: newUser,
                            isCuidador: _isCuidador,
                          ),
                        );
                    Navigator.pop(context);
                  }
                },
                child: const Text('Guardar Usuario'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
