'''
Proyecto final del curso "Programador Python [ID: PP-18-20230511]"
Opción "Blog"

Autor: Julian Griffin

'''

import traceback
import requests
from flask import Flask, request, jsonify, render_template, Response, redirect, url_for

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"

# Asociación del controlador de la base de datos con la aplicacion
db = SQLAlchemy()
db.init_app(app)



class Posteos(db.Model):
    __tablename__ = "posteos"
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String)
    titulo = db.Column(db.String)
    texto = db.Column(db.String)

def postear(usuario, titulo, texto):
    
    post = Posteos(usuario=usuario, titulo=titulo, texto=texto)

    # Agregar el posteo a la DB
    db.session.add(post)
    db.session.commit()

#-------------------------#
#-------------------------#
#-------------------------#

@app.route("/")
def index():
    try:
        return render_template("blog.html")
    except:
        return jsonify({"trace": traceback.format_exc()})

#-------------------------#

@app.route("/login")
def login():
    try:
        return render_template("login.html")
    except:
        return jsonify({"trace": traceback.format_exc()})

#-------------------------#

@app.route("/posteos/<usuario>", methods=["GET", "POST", "DELETE"])
def posteos(usuario):
    if request.method == "GET":
        try:
            query = db.session.query(Posteos).filter(Posteos.usuario == usuario).order_by(Posteos.id.desc())
            resultado = query.limit(3)

            datos = []

            for obj in resultado:
                titulo_texto = {}
                titulo_texto["titulo"] = obj.titulo
                titulo_texto["texto"] = obj.texto
                datos.append(titulo_texto)

            return jsonify(datos)
            # return render_template('blog.html', usuario=usuario)

        except:
            return jsonify({"trace": traceback.format_exc()})
        
    if request.method == "POST":
        try:
            titulo = request.form.get("titulo")
            texto = request.form.get("texto")

            postear(usuario, titulo, texto)

            return Response(status=201)

        except:
            return jsonify({"trace": traceback.format_exc()})
        
    # if request.method == "DELETE":
    #     try:
    #         query = db.session.query(Posteos).filter(Posteos.usuario == usuario).get(all)

    #         if query is not None:
    #             for obj in query:
    #                 db.session.delete(obj)

    #             db.session.commit()

    #             mensaje = f"Todos los posteos de {usuario} fueron eliminados."
            
    #         else:
    #             mensaje = f"El usuario '{usuario}' no existe"
            
    #         return mensaje
        
    #     except:
    #         return jsonify({"trace": traceback.format_exc()})
        
#-------------------------#


@app.route("/borrar/<usuario>", methods=["DELETE"])
def borrar(usuario):        
    try:
        query = db.session.query(Posteos).filter(Posteos.usuario == usuario).get(all)

        if query is not None:
            for obj in query:
                db.session.delete(obj)

                db.session.commit()

                mensaje = f"Todos los posteos de {usuario} fueron eliminados."
            
        else:
            mensaje = f"El usuario '{usuario}' no existe"
            
        return mensaje
        
    except:
        return jsonify({"trace": traceback.format_exc()})
        

#-------------------------#

# Este método se ejecutará la primera vez
# cuando se construye la app.
with app.app_context():
    # Crear aquí la base de datos
    db.create_all()
    print("BASE DE DATOS GENERADA")



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)