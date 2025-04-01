import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:tapatapp/core/models/tap.dart';
import 'package:tapatapp/core/widgets/role_based_widget.dart';
import 'package:tapatapp/features/taps/bloc/taps_bloc.dart';

class TapsListScreen extends StatelessWidget {
  final int childId;

  const TapsListScreen({super.key, required this.childId});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Registro de Taps')),
      floatingActionButton: RoleBasedWidget(
        allowedRoles: const [RoleConstants.medico, RoleConstants.tutor],
        child: FloatingActionButton(
          onPressed: () => Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => AddTapScreen(childId: childId),
            ),
          ),
          child: const Icon(Icons.add),
        ),
      ),
      body: BlocBuilder<TapsBloc, TapsState>(
        builder: (context, state) {
          if (state is TapsLoading) {
            return const Center(child: CircularProgressIndicator());
          } else if (state is TapsLoaded) {
            return ListView.builder(
              itemCount: state.taps.length,
              itemBuilder: (context, index) {
                final tap = state.taps[index];
                return Card(
                  margin: const EdgeInsets.all(8.0),
                  child: ListTile(
                    title: Text('De ${tap.init} a ${tap.end}'),
                    subtitle: Text('Estado ID: ${tap.statusId}'),
                    trailing: RoleBasedWidget(
                      allowedRoles: const [RoleConstants.admin, RoleConstants.medico],
                      child: IconButton(
                        icon: const Icon(Icons.delete),
                        onPressed: () {
                          context.read<TapsBloc>().add(
                                DeleteTap(tapId: tap.id, childId: childId),
                              );
                        },
                      ),
                    ),
                  ),
                );
              },
            );
          } else if (state is TapsError) {
            return Center(child: Text(state.message));
          }
          return const Center(child: Text('No hay registros de taps'));
        },
      ),
    );
  }
}
