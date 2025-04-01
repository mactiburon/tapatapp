import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:tapatapp/core/models/comment.dart';
import 'package:tapatapp/core/widgets/role_based_widget.dart';
import 'package:tapatapp/features/comments/bloc/comments_bloc.dart';
import 'package:tapatapp/features/comments/screens/add_comment_screen.dart';

class CommentsListScreen extends StatelessWidget {
  final int childId;

  const CommentsListScreen({super.key, required this.childId});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Comentarios')),
      floatingActionButton: FloatingActionButton(
        onPressed: () => Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => AddCommentScreen(childId: childId),
          ),
        ),
        child: const Icon(Icons.add),
      ),
      body: BlocBuilder<CommentsBloc, CommentsState>(
        builder: (context, state) {
          if (state is CommentsLoading) {
            return const Center(child: CircularProgressIndicator());
          } else if (state is CommentsLoaded) {
            return ListView.builder(
              padding: const EdgeInsets.all(8.0),
              itemCount: state.comments.length,
              itemBuilder: (context, index) {
                final comment = state.comments[index];
                return Card(
                  child: ListTile(
                    title: Text(comment.text),
                    subtitle: Text(comment.timestamp),
                    trailing: RoleBasedWidget(
                      allowedRoles: const [RoleConstants.admin, RoleConstants.medico],
                      child: IconButton(
                        icon: const Icon(Icons.delete),
                        onPressed: () {
                          context.read<CommentsBloc>().add(
                                DeleteComment(
                                  commentId: comment.id,
                                  childId: childId,
                                ),
                              );
                        },
                      ),
                    ),
                  ),
                );
              },
            );
          } else if (state is CommentsError) {
            return Center(child: Text(state.message));
          }
          return const Center(child: Text('No hay comentarios'));
        },
      ),
    );
  }
}
