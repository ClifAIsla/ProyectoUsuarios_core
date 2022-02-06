from flask import Flask, render_template, request, redirect, session, flash
from flask_app import app
from flask_app.modelos.usuario import Usuario
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

@app.route('/', methods=['GET'])
def index():
    return render_template ('index.html')

@app.route('/dashboard',methods=['GET'])
def dashboard():

    if 'user_id' not in session:
        return redirect('/')

    data = {
        "id" : session['user_id']
    }
    resultado = Usuario.dameUsuarioId( data )
    print("DALE UN CHEQUEADA A RESULTADOS", resultado)
    return render_template('dashboard.html', usuario=resultado)

@app.route('/registrarUsuario', methods=['POST'])
def registrarUsuario():
  
    datosUsuario = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : request.form['password'],
        "confirm_password" : request.form['confirm_password']
    }

    if not Usuario.validate_usuario( datosUsuario ):
        return redirect('/')
        
    #bcrypt PARA PASSWORD
    datosUsuario['password'] = bcrypt.generate_password_hash(request.form['password'])
    #bcrypt PARA CONFIRMAR PASSWORD
    datosUsuario['confirm_password'] = bcrypt.generate_password_hash(request.form['confirm_password'])

    id = Usuario.guardarUsuario( datosUsuario )
    session['user_id'] = id

    return redirect('/dashboard')

@app.route('/ingresarUsuario', methods=['POST'])
def ingresarUsuario():

    dastosSesion={
        "email" : request.form['emailLogin'],
        "password" : request.form['passwordLogin']
    }
    if not Usuario.validar_credenciales( dastosSesion ):
        return redirect('/')

    #print("Si se imprime esto significa que se va a iniciar sesion")

    usuario = Usuario.dameUsuarioCorreo( dastosSesion )
    if not bcrypt.check_password_hash(usuario.password, dastosSesion['password']):
        flash("La contraseña ingresada no es valida.","passwordLogin")
        return redirect('/')
    session['user_id'] = usuario.id
    return redirect('/dashboard')

@app.route('/logOut',methods=['GET'])
def salir():
    session.clear()
    return redirect('/')