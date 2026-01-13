from flask import Blueprint, render_template
from datetime import datetime
from random import sample

# DEFINIÇÃO CORRETA: O Blueprint é criado aqui dentro
intro_bp = Blueprint('intro_bp', __name__, template_folder='templates')

class BannerColors:
    COLORS = [
        "lightcoral", "red", "gold", "blue", "green", "silver"
    ]
    def get_colors(self):
        return sample(BannerColors.COLORS, 5)

@intro_bp.route("/")
def home():
    # Nota: O Flask agora vai procurar em templates/intro/index.html
    return render_template("intro/index.html", data={
        "now": datetime.now(),
        "banner_colors": BannerColors().get_colors()
    })
