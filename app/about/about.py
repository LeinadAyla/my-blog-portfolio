from flask import Blueprint, render_template

# Criamos o Blueprint 'about'
about_bp = Blueprint(
    'about', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

@about_bp.route('/sobre-mim')
def sobre():
    # Aqui você pode passar dados para o seu perfil
    meu_perfil = {
        "nome": "Leinad Ayla",
        "cargo": "Engenheiro de Software & Segurança",
        "bio": "Desenvolvedor focado em arquitetura Python escalável e segura."
    }
    return render_template('about/index.html', perfil=meu_perfil)
