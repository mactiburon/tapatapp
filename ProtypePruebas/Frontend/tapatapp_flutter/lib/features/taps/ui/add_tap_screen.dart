import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:tapatapp/core/models/tap.dart';
import 'package:tapatapp/features/taps/bloc/taps_bloc.dart';

class AddTapScreen extends StatefulWidget {
  final int childId;

  const AddTapScreen({super.key, required this.childId});

  @override
  State<AddTapScreen> createState() => _AddTapScreenState();
}

class _AddTapScreenState extends State<AddTapScreen> {
  final _formKey = GlobalKey<FormState>();
  final _initController = TextEditingController();
  final _endController = TextEditingController();
  int _selectedStatus = 1;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Agregar Tap')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: ListView(
            children: [
              TextFormField(
                controller: _initController,
                decoration: const InputDecoration(
                  labelText: 'Hora de inicio (HH:MM)',
                  border: OutlineInputBorder(),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Ingrese hora de inicio';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _endController,
                decoration: const InputDecoration(
                  labelText: 'Hora de fin (HH:MM)',
                  border: OutlineInputBorder(),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Ingrese hora de fin';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),
              DropdownButtonFormField<int>(
                value: _selectedStatus,
                items: const [
                  DropdownMenuItem(value: 1, child: Text('Dormido')),
                  DropdownMenuItem(value: 2, child: Text('Despierto')),
                  DropdownMenuItem(value: 3, child: Text('Inquieto')),
                ],
                onChanged: (value) {
                  setState(() {
                    _selectedStatus = value!;
                  });
                },
                decoration: const InputDecoration(
                  labelText: 'Estado',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: () {
                  if (_formKey.currentState!.validate()) {
                    final newTap = Tap(
                      id: 0,
                      childId: widget.childId,
                      statusId: _selectedStatus,
                      userId: 0, // Se completará con el usuario logueado
                      init: _initController.text,
                      end: _endController.text,
                    );

                    context.read<TapsBloc>().add(AddTap(tap: newTap));
                    Navigator.pop(context);
                  }
                },
                child: const Text('Guardar Tap'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
