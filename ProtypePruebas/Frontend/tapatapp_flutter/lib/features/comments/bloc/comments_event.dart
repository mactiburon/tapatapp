part of 'comments_bloc.dart';

abstract class CommentsEvent extends Equatable {
  const CommentsEvent();

  @override
  List<Object> get props => [];
}

class LoadComments extends CommentsEvent {
  final int childId;

  const LoadComments({required this.childId});

  @override
  List<Object> get props => [childId];
}

class AddComment extends CommentsEvent {
  final int childId;
  final String text;

  const AddComment({required this.childId, required this.text});

  @override
  List<Object> get props => [childId, text];
}

class DeleteComment extends CommentsEvent {
  final int commentId;
  final int childId;

  const DeleteComment({required this.commentId, required this.childId});

  @override
  List<Object> get props => [commentId, childId];
}
