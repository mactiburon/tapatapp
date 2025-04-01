part of 'history_bloc.dart';

abstract class HistoryEvent extends Equatable {
  const HistoryEvent();

  @override
  List<Object> get props => [];
}

class LoadHistory extends HistoryEvent {
  final int childId;

  const LoadHistory({required this.childId});

  @override
  List<Object> get props => [childId];
}

class AddHistory extends HistoryEvent {
  final Historial historial;

  const AddHistory({required this.historial});

  @override
  List<Object> get props => [historial];
}

class DeleteHistory extends HistoryEvent {
  final int historyId;
  final int childId;

  const DeleteHistory({required this.historyId, required this.childId});

  @override
  List<Object> get props => [historyId, childId];
}
