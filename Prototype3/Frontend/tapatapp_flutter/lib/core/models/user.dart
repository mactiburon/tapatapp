import 'package:json_annotation/json_annotation.dart';
import 'package:tapatapp/core/constants/role_constants.dart';

part 'user.g.dart';

@JsonSerializable()
class User {
  final int id;
  final String username;
  final String email;
  @JsonKey(name: 'role_id')
  final int roleId;
  final String? password;

  User({
    required this.id,
    required this.username,
    required this.email,
    required this.roleId,
    this.password,
  });

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
  Map<String, dynamic> toJson() => _$UserToJson(this);

  bool get isAdmin => roleId == RoleConstants.admin;
  bool get isMedico => roleId == RoleConstants.medico;
  bool get isTutor => roleId == RoleConstants.tutor;
  bool get isCuidador => roleId == RoleConstants.cuidador;

  String get roleName => RoleConstants.getRoleName(roleId);
}