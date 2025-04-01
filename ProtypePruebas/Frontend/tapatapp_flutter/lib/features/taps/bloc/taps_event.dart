part of 'taps_bloc.dart';

abstract class TapsEvent extends Equatable {
  const TapsEvent();

  @override
  List<Object> get props => [];
}

class LoadTaps extends TapsEvent {
  final int childId;

  const LoadTaps({required this.childId});

  @override
  List<Object> get props => [childId];
}

class AddTap extends TapsEvent {
  final Tap tap;

  const AddTap({required this.tap});

  @override
  List<Object> get props => [tap];
}

class DeleteTap extends TapsEvent {
  final int tapId;
  final int childId;

  const DeleteTap({required this.tapId, required this.childId});

  @override
  List<Object> get props => [tapId, childId];
}
