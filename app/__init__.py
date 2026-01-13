from flask import Flask

def create_app():
    # Inicializa o Flask definindo onde estão os templates globais
    app = Flask(__name__, template_folder='templates')

    # Importações dentro da função para evitar importação circular
    from .intro.intro import intro_bp
    from .about.about import about_bp

    # Registro dos Blueprints
    app.register_blueprint(intro_bp)
    app.register_blueprint(about_bp)

    return app