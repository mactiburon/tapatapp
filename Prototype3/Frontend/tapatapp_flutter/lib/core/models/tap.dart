import 'package:json_annotation/json_annotation.dart';

part 'tap.g.dart';

@JsonSerializable()
class Tap {
  final int id;
  @JsonKey(name: 'child_id')
  final int childId;
  @JsonKey(name: 'status_id')
  final int statusId;
  @JsonKey(name: 'user_id')
  final int userId;
  final String init; // Hora inicio
  final String end; // Hora fin

  Tap({
    required this.id,
    required this.childId,
    required this.statusId,
    required this.userId,
    required this.init,
    required this.end,
  });

  factory Tap.fromJson(Map<String, dynamic> json) => _$TapFromJson(json);
  Map<String, dynamic> toJson() => _$TapToJson(this);
}