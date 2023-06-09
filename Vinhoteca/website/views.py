from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Vinhos
from .models import Inventario
from .models import Vinicola
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from . import db
import json
import csv
from sqlalchemy import or_

class Views:
    views = Blueprint('views', __name__)

    @views.route('/', methods=['GET', 'POST'])
    @login_required
    def home():
        inventarios_usuario = Inventario.query.filter_by(user_id=current_user.id).all()

        vinhos_ids_distintos = set(inventario.vinho_id for inventario in inventarios_usuario)
        vinhos_inventario = Vinhos.query.filter(Vinhos.id.in_(vinhos_ids_distintos)).all()

        return render_template("home.html", vinhos=vinhos_inventario, inventario=inventarios_usuario, user=current_user)

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
    
    """"
    def register_wine(nome, safra, uva, tempodeguarda, harmonizacao):
        novo_vinho = Vinhos(nome=nome, safra=safra, uva=uva, tempodeguarda = tempodeguarda, harmonizacao=harmonizacao)  #providing the schema for the note 
        db.session.add(novo_vinho) #adding the note to the database 
        db.session.commit()
        flash('Vinho Adicionado!', category='success') """

    def register_wine(nome, safra, uva, tempodeguarda, harmonizacao, vinicola_nome, vinicola_regiao):
        vinicola = Vinicola.query.filter_by(nome=vinicola_nome).first()
        if vinicola:
            vinicola_id = vinicola.id
        else:
            nova_vinicola = Vinicola(nome=vinicola_nome, regiao=vinicola_regiao)
            db.session.add(nova_vinicola)
            db.session.commit()
            vinicola_id = nova_vinicola.id
    
        novo_vinho = Vinhos(nome=nome, safra=safra, uva=uva, tempodeguarda=tempodeguarda, harmonizacao=harmonizacao, vinicola_id=vinicola_id)
        db.session.add(novo_vinho)
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
                vinicola_nome = request.form.get('vinicola.nome')     
                vinicola_regiao = request.form.get('vinicola.regiao')                
                
                if Views.validate_wine(nome,safra,uva,tempodeguarda,harmonizacao):
                    Views.register_wine(nome,safra,uva,tempodeguarda,harmonizacao,vinicola_nome,vinicola_regiao)

            if 'procura' in request.form:
                nome = request.form.get('procura_vinho')
                vinhos = Vinhos.query.filter(Vinhos.nome.ilike(f'%{nome}%'))
                return render_template("wine_register.html", vinhos=vinhos, user=current_user)

        vinhos = Vinhos.query.all()
        return render_template("wine_register.html", vinhos=vinhos, user=current_user)

    @views.route('/harmonizacao', methods=['GET', 'POST'])
    @login_required
    def pairing():
        if request.method == 'POST': 
            if 'harmonize' in request.form:
                harmonizacao = request.form.get('harmonizacao')
                vinhos = Vinhos.query.filter(Vinhos.harmonizacao.ilike(f'%{harmonizacao}%'))
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

    @views.route('/adicionar/<int:vinho_id>', methods=['GET', 'POST'])
    @login_required
    def add_wine(vinho_id):
        if request.method == 'POST':
            if 'addvinho' in request.form:
                print(vinho_id)
                localizacao = request.form.get('localizacao')
                quantidade = request.form.get('quantidade')
                print(current_user)

                novo_inventario = Inventario(localizacao=localizacao, quantidade=quantidade, user_id=current_user.id, vinho_id=vinho_id)  #providing the schema for the note 
                db.session.add(novo_inventario) #adding the note to the database 
                db.session.commit()

                flash('Vinho Adicionado!', category='success')
                return redirect(url_for('views.home'))

        return render_template("add_wine.html", user=current_user)

    @views.route('/remover_vinho/<int:vinho_id>/<int:inventario_id>', methods=['POST'])
    @login_required
    def remover_vinho(vinho_id, inventario_id):
        inventario = Inventario.query.filter_by(user_id=current_user.id, vinho_id=vinho_id, id=inventario_id).first()

        if inventario:
            db.session.delete(inventario)
            db.session.commit()
            flash('Vinho removido do inventário com sucesso.', 'success')
        else:
            flash('Vinho não encontrado no inventário.', 'error')

        return redirect(url_for('views.home'))

    
    @views.route('/editar_vinho/<int:vinho_id>/<int:inventario_id>', methods=['POST'])
    @login_required
    def editar_vinho(vinho_id, inventario_id):
        inventario = Inventario.query.filter_by(id=inventario_id, vinho_id=vinho_id, user_id=current_user.id).first()

        if inventario:
            quantidade = request.form.get('quantidade')
            localizacao = request.form.get('localizacao')

            if quantidade:
                inventario.quantidade = quantidade

            if localizacao:
                inventario.localizacao = localizacao

            db.session.commit()
            flash('Dados do vinho editados com sucesso.', 'success')
        else:
            flash('Vinho não encontrado no inventário.', 'error')

        return redirect(url_for('views.home'))

