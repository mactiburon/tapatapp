import 'package:json_annotation/json_annotation.dart';

part 'child.g.dart';

@JsonSerializable()
class Child {
  final int id;
  @JsonKey(name: 'child_name')
  final String childName;
  final int edad;
  @JsonKey(name: 'informacioMedica')
  final String informacionMedica;
  @JsonKey(name: 'tutor_id')
  final int? tutorId;
  @JsonKey(name: 'cuidador_id')
  final int? cuidadorId;
  @JsonKey(name: 'sleep_average')
  final double? sleepAverage;
  @JsonKey(name: 'treatment_id')
  final int? treatmentId;

  Child({
    required this.id,
    required this.childName,
    required this.edad,
    required this.informacionMedica,
    this.tutorId,
    this.cuidadorId,
    this.sleepAverage,
    this.treatmentId,
  });

  factory Child.fromJson(Map<String, dynamic> json) => _$ChildFromJson(json);
  Map<String, dynamic> toJson() => _$ChildToJson(this);
}