import 'package:json_annotation/json_annotation.dart';

part 'historial.g.dart';

@JsonSerializable()
class Historial {
  final int id;
  @JsonKey(name: 'child_id')
  final int childId;
  final String data; // Fecha en formato YYYY-MM-DD
  final String hora; // Hora en formato HH:MM
  final String estat; // Estado del sueño
  @JsonKey(name: 'totalHores')
  final double totalHoras;

  Historial({
    required this.id,
    required this.childId,
    required this.data,
    required this.hora,
    required this.estat,
    required this.totalHoras,
  });

  factory Historial.fromJson(Map<String, dynamic> json) => _$HistorialFromJson(json);
  Map<String, dynamic> toJson() => _$HistorialToJson(this);
}
