from datetime import datetime
import requests  # Essencial para falar com o n8n!
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
    
    # --- EVOLUÇÃO DO MODELO ---
    categoria = db.Column(db.String(50), nullable=True)
    codigo_snippet = db.Column(db.Text, nullable=True)
    
    # Relacionamento com Livros (um post pertence a um livro)
    livro_id = db.Column(db.Integer, db.ForeignKey('livro.id'), nullable=True)
    livro = db.relationship('Livro', backref=db.backref('posts', lazy=True))

    # Relacionamento para acessar os comentários de um post
    comentarios = db.relationship('Comentario', backref='post', lazy=True, cascade="all, delete-orphan")

# Model para os Livros
class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), unique=True, nullable=False)

    def __repr__(self):
        return f'<Livro {self.titulo}>'

# Model para os Comentários
class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    # Chave estrangeira para ligar o comentário ao post
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

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

@blog_bp.route('/blog/livros', methods=['GET', 'POST'])
def gerenciar_livros():
    if not session.get('logado'):
        return redirect(url_for('blog_bp.login'))

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        if titulo:
            livro_existente = Livro.query.filter_by(titulo=titulo).first()
            if livro_existente:
                flash(f'Livro "{titulo}" já existe.', 'warning')
            else:
                novo_livro = Livro(titulo=titulo)
                db.session.add(novo_livro)
                db.session.commit()
                flash(f'Livro "{titulo}" adicionado com sucesso!', 'success')
        else:
            flash('O título do livro não pode ser vazio.', 'danger')
        return redirect(url_for('blog_bp.gerenciar_livros'))

    livros = Livro.query.order_by(Livro.titulo).all()
    return render_template('blog/livros.html', livros=livros)

# --- ROTAS DO BLOG (CRUD) ---
@blog_bp.route('/blog')
def lista_posts():
    # Buscamos todos os posts para enviar ao template
    posts = Post.query.order_by(Post.data_criacao.desc()).all()
    return render_template('blog/index.html', posts=posts)

@blog_bp.route('/blog/post/<int:post_id>')
def ver_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('blog/post.html', post=post)

@blog_bp.route('/blog/post/<int:post_id>/comentar', methods=['POST'])
def novo_comentario(post_id):
    post = Post.query.get_or_404(post_id)
    conteudo = request.form.get('conteudo')
    
    if conteudo:
        comentario = Comentario(conteudo=conteudo, post=post)
        db.session.add(comentario)
        db.session.commit()

    return redirect(url_for('blog_bp.ver_post', post_id=post_id))

@blog_bp.route('/blog/novo', methods=['GET', 'POST'])
def novo_post():
    if not session.get('logado'): return redirect(url_for('blog_bp.login'))
    
    livros = Livro.query.order_by(Livro.titulo).all() # Para preencher o select
    categorias_disponiveis = ["Segurança", "Automação", "Estudos", "Outro"] # Categorias fixas

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        conteudo = request.form.get('conteudo')
        categoria = request.form.get('categoria')
        codigo_snippet = request.form.get('codigo_snippet')
        livro_id = request.form.get('livro_id')
        
        # Converte livro_id para int ou None se vazio
        livro_id = int(livro_id) if livro_id else None

        # 1. Salva no banco de dados local
        post = Post(
            titulo=titulo,
            conteudo=conteudo,
            categoria=categoria if categoria and categoria != "Outro" else None, # Salva como None se for "Outro" ou não selecionado
            codigo_snippet=codigo_snippet if codigo_snippet else None,
            livro_id=livro_id
        )
        db.session.add(post)
        db.session.commit()

        # 2. --- CONEXÃO COM N8N (MODO TESTE ATIVADO) ---
        # Adicionado o '-test' para casar com o botão "Execute Workflow" do n8n
        URL_N8N = "http://localhost:5678/webhook/post-blog-engenharia"
        
        dados_n8n = {
            "titulo": titulo,
            "autor": "Engenheiro Wilson",
            "mensagem": "🔥 Novo post técnico publicado!",
            "link": url_for('blog_bp.lista_posts', _external=True)
        }
        
        try:
            # timeout=5 evita que o blog trave se o Docker estiver lento
            requests.post(URL_N8N, json=dados_n8n, timeout=5)
        except Exception as e:
            # O post é criado mas não crasha o site se o n8n falhar
            print(f"Alerta: n8n offline ou erro de conexão: {e}")

        return redirect(url_for('blog_bp.lista_posts'))
    
    return render_template('blog/novo.html', livros=livros, categorias_disponiveis=categorias_disponiveis)

@blog_bp.route('/blog/editar/<int:id>', methods=['GET', 'POST'])
def editar_post(id):
    if not session.get('logado'): return redirect(url_for('blog_bp.login'))
    post = Post.query.get_or_404(id) # Garante que o post exista ou dá erro 404
    
    livros = Livro.query.order_by(Livro.titulo).all() # Para preencher o select
    categorias_disponiveis = ["Segurança", "Automação", "Estudos", "Outro"] # Categorias fixas

    if request.method == 'POST':
        post.titulo = request.form.get('titulo')
        post.conteudo = request.form.get('conteudo')
        
        post.categoria = request.form.get('categoria')
        if post.categoria == "Outro": post.categoria = None # Se for "Outro", salva como None

        post.codigo_snippet = request.form.get('codigo_snippet')
        if not post.codigo_snippet: post.codigo_snippet = None # Salva como None se vazio

        livro_id = request.form.get('livro_id')
        post.livro_id = int(livro_id) if livro_id else None # Converte para int ou None

        db.session.commit()
        flash('Post atualizado com sucesso!', 'success')
        return redirect(url_for('blog_bp.lista_posts'))
    
    return render_template('blog/editar.html', post=post, livros=livros, categorias_disponiveis=categorias_disponiveis)

@blog_bp.route('/blog/excluir/<int:id>')
def excluir_post(id):
    if not session.get('logado'): return redirect(url_for('blog_bp.login'))
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog_bp.lista_posts'))

from sqlalchemy import func

# --- ROTA: AGENTE DE IA ---
@blog_bp.route('/blog/ajuda_ia', methods=['POST'])
def ajuda_ia():
    if not session.get('logado'): 
        return jsonify({"feedback": "Acesso negado."}), 403
    
    dados = request.get_json()
    conteudo_atual = dados.get('conteudo', '')
    
    if not conteudo_atual:
        return jsonify({"feedback": "O campo está vazio!"}), 400

    feedback_ia = pedir_ajuda_ia(conteudo_atual)
    return jsonify({"feedback": feedback_ia})

# --- ROTA: DASHBOARD DE ENGENHARIA ---
@blog_bp.route('/blog/dashboard')
def dashboard():
    if not session.get('logado'):
        return redirect(url_for('blog_bp.login'))

    # 1. Contagem de posts por categoria
    contagem_categorias = dict(db.session.query(
        Post.categoria, func.count(Post.id)
    ).group_by(Post.categoria).all())

    # 2. Total de automações (posts com código)
    total_automacoes = Post.query.filter(Post.codigo_snippet.isnot(None)).count()
    
    # Mapeia os resultados para o template
    metricas = {
        "seguranca": contagem_categorias.get('Segurança', 0),
        "automacao": contagem_categorias.get('Automação', 0),
        "estudos": contagem_categorias.get('Estudos', 0),
        "total_automacoes": total_automacoes
    }

    return render_template('blog/dashboard.html', metricas=metricas)