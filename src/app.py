from flask import Flask,jsonify,request
from flask_mysqldb import MySQL

from config import config
from validations import *

app = Flask(__name__)

conexion = MySQL(app)

#Funcion para validar existencia de residente en la base de datos
def existe_residente(id):
    try:
        cursor = conexion.connection.cursor()
        sql = f"SELECT id, nombre, apellidos, telefono, correo, edad, direccion, comida_entregada, observacion FROM residente WHERE id = {id}"
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            residente = {'id':datos[0],'nombre':datos[1],'apellidos':datos[2],'telefono':datos[3],'correo':datos[4],'edad':datos[5],'direccion':datos[6],'comida_entregada':datos[7],'observacion':datos[8]}
            return residente
        else:
            return None
    except Exception as e:
        raise e

#Funcion para mostrar si el 100% de los campos se introdujeron en el formato correcto
def validateAll() -> bool:
    try:
        return (validate_nombre(request.json['nombre']) == None and validate_apellidos(request.json['apellidos']) == None and
        validate_telefono(request.json['telefono']) == None and validate_correo(request.json['correo']) == None and validate_edad(request.json['edad']) == None and
        validate_direccion(request.json['direccion']) == None and validate_entrega(request.json['comida_entregada']) == None and validate_observacion(request.json['observacion']) == None)
    except Exception as e:
        return False

@app.route('/residentes/<actual>', methods=['GET'])
def obtener_residentes(actual):
    try:
        
        cursor = conexion.connection.cursor()
        sql = f"SELECT id, nombre, apellidos, telefono, correo, edad, direccion, comida_entregada, observacion, fecha FROM residente ORDER BY fecha DESC LIMIT {actual},10"
        cursor.execute(sql)
        datos = cursor.fetchall()
        residentes = []
        for fila in datos:
            residente = {'id':fila[0],'nombre':fila[1],'apellidos':fila[2],'telefono':fila[3],'correo':fila[4],'edad':fila[5],'direccion':fila[6],'comida_entregada':fila[7],'observacion':fila[8],'fecha':fila[9]}
            residentes.append(residente)
        return jsonify({'residentes':residentes,'mensaje':'Residentes listados'})

    except Exception as e:
            return jsonify({'mensaje': 'Error, es posible que no se haya conectado a la base de datos correctamnte', 'exito': False})

    
@app.route('/residente/<id>', methods=['GET'])
def obtener_residente(id):
    try:
        residente = existe_residente(id)
        if residente != None:
            return jsonify({'residente': residente, 'mensaje': "Residente encontrado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Residente no encontrado.", 'exito': False})
    except Exception as e:
            return jsonify({'mensaje': 'Error, es posible que no se haya conectado a la base de datos correctamnte', 'exito': False})
    

@app.route('/residentes', methods=['POST'])
def registrar_residentes():
    if (validateAll() and validate_id(request.json['id']) == None):
        try:  
            residente = existe_residente(request.json['id'])
            if residente != None:
                return jsonify({'mensaje': "ID ya existe, no se puede duplicar.", 'exito': False})
            else:
                is_comida_entregada = 0
                if request.json['comida_entregada'] == True:
                    is_comida_entregada = 1
                else:
                    is_comida_entregada = 0
                   
                cursor = conexion.connection.cursor()
                sql = """INSERT INTO residente (id, nombre, apellidos, telefono, correo,
                  edad, direccion, comida_entregada, observacion, fecha) 
                VALUES ('{0}','{1}','{2}',{3},'{4}',{5},'{6}','{7}','{8}', NOW())""".format(request.json['id'],request.json['nombre'],
                request.json['apellidos'],request.json['telefono'],request.json['correo'],request.json['edad'],
                request.json['direccion'],is_comida_entregada,request.json['observacion'])
                cursor.execute(sql)
                conexion.connection.commit()  
                return jsonify({'mensaje': "Residente registrado.", 'exito': True})
        except Exception as e:
            return jsonify({'mensaje': 'Error, es posible que no se haya conectado a la base de datos correctamnte', 'exito': False})
    else:
  
        v_id, v_nombre, v_apellidos, v_telefono, v_correo, v_edad, v_direccion, v_comida_entregada, v_observacion  = [["id",validate_id(request.json['id'])],["nombre",validate_nombre(request.json['nombre'])] , ["apellidos",validate_apellidos(request.json['apellidos'])] ,["telefono",validate_telefono(request.json['telefono'])] , ["correo",validate_correo(request.json['correo'])],["edad",validate_edad(request.json['edad'])] ,["direccion",validate_direccion(request.json['direccion'])],["comida_entregada",validate_entrega(request.json['comida_entregada'])] , ["observacion",validate_observacion(request.json['observacion'])]]
        errors = [v_id, v_nombre, v_apellidos, v_telefono, v_correo, v_edad, v_direccion, v_comida_entregada, v_observacion]
        messages =[]
        for item in errors:
            if item is not None:
             message = {f'{item[0]}':item[1]}
             messages.append(message)
        return jsonify({'errors messages':messages})

        

