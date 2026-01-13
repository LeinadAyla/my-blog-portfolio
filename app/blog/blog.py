from datetime import datetime
from flask import Blueprint, render_template
from app import db  # Importa a instância do banco que criamos no __init__.py

# Criando o Blueprint do Blog
blog_bp = Blueprint('blog_bp', __name__, template_folder='templates')

# Definindo a tabela de Postagens (Model) para o Banco de Dados
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Post {self.titulo}>'

# Rota para a página principal do blog - AJUSTADA
@blog_bp.route('/blog')
def lista_posts():
    # Buscamos todos os posts do banco de dados, ordenando pelos mais recentes
    # O .query.all() é o comando que traz os dados do SQLite para o Python
    posts = Post.query.order_by(Post.data_criacao.desc()).all()
    
    # Agora passamos a variável 'posts' para o template
    return render_template('blog/index.html', posts=posts)