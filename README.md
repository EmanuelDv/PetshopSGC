# PetShop SGC - Sistema de Gestión de Citas

Este proyecto es un sistema de gestión de citas para una petshop. Permite registrar citas de baño y otros servicios para mascotas, así como gestionar la información de los dueños y las mascotas. Además, envía notificaciones por correo a los dueños después de un mes sin visitas.

## Características

- **Registro de dueños y mascotas**: Los dueños pueden registrar sus datos y asociar sus mascotas al sistema.
- **Agenda de citas**: Permite agendar citas para servicios de baño, peluquería, y más.
- **Base de datos**: Se utiliza SQLite para almacenar la información de las citas, los dueños y las mascotas.
- **Interfaz de usuario**: La aplicación utiliza Flask para manejar la parte backend del sistema, y la base de datos está integrada directamente.

## Tecnologías Usadas

- **Backend**: Python (Flask)
- **Base de datos**: SQLite (gestionada por Flask)
- **Frontend**: HTML, CSS (para las interfaces de usuario)

## Instalación

### Requisitos

- Python 3.7+
- Flask
- SQLite (incluido por defecto en Python)

### Pasos para la instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/EmanuelDv/PetshopSGC.git
