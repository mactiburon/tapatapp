import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:tapatapp/core/models/user.dart';
import 'package:tapatapp/core/widgets/role_based_widget.dart';
import 'package:tapatapp/features/users/bloc/users_bloc.dart';
import 'package:tapatapp/features/users/screens/add_user_screen.dart';

class UsersListScreen extends StatelessWidget {
  const UsersListScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Gestión de Usuarios')),
      floatingActionButton: RoleBasedWidget(
        allowedRoles: const [RoleConstants.admin],
        child: FloatingActionButton(
          onPressed: () => Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => const AddUserScreen(),
            ),
          ),
          child: const Icon(Icons.add),
        ),
      ),
      body: BlocBuilder<UsersBloc, UsersState>(
        builder: (context, state) {
          if (state is UsersLoading) {
            return const Center(child: CircularProgressIndicator());
          } else if (state is UsersLoaded) {
            return ListView.builder(
              itemCount: state.users.length,
              itemBuilder: (context, index) {
                final user = state.users[index];
                return Card(
                  margin: const EdgeInsets.all(8.0),
                  child: ListTile(
                    title: Text(user.username),
                    subtitle: Text('${user.email} - ${user.roleName}'),
                    trailing: RoleBasedWidget(
                      allowedRoles: const [RoleConstants.admin],
                      child: IconButton(
                        icon: const Icon(Icons.delete),
                        onPressed: () {
                          context.read<UsersBloc>().add(
                                DeleteUser(userId: user.id),
                              );
                        },
                      ),
                    ),
                    onTap: () {
                      // Navegar a detalles/edición
                    },
                  ),
                );
              },
            );
          } else if (state is UsersError) {
            return Center(child: Text(state.message));
          }
          return const Center(child: Text('No hay usuarios registrados'));
        },
      ),
    );
  }
}
