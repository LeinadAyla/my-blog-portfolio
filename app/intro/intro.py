from flask import Blueprint, render_template
from datetime import datetime
from random import sample, choice

# DEFINIÇÃO CORRETA: O Blueprint é criado aqui dentro
intro_bp = Blueprint('intro_bp', __name__, template_folder='templates')

class BannerColors:
    COLORS = [
        "lightcoral", "red", "gold", "blue", "green", "silver"
    ]
    def get_colors(self):
        # Retorna 5 cores aleatórias da lista principal
        return sample(BannerColors.COLORS, 5)

@intro_bp.route("/")
def home():
    # Pegamos as 5 cores que serão exibidas na lista
    lista_cores = BannerColors().get_colors()
    
    # O SEGREDO: Escolhemos uma dessas 5 para ser a cor ativa do banner
    cor_ativa = choice(lista_cores)
    
    # Nota: O Flask agora vai procurar em templates/intro/index.html
    return render_template("intro/index.html", data={
        "now": datetime.now(),
        "banner_colors": lista_cores,
        "active_color": cor_ativa  # <--- ESSA VARIÁVEL É A CHAVE DO SUCESSO!
    })