from getpass import getpass
from pymysql.err import MySQLError
from conexion import ConexionDB

def probar_consultas(conexion):
    """Ejemplo de lectura (SELECT) de datos."""
    print("\n--- Ejecutando SELECT ---")
    try:
        with conexion.cursor() as cursor:
            sql = "SELECT id_usuario, username, estado, id_rol FROM usuario LIMIT 5;"
            cursor.execute(sql)
            
            resultados = cursor.fetchall()
            
            if not resultados:
                print("No se encontraron registros.")
                return

            for fila in resultados:
                print(f"ID: {fila['id_usuario']} | Nombre: {fila['username']} | Estado: {fila['estado']} | Rol: {fila['id_rol']}")
                
    except MySQLError as e:
        print(f"Error al leer datos: {e}")


def probar_insert(conexion):
    """Ejemplo de escritura (INSERT) utilizando marcadores parametrizados (%s)."""
    print("\n--- Ejecutando INSERT ---")
    try:
        with conexion.cursor() as cursor:
            sql = "INSERT INTO usuario(id_usuario, username, password_hash, estado, intentos_fallidos, id_rol) VALUES (%s, %s, %s, %s, %s, %s);"
            datos_nuevos = ("USER-00", "Rodrigo_Cañas", "asoikdjalkdjjhaslkd", True, 0, "ROL-00")
            
            cursor.execute(sql, datos_nuevos)
        
            print(f"Registro insertado con éxito. ID generado: {cursor.lastrowid}")
            
    except MySQLError as e:
        print(f"Error al insertar datos: {e}")


def main():
    # Solicitamos la contraseña para inicializar tu clase
    password_eco_db = getpass("Contraseña de MySQL para EcoTech: ")
    db = ConexionDB(password=password_eco_db)
    
    # Intentamos conectar
    conexion = db.conectar()
    
    if conexion is None:
        print("No se puede continuar sin conexión activa.")
        return

    try:
        # --- AQUÍ EJECUTAS LAS PRUEBAS QUE QUIERAS ---
        probar_insert(conexion)
        probar_consultas(conexion)
        
    finally:
        # Garantizamos que la conexión se cierre pase lo que pase
        db.desconectar()


if __name__ == "__main__":
    main()