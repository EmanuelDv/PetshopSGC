import sqlite3
import os

# Esto asegurará que la base de datos se busque fuera de 'frontend'
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'petshop.db')

def registrar_dueño(cedula, nombre, apellido, correo, telefono, direccion):
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Eliminar espacios en la cédula
        cedula = cedula.strip()

        # Verificar si la cédula ya está registrada
        cursor.execute('SELECT COUNT(*) FROM pets_parents WHERE cedula = ?', (cedula,))
        count = cursor.fetchone()[0]
        
        print(f"Consultando cédula: {cedula}, Count: {count}")  # Para depuración

        if count > 0:
            return None  # Retorna None si la cédula ya está registrada

        # Si no existe, insertar el nuevo dueño
        cursor.execute(
            'INSERT INTO pets_parents (cedula, nombre, apellido, correo, telefono, direccion) VALUES (?, ?, ?, ?, ?, ?)',
            (cedula, nombre, apellido, correo, telefono, direccion)
        )
        conn.commit()
        conn.close()
        return cedula  # Retornamos la cédula como identificador único
    except sqlite3.Error as e:
        print(f"Error en la base de datos: {e}")
        return None



def registrar_mascota(nombre, especie, raza, edad, peso, dueño_id):
    try:
        # Conexión a la base de datos
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Inserción de la nueva mascota con el dueño
        cursor.execute('''INSERT INTO Pet (nombre, especie, raza, edad, peso, dueño_id) 
                          VALUES (?, ?, ?, ?, ?, ?)''', 
                          (nombre, especie, raza, edad, peso, dueño_id))
        
        # Obtener el ID de la mascota recién insertada
        id_pet = cursor.lastrowid
        conn.commit()
        
        return id_pet  # Retorna el ID de la mascota recién registrada
    except sqlite3.Error as e:
        print(f"Error al registrar mascota: {e}")
        return None
    finally:
        conn.close()


def registrar_cita(cedula_dueño, mascota_id, servicio, fecha, hora):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Verificar si ya existe una cita en la misma fecha y hora
        cursor.execute(
            'SELECT COUNT(*) FROM Cita WHERE fecha = ? AND hora = ?',
            (fecha, hora)
        )
        if cursor.fetchone()[0] > 0:
            return None  # Retorna None si ya hay una cita en esa fecha y hora
        
        # Si no hay conflictos, insertamos la nueva cita
        cursor.execute(
            'INSERT INTO Cita (id_pets_parents, id_pet, servicio, fecha, hora) VALUES (?, ?, ?, ?, ?)',
            (cedula_dueño, mascota_id, servicio, fecha, hora)
        )
        conn.commit()
        cita_id = cursor.lastrowid
        conn.close()
        return cita_id  # Retorna el ID de la cita recién creada
    except sqlite3.Error as e:
        print(f"Error en la base de datos: {e}")
        return None



def obtener_todos_los_dueños():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT cedula, nombre, apellido FROM pets_parents')
    dueños = cursor.fetchall()
    conn.close()
    return dueños


def obtener_todas_las_mascotas():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT Id_pet, nombre FROM Pet')
    mascotas = cursor.fetchall()  # Devuelve una lista de tuplas (id_mascota, nombre_mascota)
    conn.close()
    return mascotas

def obtener_cita(cita_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''SELECT Cita.Id_Cita, 
                         pets_parents.nombre AS dueño_nombre, 
                         pets_parents.apellido AS dueño_apellido,  
                         pets_parents.correo AS dueño_correo, 
                         pets_parents.telefono AS dueño_telefono,
                         Pet.nombre AS mascota_nombre, 
                         Pet.especie, 
                         Pet.raza, 
                         Cita.Servicio, 
                         Cita.Fecha, 
                         Cita.Hora
                     FROM Cita
                     JOIN pets_parents ON Cita.Id_pets_parents = pets_parents.cedula
                     JOIN Pet ON Cita.Id_pet = Pet.id_pet
                     WHERE Cita.Id_Cita = ?''', (cita_id,))

    cita = cursor.fetchone()
    conn.close()

    return cita









