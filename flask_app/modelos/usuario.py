from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app

from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

PASSWORD_REGEX = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')

class Usuario:
    def __init__(self,id,first_name,last_name,email,password,confirm_password):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.confirm_password = confirm_password
    
    @classmethod
    def guardarUsuario(cls,data):
        query = "INSERT INTO usuarios (first_name, last_name, email, password, confirm_password) VALUES	(%(first_name)s,%(last_name)s,%(email)s,%(password)s,%(confirm_password)s);"
        resultado = connectToMySQL('usuarios').query_db(query,data)
        #print("esto tiene resultado guardarUsuario",resultado)
        return resultado
    
    @classmethod
    def dameDatosDeUsuario(cls):
        query = "SELECT * FROM usuarios;"
        resultado = connectToMySQL('usuarios').query_db(query)
        listaUsuarioa = []      
        for usuario in resultado:
            listaUsuarioa.append( cls( usuario["id"],usuario["first_name"],usuario["last_name"],usuario["email"],usuario["password"],usuario["confirm_password"]))
        return listaUsuarioa
    
    @classmethod
    def dameUsuarioId(cls,data):
        query = "SELECT * FROM usuarios WHERE id=%(id)s;"
        resultado = connectToMySQL('usuarios').query_db(query,data)
        return cls(resultado[0]['id'],resultado[0]['first_name'],resultado[0]['last_name'],resultado[0]['email'],resultado[0]['password'],resultado[0]['confirm_password'])

    @classmethod
    def dameUsuarioCorreo(cls,data):
        query = "SELECT * FROM usuarios WHERE email=%(email)s;"
        resultado = connectToMySQL('usuarios').query_db(query,data)
        return cls(resultado[0]['id'],resultado[0]['first_name'],resultado[0]['last_name'],resultado[0]['email'],resultado[0]['password'],resultado[0]['confirm_password'])

    @staticmethod
    def validate_usuario(usuario):
        #ESTE QUERY ES PARA EL CORREO
        query = "SELECT * FROM usuarios WHERE email=%(email)s;"
        resultado = connectToMySQL('usuarios').query_db(query,usuario)
        #print("VEAMOS QUE ESTA DENTRO DE RESULTAD",resultado)

        is_valid = True # asumimos que esto es true

        #ESTE QUERY ES PARA EL password
        query2 = "SELECT * FROM usuarios WHERE password=%(password)s;"
        resultado2 = connectToMySQL('usuarios').query_db(query2,usuario)
        #print("VEAMOS QUE ESTA DENTRO DE RESULTAD2",resultado2)

        if len(usuario['first_name']) < 2:
            flash("Name must be at least 2 characters.","name")
            is_valid = False
        
        #if not usuario['first_name'].isalpha()


        if len(usuario['last_name']) < 2:
            flash("Last name must be at least 2 characters.","last_name")
            is_valid = False
            #print("que viene",resultado)
        #VALIDACION CORREO
        if len(resultado) > 0:
            flash("Email ya registrado.","correo_registrado")
            is_valid = False           
        if not EMAIL_REGEX.match(usuario['email']):
            flash("Ingrese un email valido.","correo_invalido")
            is_valid = False
        #VALIDACION PASSWORD
        if not PASSWORD_REGEX.match(usuario['password']):
            flash("Ingrese una contrasñe que tenga al menos 8 caracteres, al menos 1 letra y 1 numero.","password")
            is_valid = False
        #VALIDACION CONFIRMAR PASSWORD
        if usuario['confirm_password'] != usuario['password']:
            flash("La contraseña ingresada no coincide.","confirm_password")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validar_credenciales( usuario ):
        query = "SELECT * FROM usuarios WHERE email=%(email)s;"
        resultado = connectToMySQL('usuarios').query_db(query,usuario)
        #print("VALIDACION PARA INICIAR SESION", resultado)
        #print("IMPRIMEME SU CONTRASEÑA", resultado[0]['password'])

        is_valid = True # asumimos que esto es true

        if len(resultado) == 0:
            flash("El correo proporcionado no existe.","correoLogin")
            is_valid = False
        return is_valid

            



