import 'dart:async';
import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:tapatapp/core/api/api_client.dart';
import 'package:tapatapp/core/api/api_routes.dart';
import 'package:tapatapp/core/models/comment.dart';

part 'comments_event.dart';
part 'comments_state.dart';

class CommentsBloc extends Bloc<CommentsEvent, CommentsState> {
  final ApiClient apiClient;

  CommentsBloc({required this.apiClient}) : super(CommentsInitial()) {
    on<LoadComments>(_onLoadComments);
    on<AddComment>(_onAddComment);
    on<DeleteComment>(_onDeleteComment);
  }

  FutureOr<void> _onLoadComments(
    LoadComments event,
    Emitter<CommentsState> emit,
  ) async {
    emit(CommentsLoading());
    try {
      final response = await apiClient.get(
        ApiRoutes.commentsByChild(event.childId),
      );
      final comments = (response.data as List)
          .map((json) => Comment.fromJson(json))
          .toList();
      emit(CommentsLoaded(comments: comments));
    } catch (e) {
      emit(CommentsError(message: e.toString()));
    }
  }

  FutureOr<void> _onAddComment(
    AddComment event,
    Emitter<CommentsState> emit,
  ) async {
    try {
      await apiClient.post(
        ApiRoutes.comments,
        data: {
          'child_id': event.childId,
          'text': event.text,
        },
      );
      add(LoadComments(childId: event.childId));
    } catch (e) {
      emit(CommentsError(message: e.toString()));
    }
  }

  FutureOr<void> _onDeleteComment(
    DeleteComment event,
    Emitter<CommentsState> emit,
  ) async {
    try {
      await apiClient.delete(
        ApiRoutes.commentById(event.commentId),
      );
      add(LoadComments(childId: event.childId));
    } catch (e) {
      emit(CommentsError(message: e.toString()));
    }
  }
}
