from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app import db 
# Importamos a função do agente de IA que você criou
from app.ia_agente import pedir_ajuda_ia

blog_bp = Blueprint('blog_bp', __name__, template_folder='templates')

# Model para persistência no SQLite
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

# --- ROTAS DE PROTEÇÃO ---
@blog_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        senha = request.form.get('senha')
        if senha == 'SELVA2026':  # Sua senha mestre definida
            session['logado'] = True
            return redirect(url_for('blog_bp.lista_posts'))
    return render_template('blog/login.html')

@blog_bp.route('/logout')
def logout():
    session.pop('logado', None)
    return redirect(url_for('blog_bp.lista_posts'))

# --- ROTAS DO BLOG (CRUD) ---
@blog_bp.route('/blog')
def lista_posts():
    posts = Post.query.order_by(Post.data_criacao.desc()).all()
    return render_template('blog/index.html', posts=posts)

@blog_bp.route('/blog/novo', methods=['GET', 'POST'])
def novo_post():
    if not session.get('logado'): return redirect(url_for('blog_bp.login'))
    if request.method == 'POST':
        post = Post(titulo=request.form.get('titulo'), conteudo=request.form.get('conteudo'))
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('blog_bp.lista_posts'))
    return render_template('blog/novo.html')

@blog_bp.route('/blog/editar/<int:id>', methods=['GET', 'POST'])
def editar_post(id):
    if not session.get('logado'): return redirect(url_for('blog_bp.login'))
    post = Post.query.get_or_404(id)
    if request.method == 'POST':
        post.titulo = request.form.get('titulo')
        post.conteudo = request.form.get('conteudo')
        db.session.commit()
        return redirect(url_for('blog_bp.lista_posts'))
    return render_template('blog/editar.html', post=post)

@blog_bp.route('/blog/excluir/<int:id>')
def excluir_post(id):
    if not session.get('logado'): return redirect(url_for('blog_bp.login'))
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog_bp.lista_posts'))

# --- NOVA ROTA: AGENTE DE IA ---
@blog_bp.route('/blog/ajuda_ia', methods=['POST'])
def ajuda_ia():
    # Verifica se você está logado antes de gastar seus créditos da API
    if not session.get('logado'): 
        return jsonify({"feedback": "Acesso negado. Logue-se primeiro."}), 403
    
    # Recebe o texto enviado via JavaScript (JSON)
    dados = request.get_json()
    conteudo_atual = dados.get('conteudo', '')
    
    if not conteudo_atual:
        return jsonify({"feedback": "O campo de conteúdo está vazio, Comandante!"}), 400

    # Chama o cérebro do Gemini
    feedback_ia = pedir_ajuda_ia(conteudo_atual)
    
    return jsonify({"feedback": feedback_ia})