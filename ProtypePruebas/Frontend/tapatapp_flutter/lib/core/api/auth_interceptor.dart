import 'package:dio/dio.dart';
import 'package:tapatapp/core/utils/storage_helper.dart';

class AuthInterceptor extends Interceptor {
  final StorageHelper storageHelper;

  AuthInterceptor(this.storageHelper);

  @override
  Future<void> onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) async {
    final token = await storageHelper.getAccessToken();
    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }
    return handler.next(options);
  }

  @override
  Future<void> onError(
    DioException err,
    ErrorInterceptorHandler handler,
  ) async {
    if (err.response?.statusCode == 401) {
      // Lógica para refresh token
    }
    return handler.next(err);
  }
}
