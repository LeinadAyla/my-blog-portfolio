from flask import render_template
from datetime import datetime
from random import sample
from . import intro_bp

class BannerColors:
    COLORS = [
        "lightcoral", "red", "gold", "blue", "green", "silver"
    ]
    def get_colors(self):
        return sample(BannerColors.COLORS, 5)

@intro_bp.route("/")
def home():
    return render_template("index.html", data={
        "now": datetime.now(),
        "banner_colors": BannerColors().get_colors()
    })