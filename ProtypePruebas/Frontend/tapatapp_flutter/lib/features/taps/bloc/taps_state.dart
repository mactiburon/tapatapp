part of 'taps_bloc.dart';

abstract class TapsState extends Equatable {
  const TapsState();

  @override
  List<Object> get props => [];
}

class TapsInitial extends TapsState {}

class TapsLoading extends TapsState {}

class TapsLoaded extends TapsState {
  final List<Tap> taps;

  const TapsLoaded({required this.taps});

  @override
  List<Object> get props => [taps];
}

class TapsError extends TapsState {
  final String message;

  const TapsError({required this.message});

  @override
  List<Object> get props => [message];
}
