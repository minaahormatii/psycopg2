from flask import Blueprint

import controllers

product_category_xref = Blueprint('product_category_xref', __name__)

@product_category_xref.route('/product/category', methods=['POST'])
def create_product_category_xref():
    return controllers.create_product_category_xref()