@app.route('/residentes/<id>', methods=['PUT'])
def actualizar_residentes(id):

    if (validateAll()):
        try:  
            residente = existe_residente(id)
            if residente != None:

                is_comida_entregada = 0
                if request.json['comida_entregada'] == True:
                    is_comida_entregada = 1
                else:
                    is_comida_entregada = 0

                cursor = conexion.connection.cursor()
                sql = f"""UPDATE residente SET id = '{id}', nombre = '{request.json['nombre']}',
                  apellidos = '{ request.json['apellidos']}', telefono = '{request.json['telefono']}',
                  correo = '{request.json['correo']}', edad = '{request.json['edad']}', direccion = '{request.json['direccion']}'
                  , comida_entregada = '{is_comida_entregada}', observacion = '{request.json['observacion']}'"""
                cursor.execute(sql)
                conexion.connection.commit()  
                return jsonify({'mensaje': "Residente actualizado.", 'exito': True})            
            else:
                return jsonify({'mensaje': "Residente no encontrado.", 'exito': False})
        except Exception as e:
            return jsonify({'mensaje': 'Error, es posible que no se haya conectado a la base de datos correctamnte', 'exito': False})
    else:

        v_nombre, v_apellidos, v_telefono, v_correo, v_edad, v_direccion, v_comida_entregada, v_observacion  = [["nombre",validate_nombre(request.json['nombre'])] , ["apellidos",validate_apellidos(request.json['apellidos'])] ,["telefono",validate_telefono(request.json['telefono'])] , ["correo",validate_correo(request.json['correo'])],["edad",validate_edad(request.json['edad'])] ,["direccion",validate_direccion(request.json['direccion'])],["comida_entregada",validate_entrega(request.json['comida_entregada'])] , ["observacion",validate_observacion(request.json['observacion'])]]
        errors = [v_id, v_nombre, v_apellidos, v_telefono, v_correo, v_edad, v_direccion, v_comida_entregada, v_observacion]
        messages =[]
        for item in errors:
            if item is not None:
             message = {f'{item[0]}':item[1]}
             messages.append(message)
        return jsonify({'errors messages':messages})

        
@app.route('/residentes/<id>', methods=['DELETE'])
def borrar_residentes(id):

        try:  
            residente = existe_residente(id)
            if residente != None:
                cursor = conexion.connection.cursor()
                sql = f"DELETE FROM residente WHERE id = '{id}'"
                cursor.execute(sql)
                conexion.connection.commit()  
                return jsonify({'mensaje': "Residente Borrado.", 'exito': True})            
            else:
                return jsonify({'mensaje': "Residente no encontrado.", 'exito': False})
        except Exception as e:
            return jsonify({'mensaje': 'Error, es posible que no se haya conectado a la base de datos correctamnte', 'exito': False})
        
@app.route('/residentes/search/<word>' , methods=['GET'])
def search_by_correo_or_name(word):
    try:
        cursor = conexion.connection.cursor()
        sql = f"SELECT id, nombre, apellidos, telefono, correo, edad, direccion, comida_entregada, observacion FROM residente WHERE nombre LIKE '%{word}%' OR correo LIKE '%{word}%'"
        cursor.execute(sql)
        datos = cursor.fetchall()
        residentes = []
        for fila in datos:
            residente = {'id':fila[0],'nombre':fila[1],'apellidos':fila[2],'telefono':fila[3],'correo':fila[4],'edad':fila[5],'direccion':fila[6],'comida_entregada':fila[7],'observacion':fila[8]}
            residentes.append(residente)
        return jsonify({'mensaje':'Residentes que coinciden con tu busqueda','residentes':residentes}) 
        
    except Exception as e:
        raise e

@app.route('/residentes/byalphabet', methods=['GET'])
def obtener_residentes_alph():
    try:
        cursor = conexion.connection.cursor()
        sql = f"SELECT id, nombre, apellidos, telefono, correo, edad, direccion, comida_entregada, observacion, fecha FROM residente ORDER BY nombre ASC"
        cursor.execute(sql)
        datos = cursor.fetchall()
        residentes = []
        for fila in datos:
            residente = {'id':fila[0],'nombre':fila[1],'apellidos':fila[2],'telefono':fila[3],'correo':fila[4],'edad':fila[5],'direccion':fila[6],'comida_entregada':fila[7],'observacion':fila[8],'fecha':fila[9]}
            residentes.append(residente)
        return jsonify({'residentes':residentes,'mensaje':'Residentes listados'})

    except Exception as e:
            return jsonify({'mensaje': 'Error, es posible que no se haya conectado a la base de datos correctamnte', 'exito': False})


@app.route('/residentes/byage', methods=['GET'])
def obtener_residentes_age():
    try:
        cursor = conexion.connection.cursor()
        sql = f"SELECT id, nombre, apellidos, telefono, correo, edad, direccion, comida_entregada, observacion, fecha FROM residente ORDER BY edad DESC"
        cursor.execute(sql)
        datos = cursor.fetchall()
        residentes = []
        for fila in datos:
            residente = {'id':fila[0],'nombre':fila[1],'apellidos':fila[2],'telefono':fila[3],'correo':fila[4],'edad':fila[5],'direccion':fila[6],'comida_entregada':fila[7],'observacion':fila[8],'fecha':fila[9]}
            residentes.append(residente)
        return jsonify({'residentes':residentes,'mensaje':'Residentes listados'})

    except Exception as e:
            return jsonify({'mensaje': 'Error, es posible que no se haya conectado a la base de datos correctamnte', 'exito': False})


def pagina_no_encontrada(error):
    return jsonify({'mensaje':'Ruta erronea'})


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()