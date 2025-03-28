import 'package:json_annotation/json_annotation.dart';

part 'comment.g.dart';

@JsonSerializable()
class Comment {
  final int id;
  @JsonKey(name: 'child_id')
  final int childId;
  @JsonKey(name: 'user_id')
  final int userId;
  final String text;
  final String timestamp;
  final bool important;

  Comment({
    required this.id,
    required this.childId,
    required this.userId,
    required this.text,
    required this.timestamp,
    this.important = false,
  });

  factory Comment.fromJson(Map<String, dynamic> json) => _$CommentFromJson(json);
  Map<String, dynamic> toJson() => _$CommentToJson(this);
}