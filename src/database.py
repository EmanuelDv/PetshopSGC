import sqlite3
import os

def crear_base_datos():
    # Conecta correctamente a la base de datos fuera de la carpeta frontend
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), '..', 'petshop.db'))
    cursor = conn.cursor()

    # Crear tablas...
    cursor.execute('''CREATE TABLE IF NOT EXISTS pets_parents (
        cedula TEXT PRIMARY KEY,
        nombre TEXT,
        apellido TEXT,
        correo TEXT,           
        telefono TEXT,
        direccion TEXT
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Pet (
        id_pet INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        especie TEXT,
        raza TEXT,
        edad INTEGER,
        peso REAL,
        dueño_id TEXT,
        FOREIGN KEY(dueño_id) REFERENCES pets_parents(cedula)
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Cita (
        Id_Cita INTEGER PRIMARY KEY AUTOINCREMENT,
        Id_pets_parents TEXT NOT NULL,
        Id_pet INTEGER NOT NULL,
        Servicio TEXT NOT NULL CHECK(Servicio IN (
            'Combo básico', 'Combo keratina', 'Combo gato', 
            'Mantenimiento básico', 'Combo alisado')),
        Fecha TEXT NOT NULL,
        Hora TEXT NOT NULL,
        FOREIGN KEY (Id_pets_parents) REFERENCES pets_parents (cedula),
        FOREIGN KEY (Id_pet) REFERENCES Pet (id_pet)
    )''')

    # cursor.execute('''CREATE TABLE IF NOT EXISTS Consultar_cita (
    #     Id_cita INTEGER PRIMARY KEY,
    #     Id_pets_parent TEXT,
    #     Id_pet INTEGER,
    #     servicio TEXT,
    #     Fecha TEXT,
    #     Hora TEXT,
    #     FOREIGN KEY(Id_pets_parent) REFERENCES pets_parents(cedula),
    #     FOREIGN KEY(Id_pet) REFERENCES Pet(id_pet)
    # )''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    crear_base_datos()
