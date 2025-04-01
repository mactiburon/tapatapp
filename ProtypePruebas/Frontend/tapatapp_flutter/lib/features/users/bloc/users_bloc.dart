import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:tapatapp/core/api/api_client.dart';
import 'package:tapatapp/core/api/api_routes.dart';
import 'package:tapatapp/core/models/user.dart';

part 'users_event.dart';
part 'users_state.dart';

class UsersBloc extends Bloc<UsersEvent, UsersState> {
  final ApiClient apiClient;

  UsersBloc({required this.apiClient}) : super(UsersInitial()) {
    on<LoadUsers>(_onLoadUsers);
    on<LoadCuidadores>(_onLoadCuidadores);
    on<LoadTutores>(_onLoadTutores);
    on<AddUser>(_onAddUser);
    on<UpdateUser>(_onUpdateUser);
    on<DeleteUser>(_onDeleteUser);
  }

  FutureOr<void> _onLoadUsers(
    LoadUsers event,
    Emitter<UsersState> emit,
  ) async {
    emit(UsersLoading());
    try {
      final response = await apiClient.get(ApiRoutes.adminUsers);
      final users = (response.data as List)
          .map((json) => User.fromJson(json))
          .toList();
      emit(UsersLoaded(users: users));
    } catch (e) {
      emit(UsersError(message: e.toString()));
    }
  }

  FutureOr<void> _onLoadCuidadores(
    LoadCuidadores event,
    Emitter<UsersState> emit,
  ) async {
    emit(UsersLoading());
    try {
      final response = await apiClient.get(ApiRoutes.cuidadores);
      final users = (response.data as List)
          .map((json) => User.fromJson(json))
          .toList();
      emit(UsersLoaded(users: users));
    } catch (e) {
      emit(UsersError(message: e.toString()));
    }
  }

  FutureOr<void> _onLoadTutores(
    LoadTutores event,
    Emitter<UsersState> emit,
  ) async {
    emit(UsersLoading());
    try {
      final response = await apiClient.get(ApiRoutes.tutores);
      final users = (response.data as List)
          .map((json) => User.fromJson(json))
          .toList();
      emit(UsersLoaded(users: users));
    } catch (e) {
      emit(UsersError(message: e.toString()));
    }
  }

  FutureOr<void> _onAddUser(
    AddUser event,
    Emitter<UsersState> emit,
  ) async {
    try {
      await apiClient.post(
        event.isCuidador ? ApiRoutes.adminCuidadores : ApiRoutes.adminUsers,
        data: event.user.toJson(),
      );
      add(LoadUsers());
    } catch (e) {
      emit(UsersError(message: e.toString()));
    }
  }

  FutureOr<void> _onUpdateUser(
    UpdateUser event,
    Emitter<UsersState> emit,
  ) async {
    try {
      await apiClient.put(
        ApiRoutes.adminUserById(event.user.id),
        data: event.user.toJson(),
      );
      add(LoadUsers());
    } catch (e) {
      emit(UsersError(message: e.toString()));
    }
  }

  FutureOr<void> _onDeleteUser(
    DeleteUser event,
    Emitter<UsersState> emit,
  ) async {
    try {
      await apiClient.delete(
        ApiRoutes.adminUserById(event.userId),
      );
      add(LoadUsers());
    } catch (e) {
      emit(UsersError(message: e.toString()));
    }
  }
}
