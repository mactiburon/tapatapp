class RoleConstants {
  static const int admin = 1;
  static const int medico = 2;
  static const int tutor = 3;
  static const int cuidador = 4;

  static String getRoleName(int roleId) {
    switch (roleId) {
      case admin:
        return 'Administrador';
      case medico:
        return 'Médico';
      case tutor:
        return 'Tutor';
      case cuidador:
        return 'Cuidador';
      default:
        return 'Desconocido';
    }
  }
}
