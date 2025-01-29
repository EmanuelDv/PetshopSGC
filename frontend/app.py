import sys
import sqlite3

import os


# Cambia la ruta de la base de datos
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'petshop.db')
print(DB_PATH)  # Verifica la ruta que se está utilizando

# Añadir la carpeta raíz del proyecto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

print(sys.path)  # Verifica las rutas


from flask import Flask, render_template, request
from src.models import (
    registrar_dueño,
    registrar_mascota,
    registrar_cita,
    obtener_todos_los_dueños,
    obtener_todas_las_mascotas,
    obtener_cita,
)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro_dueño', methods=['GET', 'POST'])
def registro_dueño():
    if request.method == 'POST':
        cedula = request.form['cedula']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        
        # Registrar el dueño
        dueño_registrado = registrar_dueño(cedula, nombre, apellido, correo, telefono, direccion)
        
        if dueño_registrado:
            return render_template('registro_dueño.html', mensaje="Registro exitoso", dueño_id=dueño_registrado)
        else:
            return render_template('registro_dueño.html', mensaje="Error: La cédula ya está registrada.")
    
    return render_template('registro_dueño.html')




@app.route('/registro_mascota', methods=['GET', 'POST'])
def registro_mascota():
    # Conexión a la base de datos para obtener los dueños registrados
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Obtener todos los dueños registrados
        cursor.execute('SELECT cedula, nombre, apellido FROM pets_parents')
        dueños = cursor.fetchall()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error al obtener los dueños: {e}")
        dueños = []

    if request.method == 'POST':
        nombre = request.form['nombre']
        especie = request.form['especie']
        raza = request.form['raza']
        edad = request.form['edad']
        peso = request.form['peso']
        dueño_id = request.form['dueño_id']  # Obtener el dueño seleccionado
        
        # Llamar a la función de registro de mascota
        id_pet = registrar_mascota(nombre, especie, raza, edad, peso, dueño_id)
        
        if id_pet:
            mensaje = f"Registro exitoso, ID de la mascota: {id_pet}"
            return render_template('registro_mascota.html', mensaje=mensaje, dueños=dueños)
        else:
            mensaje = "Error al registrar la mascota."
            return render_template('registro_mascota.html', mensaje=mensaje, dueños=dueños)
    
    return render_template('registro_mascota.html', dueños=dueños)




@app.route('/agendar_cita', methods=['GET', 'POST'])
def agendar_cita():
    # Obtener los dueños y mascotas
    dueños = obtener_todos_los_dueños()
    mascotas = obtener_todas_las_mascotas()

    if request.method == 'POST':
        fecha = request.form['fecha']
        hora = request.form['hora']
        cedula_dueño = request.form['cedula_dueño']
        mascota_id = request.form['mascota_id']
        servicio = request.form['servicio']

        # Llamar a la función para registrar la cita
        cita_id = registrar_cita(cedula_dueño, mascota_id, servicio, fecha, hora)

        if cita_id is None:
            error_message = "Ya existe una cita para esta fecha y hora. Por favor elija otro horario."
            return render_template('agendar_cita.html', error_message=error_message, dueños=dueños, mascotas=mascotas, cita_id=None, mostrar_modal=True)

        return render_template('agendar_cita.html', cita_id=cita_id, dueños=dueños, mascotas=mascotas, mostrar_modal=False)

    return render_template('agendar_cita.html', dueños=dueños, mascotas=mascotas, mostrar_modal=False)





@app.route('/consulta_cita', methods=['GET', 'POST'])
def consulta_cita():
    if request.method == 'POST':
        cita_id = request.form['cita_id']
        cita = obtener_cita(cita_id)
        if cita:
            # Aquí se asume que el apellido está en la columna 4 de la base de datos (ajusta el índice según tu base de datos)
            dueño = {'nombre': cita[1], 'apellido': cita[2], 'correo': cita[3], 'telefono': cita[4]}
            mascota = {'nombre': cita[5], 'especie': cita[6], 'raza': cita[7]}
            return render_template('consulta_cita.html', dueño=dueño, mascota=mascota, cita=cita)
        else:
            return render_template('consulta_cita.html', error_message="Cita no encontrada.")
    return render_template('consulta_cita.html')


if __name__ == '__main__':
    app.run(debug=True, port=3000)
