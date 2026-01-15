from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Instância do banco de dados (SQLAlchemy)
db = SQLAlchemy()

def create_app():
    # Inicializa o Flask definindo onde estão os templates globais
    app = Flask(__name__, template_folder='templates')

    # --- CONFIGURAÇÕES DO APP ---
    
    # Caminho do banco de dados SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # CHAVE SECRETA: Essencial para criptografar cookies de sessão e permitir logins
    app.config['SECRET_KEY'] = 'uma-chave-muito-secreta-selva-2026'

    # Inicializa o db com as configurações deste app
    db.init_app(app)

    # Inicializa o Migrate para controle de versão do banco de dados
    migrate = Migrate(app, db)

    # Registro dos Blueprints (modularização do código)
    from .intro.intro import intro_bp
    from .about.about import about_bp
    from .blog.blog import blog_bp 
    
    app.register_blueprint(intro_bp)
    app.register_blueprint(about_bp)
    app.register_blueprint(blog_bp)

    return app