import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:tapatapp/features/comments/bloc/comments_bloc.dart';

class AddCommentScreen extends StatefulWidget {
  final int childId;

  const AddCommentScreen({super.key, required this.childId});

  @override
  State<AddCommentScreen> createState() => _AddCommentScreenState();
}

class _AddCommentScreenState extends State<AddCommentScreen> {
  final _formKey = GlobalKey<FormState>();
  final _commentController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Agregar Comentario')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                controller: _commentController,
                maxLines: 5,
                decoration: const InputDecoration(
                  labelText: 'Comentario',
                  border: OutlineInputBorder(),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Ingrese un comentario';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: () {
                  if (_formKey.currentState!.validate()) {
                    context.read<CommentsBloc>().add(
                          AddComment(
                            childId: widget.childId,
                            text: _commentController.text,
                          ),
                        );
                    Navigator.pop(context);
                  }
                },
                child: const Text('Guardar Comentario'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
