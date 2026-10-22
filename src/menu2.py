"""Menú de consola de EcoTech (paso 1: consultas de solo lectura)."""

from pymysql.err import MySQLError

from src.database.conexion import ConexionDB
from src.servicios.validador_entradas import ValidadorEntradas


class MenuEcoTech:
    """Muestra un menú y ejecuta consultas sobre ecotech_db."""

    def __init__(self, db: ConexionDB):
        self.__db = db
        # Cada opción: número -> (texto del menú, método que se ejecuta).
        self.__opciones = {
            "1": ("Ver departamentos", self.__ver_departamentos),
            "2": ("Ver empleados", self.__ver_empleados),
            "3": ("Ver proyectos", self.__ver_proyectos),
            "4": ("Ver asignaciones activas", self.__ver_asignaciones),
            "5": ("Ver últimos registros de tiempo", self.__ver_registros),
            "6": ("Buscar empleado por nombre", self.__buscar_empleado),
            "0": ("Salir", None),
        }

    # ---------- Bucle principal ----------

    def ejecutar(self) -> None:
        while True:
            self.__mostrar_menu()
            opcion = input("Elige una opción: ").strip()

            if opcion == "0":
                print("Hasta luego.")
                break

            if opcion not in self.__opciones:
                print("Opción no válida. Intenta de nuevo.")
                continue

            self.__opciones[opcion][1]()
            input("\nPresiona Enter para volver al menú...")

    def __mostrar_menu(self) -> None:
        print("\n=== EcoTech ===")
        for numero, (texto, _) in self.__opciones.items():
            print(f"{numero}. {texto}")

    # ---------- Acceso a la base de datos ----------

    def __consultar(self, sql: str, parametros: tuple = ()) -> list:
        """Ejecuta un SELECT y devuelve una lista de diccionarios."""
        conexion = self.__db.conectar()
        if conexion is None:
            return []
        try:
            with conexion.cursor() as cursor:
                # Los valores del usuario van SIEMPRE en 'parametros',
                # nunca pegados dentro del texto SQL.
                cursor.execute(sql, parametros)
                return cursor.fetchall()
        except MySQLError:
            print("ERROR: no se pudo completar la consulta.")
            return []

    @staticmethod
    def __imprimir_tabla(filas: list) -> None:
        if not filas:
            print("\n(sin resultados)")
            return

        columnas = list(filas[0].keys())
        texto = lambda valor: "" if valor is None else str(valor)
        anchos = {
            c: max([len(c)] + [len(texto(f[c])) for f in filas])
            for c in columnas
        }

        print()
        print(" | ".join(c.ljust(anchos[c]) for c in columnas))
        print("-+-".join("-" * anchos[c] for c in columnas))
        for fila in filas:
            print(" | ".join(texto(fila[c]).ljust(anchos[c]) for c in columnas))

    # ---------- Opciones del menú ----------

    def __ver_departamentos(self) -> None:
        self.__imprimir_tabla(self.__consultar(
            """SELECT d.nombre AS departamento,
                      COALESCE(e.nombre, 'Sin gerente') AS gerente,
                      IF(d.activo, 'Activo', 'Inactivo') AS estado
               FROM departamento d
               LEFT JOIN empleado e ON e.id_empleado = d.id_gerente
               ORDER BY d.nombre"""))

    def __ver_empleados(self) -> None:
        # No mostramos salario: es un dato sensible.
        self.__imprimir_tabla(self.__consultar(
            """SELECT e.nombre, e.correo, d.nombre AS departamento,
                      e.fecha_contrato
               FROM empleado e
               JOIN departamento d ON d.id_departamento = e.id_departamento
               ORDER BY e.nombre"""))

    def __ver_proyectos(self) -> None:
        self.__imprimir_tabla(self.__consultar(
            """SELECT nombre, fecha_inicio,
                      IF(activo, 'Activo', 'Inactivo') AS estado
               FROM proyecto
               ORDER BY nombre"""))

    def __ver_asignaciones(self) -> None:
        self.__imprimir_tabla(self.__consultar(
            """SELECT e.nombre AS empleado, p.nombre AS proyecto,
                      a.rol_proyecto, a.fecha_asignacion
               FROM asignacion_proyecto a
               JOIN empleado e ON e.id_empleado = a.id_empleado
               JOIN proyecto p ON p.id_proyecto = a.id_proyecto
               WHERE a.activo = TRUE
               ORDER BY p.nombre, e.nombre"""))

    def __ver_registros(self) -> None:
        self.__imprimir_tabla(self.__consultar(
            """SELECT r.fecha, e.nombre AS empleado, p.nombre AS proyecto,
                      r.horas_trabajadas AS horas,
                      IF(r.aprobado, 'Sí', 'No') AS aprobado
               FROM registro_tiempo r
               JOIN empleado e ON e.id_empleado = r.id_empleado
               JOIN proyecto p ON p.id_proyecto = r.id_proyecto
               ORDER BY r.fecha DESC
               LIMIT 20"""))

    def __buscar_empleado(self) -> None:
        try:
            texto = ValidadorEntradas.sanitizar_entrada(
                input("Nombre a buscar: "))
        except ValueError as error:
            print(f"Entrada no válida: {error}")
            return

        if not texto:
            print("Debes escribir al menos una letra.")
            return

        self.__imprimir_tabla(self.__consultar(
            """SELECT e.nombre, e.correo, d.nombre AS departamento
               FROM empleado e
               JOIN departamento d ON d.id_departamento = e.id_departamento
               WHERE e.nombre LIKE %s
               ORDER BY e.nombre""",
            (f"%{texto}%",)))
