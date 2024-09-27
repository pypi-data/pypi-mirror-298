import json
import os
from operator import and_

from flask import Blueprint
from flask import jsonify
from flask import render_template
from flask import request

from flask_login import current_user
from flask_login import login_required

from modules.box__ecommerce.category.models import Category
from modules.box__ecommerce.pos.models import Transaction
from modules.box__ecommerce.product.models import Product

# from flask import url_for
# from flask import redirect
# from flask import flash
# from shopyo.api.html import notify_success


# from shopyo.api.forms import flash_errors


dirpath = os.path.dirname(os.path.abspath(__file__))
module_info = {}

with open(dirpath + "/info.json") as f:
    module_info = json.load(f)

globals()["{}_blueprint".format(module_info["module_name"])] = Blueprint(
    "{}".format(module_info["module_name"]),
    __name__,
    template_folder="templates",
    url_prefix=module_info["url_prefix"],
)


module_blueprint = globals()["{}_blueprint".format(module_info["module_name"])]


@module_blueprint.route("/")
@login_required
def index():
    context = {}
    categories = Category.query.all()
    context.update({"categories": categories})
    return render_template("pos/index.html", **context)


@module_blueprint.route("/transaction", methods=["GET", "POST"])
@login_required
def transaction():
    if request.method == "POST":
        json = request.get_json()
        print(json)
        for key in json:
            print(key)
            prod_id = key
            number_items = json[key]["count"]
            product = Product.query.filter_by(barcode=str(prod_id)).first()
            print(product)
            product.in_stock -= number_items

            product.update()

        transaction = Transaction()
        try:
            transaction.chashier_id = current_user.id
            transaction.products = [
                Product.query.filter_by(barcode=key).first() for key in json
            ]
            transaction.insert()
        except:
            print("User not logged in")

    return jsonify({"message": "ok"})
