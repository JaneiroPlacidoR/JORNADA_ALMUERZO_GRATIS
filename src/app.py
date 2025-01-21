from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import config
from validations import (
    validate_id, validate_nombre, validate_apellidos, validate_telefono, 
    validate_correo, validate_edad, validate_direccion, validate_entrega, 
    validate_observacion
)

def create_app():
    app = Flask(__name__)
    app.config.from_object(config['development'])
    return app

app = create_app()
mysql = MySQL(app)

def fetch_one(query, params=None):
    cursor = mysql.connection.cursor()
    cursor.execute(query, params or ())
    return cursor.fetchone()

def fetch_all(query, params=None):
    cursor = mysql.connection.cursor()
    cursor.execute(query, params or ())
    return cursor.fetchall()

def execute_query(query, params=None, commit=False):
    cursor = mysql.connection.cursor()
    cursor.execute(query, params or ())
    if commit:
        mysql.connection.commit()

def format_residente(row):
    if row:
        return {
            'id': row[0], 'nombre': row[1], 'apellidos': row[2], 'telefono': row[3],
            'correo': row[4], 'edad': row[5], 'direccion': row[6],
            'comida_entregada': row[7], 'observacion': row[8]
        }
    return None

def validate_request_data():
    validators = {
        'id': validate_id, 'nombre': validate_nombre, 'apellidos': validate_apellidos,
        'telefono': validate_telefono, 'correo': validate_correo, 'edad': validate_edad,
        'direccion': validate_direccion, 'comida_entregada': validate_entrega,
        'observacion': validate_observacion
    }
    errors = {field: validator(request.json[field]) for field, validator in validators.items() if validator(request.json[field])}
    return errors

@app.route('/residentes/<int:offset>', methods=['GET'])
def obtener_residentes(offset):
    try:
        query = """SELECT id, nombre, apellidos, telefono, correo, edad, direccion, 
                   comida_entregada, observacion, fecha FROM residente 
                   ORDER BY fecha DESC LIMIT %s, 10"""
        rows = fetch_all(query, (offset,))
        residentes = [format_residente(row) for row in rows]
        return jsonify({'residentes': residentes, 'mensaje': 'Residentes listados'})
    except Exception:
        return jsonify({'mensaje': 'Error al conectar con la base de datos', 'exito': False})

@app.route('/residente/<int:id>', methods=['GET'])
def obtener_residente(id):
    try:
        query = "SELECT * FROM residente WHERE id = %s"
        row = fetch_one(query, (id,))
        residente = format_residente(row)
        if residente:
            return jsonify({'residente': residente, 'mensaje': 'Residente encontrado.', 'exito': True})
        return jsonify({'mensaje': 'Residente no encontrado.', 'exito': False})
    except Exception:
        return jsonify({'mensaje': 'Error al conectar con la base de datos', 'exito': False})

@app.route('/residentes', methods=['POST'])
def registrar_residentes():
    errors = validate_request_data()
    if errors:
        return jsonify({'error_messages': errors})

    try:
        query = "SELECT id FROM residente WHERE id = %s"
        if fetch_one(query, (request.json['id'],)):
            return jsonify({'mensaje': 'ID ya existe, no se puede duplicar.', 'exito': False})

        is_comida_entregada = 1 if request.json['comida_entregada'] else 0
        query = """INSERT INTO residente (id, nombre, apellidos, telefono, correo, edad, 
                  direccion, comida_entregada, observacion, fecha) 
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())"""
        params = (
            request.json['id'], request.json['nombre'], request.json['apellidos'],
            request.json['telefono'], request.json['correo'], request.json['edad'],
            request.json['direccion'], is_comida_entregada, request.json['observacion']
        )
        execute_query(query, params, commit=True)
        return jsonify({'mensaje': 'Residente registrado.', 'exito': True})
    except Exception:
        return jsonify({'mensaje': 'Error al conectar con la base de datos', 'exito': False})

@app.route('/residentes/<int:id>', methods=['PUT'])
def actualizar_residentes(id):
    errors = validate_request_data()
    if errors:
        return jsonify({'error_messages': errors})

    try:
        query = "SELECT id FROM residente WHERE id = %s"
        if not fetch_one(query, (id,)):
            return jsonify({'mensaje': 'Residente no encontrado.', 'exito': False})

        is_comida_entregada = 1 if request.json['comida_entregada'] else 0
        query = """UPDATE residente SET nombre = %s, apellidos = %s, telefono = %s, 
                  correo = %s, edad = %s, direccion = %s, comida_entregada = %s, 
                  observacion = %s WHERE id = %s"""
        params = (
            request.json['nombre'], request.json['apellidos'], request.json['telefono'],
            request.json['correo'], request.json['edad'], request.json['direccion'],
            is_comida_entregada, request.json['observacion'], id
        )
        execute_query(query, params, commit=True)
        return jsonify({'mensaje': 'Residente actualizado.', 'exito': True})
    except Exception:
        return jsonify({'mensaje': 'Error al conectar con la base de datos', 'exito': False})

@app.route('/residentes/<int:id>', methods=['DELETE'])
def borrar_residentes(id):
    try:
        query = "DELETE FROM residente WHERE id = %s"
        execute_query(query, (id,), commit=True)
        return jsonify({'mensaje': 'Residente borrado.', 'exito': True})
    except Exception:
        return jsonify({'mensaje': 'Error al conectar con la base de datos', 'exito': False})

@app.route('/residentes/search/<string:word>', methods=['GET'])
def search_by_correo_or_name(word):
    try:
        query = """SELECT * FROM residente WHERE nombre LIKE %s OR correo LIKE %s"""
        rows = fetch_all(query, (f"%{word}%", f"%{word}%"))
        residentes = [format_residente(row) for row in rows]
        return jsonify({'mensaje': 'Resultados de búsqueda', 'residentes': residentes})
    except Exception:
        return jsonify({'mensaje': 'Error al conectar con la base de datos', 'exito': False})

@app.route('/residentes/byalphabet', methods=['GET'])
def obtener_residentes_alph():
    return obtener_residentes_ordered_by('nombre ASC')

@app.route('/residentes/byage', methods=['GET'])
def obtener_residentes_age():
    return obtener_residentes_ordered_by('edad DESC')

def obtener_residentes_ordered_by(order_by):
    try:
        query = f"SELECT * FROM residente ORDER BY {order_by}"
        rows = fetch_all(query)
        residentes = [format_residente(row) for row in rows]
        return jsonify({'residentes': residentes, 'mensaje': 'Residentes listados'})
    except Exception:
        return jsonify({'mensaje': 'Error al conectar con la base de datos', 'exito': False})

def pagina_no_encontrada(error):
    return jsonify({'mensaje': 'Ruta errónea'})

if __name__ == '__main__':
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()
