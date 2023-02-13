import re

def validate_id(id: str) -> str:
    if not id.isnumeric():
        return "ID solo puede contener numeros"
    elif len(id) <= 0:
        return "ID requerido"
    elif len(id) != 5:
        return "ID no contiene los 5 digitos que debe tener"
    else:
        return None

def validate_nombre(nombre: str) -> str:
    if len(nombre) <= 0:
        return "Nombre requerido"
    elif len(nombre) > 30:
        return "Nombre solo puede contener 30 caracteres"
    elif not nombre.replace(" ", "").isalpha():
        return "Nombre solo puede contener letras"
    else:
        return None

def validate_apellidos(apellidos: str) -> str:
    if len(apellidos) <= 0:
        return "Apellidos requerido"
    elif len(apellidos) > 60:
        return "Apellidos solo puede contener 60 caracteres"
    elif not apellidos.replace(" ", "").isalpha():
        return "Apellidos solo puede contener letras"
    else:
        return None

def validate_telefono(telefono:int) -> str:
    if telefono > 999999999999999:
        return "Telefono invalido, maximo 15 digitos"
    else:
        return None

def validate_correo(correo:str) -> str:
    expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    if re.match(expresion_regular, correo) is not None:
        return None
    else:
        return "Correo invalido"


def validate_edad(edad:int) -> str:
    if edad <= 0:
        return "Edad requerida"
    elif edad>200:
        return "Edad invalida, edad maxima es de 200"
    else:
        return None

def validate_entrega(comida_entregada:bool) -> str:
    if comida_entregada is None:
        return "Comida_entregada requerida"
    else:
        return None


def validate_direccion(direccion:str) -> str:
    if len(direccion)>200:
        return "Direccion solo puede contener 200 caracteres"
    else: 
        return None

def validate_observacion(observacion:str) -> str:
    if len(observacion)>600:
        return "Observacion solo puede contener 600 caracteres"
    else: 
        return None


    

    

