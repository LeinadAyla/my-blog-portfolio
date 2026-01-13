from flask import Flask

def create_app():
    """Função Factory para criar e configurar a instância do Flask"""
    app = Flask(__name__)

    with app.app_context():
        # Aqui é onde registraremos os Blueprints futuramente
        from .intro import intro_bp
        app.register_blueprint(intro_bp)

        return app
