part of 'users_bloc.dart';

abstract class UsersEvent extends Equatable {
  const UsersEvent();

  @override
  List<Object> get props => [];
}

class LoadUsers extends UsersEvent {}

class LoadCuidadores extends UsersEvent {}

class LoadTutores extends UsersEvent {}

class AddUser extends UsersEvent {
  final User user;
  final bool isCuidador;

  const AddUser({required this.user, this.isCuidador = false});

  @override
  List<Object> get props => [user, isCuidador];
}

class UpdateUser extends UsersEvent {
  final User user;

  const UpdateUser({required this.user});

  @override
  List<Object> get props => [user];
}

class DeleteUser extends UsersEvent {
  final int userId;

  const DeleteUser({required this.userId});

  @override
  List<Object> get props => [userId];
}
