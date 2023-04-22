from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from .models import Vinho
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        nome = request.form.get('nome')#Gets the note from the HTML 
        safra = request.form.get('safra')

        if len(nome) < 1:
            flash('Nome inválido!', category='error') 
        else:
            novo_vinho = Vinho(nome=nome, safra=safra, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(novo_vinho) #adding the note to the database 
            db.session.commit()
            flash('Vinho Adiconado!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-vinho', methods=['POST'])
def delete_vinho():  
    vinho = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    vinhoId = vinho['vinhoId']
    vinho = Vinho.query.get(vinhoId)
    if vinho:
        if vinho.user_id == current_user.id:
            db.session.delete(vinho)
            db.session.commit()

    return jsonify({})
