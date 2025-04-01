part of 'auth_bloc.dart';

abstract class AuthEvent extends Equatable {
  const AuthEvent();

  @override
  List<Object> get props => [];
}

class LoginEvent extends AuthEvent {
  final String email;
  final String password;

  const LoginEvent({required this.email, required this.password});

  @override
  List<Object> get props => [email, password];
}

class LogoutEvent extends AuthEvent {}

class RecoverPasswordEvent extends AuthEvent {
  final String email;

  const RecoverPasswordEvent({required this.email});

  @override
  List<Object> get props => [email];
}

class CheckAuthStatus extends AuthEvent {}