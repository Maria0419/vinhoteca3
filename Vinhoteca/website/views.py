from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Vinhos
from .models import Inventario
from .models import Vinicola
from . import db
import json

class Views:
    views = Blueprint('views', __name__)

    @views.route('/', methods=['GET', 'POST'])
    @login_required
    def home():
        vinhos = Vinhos.query.all()
        return render_template("home.html", user=current_user)

    def validate_wine(nome, safra, uva, tempodeguarda, harmonizacao):
        if len(nome) < 1: # create a validate input function
            flash('Nome inválido!', category='error')
            return 0
        
        elif len(safra) < 4:
            flash('Safra inválida!', category='error')
            return 0
        
        elif len(uva) < 1:
            flash('Uva inválida!', category='error')
            return 0
        
        elif len(tempodeguarda) < 1:
            flash('Tempo de guarda inválido!', category='error')
            return 0
        
        elif len(harmonizacao) < 1:
            flash('Harmonização inválida!', category='error')
            return 0
        
        return 1
    
    def register_wine(nome, safra, uva, tempodeguarda, harmonizacao):
        novo_vinho = Vinhos(nome=nome, safra=safra, uva=uva, tempodeguarda = tempodeguarda, harmonizacao=harmonizacao)  #providing the schema for the note 
        db.session.add(novo_vinho) #adding the note to the database 
        db.session.commit()
        flash('Vinho Adicionado!', category='success')

    @views.route('/cadastro', methods=['GET', 'POST'])
    @login_required
    def register():
        if request.method == 'POST': 
            
            if 'add' in request.form:
                return redirect(url_for('views.home'))
            
            if 'register' in request.form:
                nome = request.form.get('nome')#Gets the note from the HTML 
                safra = request.form.get('safra')
                uva = request.form.get('uva')
                tempodeguarda = request.form.get('tempodeguarda')
                harmonizacao = request.form.get('harmonizacao')                        
                
                if Views.validate_wine(nome,safra,uva,tempodeguarda,harmonizacao):
                    Views.register_wine(nome,safra,uva,tempodeguarda,harmonizacao)

        vinhos = Vinhos.query.all()
        return render_template("wine_register.html", vinhos=vinhos, user=current_user)
    
    
    @views.route('/harmonizacao', methods=['GET', 'POST'])
    @login_required
    def pairing():
            if request.method == 'POST': 

                if 'harmonize' in request.form:
                    harmonizacao = request.form.get('harmonizacao')
                    vinhos = Vinhos.query.filter_by(harmonizacao=harmonizacao)
                    return render_template("wine_pairing.html", vinhos=vinhos, user=current_user)
            
            return render_template("wine_pairing.html", vinhos=None, user=current_user)

    @views.route('/delete-vinho', methods=['POST'])
    def delete_vinho():  
        vinho = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
        vinhoId = vinho['vinhoId']
        vinho = Vinhos.query.get(vinhoId)
        if vinho:
            if vinho.user_id == current_user.id:
                db.session.delete(vinho)
                db.session.commit()

        return jsonify({})

    @views.route('/adicionar', methods=['GET', 'POST'])
    @login_required
    def add_wine():
        return render_template("add_wine.html", user=current_user)
