from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Criamos a instância do banco FORA para evitar importação circular
db = SQLAlchemy()

def create_app():
    # Inicializa o Flask definindo onde estão os templates globais
    app = Flask(__name__, template_folder='templates')

    # Configurações do Banco de Dados SQLite (o arquivo será criado na raiz do projeto)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa o db com as configurações deste app
    db.init_app(app)

    # Importações dos Blueprints (dentro da função para evitar erros de importação circular)
    from .intro.intro import intro_bp
    from .about.about import about_bp
    from .blog.blog import blog_bp  # NOVO: Importando o módulo de blog
    
    # Registro dos Blueprints no aplicativo
    app.register_blueprint(intro_bp)
    app.register_blueprint(about_bp)
    app.register_blueprint(blog_bp)  # NOVO: Registrando a rota /blog

    return app