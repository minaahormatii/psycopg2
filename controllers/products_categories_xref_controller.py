from flask import jsonify, request

from db import cursor, conn

def create_product_category_xref():
    post_data = request.form if request.form else request.json

    product_id = post_data.get("product_id")
    category_id = post_data.get("category_id")

    if not product_id or not category_id:
        return jsonify({"message": "product_id and category_id are required"}), 400

    result = cursor.execute("""
        SELECT * FROM ProductsCategoriesXref WHERE product_id = %s AND category_id = %s;
    """, (product_id, category_id))

    result = cursor.fetchone()

    if result:
        return jsonify({"message": "product-category xref already exists"}), 400

    cursor.execute("""
        INSERT INTO ProductsCategoriesXref (product_id, category_id)
        VALUES (%s, %s)
    """, (product_id, category_id))
    conn.commit()

    final_result = cursor.execute("""
        SELECT * FROM ProductsCategoriesXref WHERE product_id = %s AND category_id = %s;
    """, (product_id, category_id))

    final_result = cursor.fetchone()

    record = {
        "product_id": final_result[0],
        "category_id": final_result[1]
    }

    return jsonify({"message": "product-category xref created successfully", "result": record}), 201

