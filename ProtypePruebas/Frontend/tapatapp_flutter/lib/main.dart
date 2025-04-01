import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:tapatapp/core/api/api_client.dart';
import 'package:tapatapp/core/utils/storage_helper.dart';
import 'package:tapatapp/features/auth/bloc/auth_bloc.dart';
import 'package:tapatapp/features/children/bloc/children_bloc.dart';
import 'package:tapatapp/features/comments/bloc/comments_bloc.dart';
import 'package:tapatapp/features/history/bloc/history_bloc.dart';
import 'package:tapatapp/features/taps/bloc/taps_bloc.dart';
import 'package:tapatapp/features/users/bloc/users_bloc.dart';
import 'package:tapatapp/core/widgets/loading_indicator.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  final storageHelper = StorageHelper();
  await storageHelper.init();
  
  final apiClient = ApiClient(storageHelper: storageHelper);
  
  runApp(
    MultiRepositoryProvider(
      providers: [
        RepositoryProvider(create: (_) => apiClient),
        RepositoryProvider(create: (_) => storageHelper),
      ],
      child: MultiBlocProvider(
        providers: [
          BlocProvider(
            create: (context) => AuthBloc(
              apiClient: context.read<ApiClient>(),
              storageHelper: context.read<StorageHelper>(),
            )..add(CheckAuthStatus()),
          ),
          BlocProvider(
            create: (context) => ChildrenBloc(
              apiClient: context.read<ApiClient>(),
            ),
          ),
          BlocProvider(
            create: (context) => CommentsBloc(
              apiClient: context.read<ApiClient>(),
            ),
          ),
          BlocProvider(
            create: (context) => HistoryBloc(
              apiClient: context.read<ApiClient>(),
            ),
          ),
          BlocProvider(
            create: (context) => TapsBloc(
              apiClient: context.read<ApiClient>(),
            ),
          ),
          BlocProvider(
            create: (context) => UsersBloc(
              apiClient: context.read<ApiClient>(),
            ),
          ),
        ],
        child: const MyApp(),
      ),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'TapatApp',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: BlocBuilder<AuthBloc, AuthState>(
        builder: (context, state) {
          if (state is AuthLoading) {
            return const LoadingIndicator(message: 'Cargando...');
          } else if (state is AuthAuthenticated) {
            return MainMenuScreen(); // Replace with your main menu screen
          } else {
            return LoginScreen(); // Replace with your login screen
          }
        },
      ),
    );
  }
}