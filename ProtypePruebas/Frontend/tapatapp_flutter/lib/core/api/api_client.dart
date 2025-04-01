import 'package:dio/dio.dart';
import 'package:tapatapp/core/api/api_routes.dart';
import 'package:tapatapp/core/errors/api_exceptions.dart';
import 'package:tapatapp/core/utils/storage_helper.dart';

class ApiClient {
  final Dio _dio;
  final StorageHelper _storageHelper;

  ApiClient({required StorageHelper storageHelper})
      : _dio = Dio(BaseOptions(
          baseUrl: ApiRoutes.baseUrl,
          connectTimeout: const Duration(seconds: 30),
          receiveTimeout: const Duration(seconds: 30),
          headers: {'Content-Type': 'application/json'},
        )),
        _storageHelper = storageHelper {
    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: _onRequest,
      onError: _onError,
    ));
  }

  Future<void> _onRequest(
      RequestOptions options, RequestInterceptorHandler handler) async {
    final token = await _storageHelper.getAccessToken();
    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }
    return handler.next(options);
  }

  Future<void> _onError(
      DioException error, ErrorInterceptorHandler handler) async {
    if (error.response?.statusCode == 401) {
      try {
        final newToken = await _refreshToken();
        if (newToken != null) {
          error.requestOptions.headers['Authorization'] = 'Bearer $newToken';
          return handler.resolve(await _dio.fetch(error.requestOptions));
        }
      } catch (e) {
        handler.reject(error);
      }
    }
    
    final exception = ApiException.fromDioError(error);
    return handler.reject(exception);
  }

  Future<String?> _refreshToken() async {
    try {
      final refreshToken = await _storageHelper.getRefreshToken();
      if (refreshToken == null) return null;

      final response = await _dio.post(
        ApiRoutes.refresh,
        options: Options(headers: {'Authorization': 'Bearer $refreshToken'}),
      );

      final newToken = response.data['access_token'];
      await _storageHelper.saveAccessToken(newToken);
      return newToken;
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    }
  }

  // Métodos HTTP
  Future<Response> get(String path, {Map<String, dynamic>? query}) async {
    try {
      return await _dio.get(path, queryParameters: query);
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    }
  }

  Future<Response> post(String path, {dynamic data}) async {
    try {
      return await _dio.post(path, data: data);
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    }
  }

  Future<Response> put(String path, {dynamic data}) async {
    try {
      return await _dio.put(path, data: data);
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    }
  }

  Future<Response> delete(String path) async {
    try {
      return await _dio.delete(path);
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    }
  }
}