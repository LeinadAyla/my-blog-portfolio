from flask import Blueprint

# Criando o Blueprint 'intro_bp'
# O static_folder e template_folder dizem ao Flask para procurar arquivos dentro deste módulo
intro_bp = Blueprint(
    'intro_bp', 
    __name__,
    static_folder="static",
    static_url_path="/intro/static",
    template_folder="templates"
)

from . import intro