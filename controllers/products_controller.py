from flask import jsonify, request

from db import conn, cursor


def create_product():
    post_data = request.form if request.form else request.json

    product_name = post_data.get("product_name")
    description = post_data.get("description")
    price = post_data.get("price")
    company_id = post_data.get("company_id")

    if not product_name:
        return jsonify({"message": "product name is a required field"}), 400

    try:
        cursor.execute("""
            SELECT * FROM Products WHERE product_name = %s
        """, (product_name,))

        result = cursor.fetchone()

        if result:
            return jsonify({"message": "product already exists"}), 400

        cursor.execute("""
            INSERT INTO Products
                (product_name, description, price, company_id)
            VALUES (%s, %s, %s, %s)
            RETURNING product_id, product_name, description, price, company_id, active
        """, (product_name, description, price, company_id))

        final_result = cursor.fetchone()
        conn.commit()

        record = {
            "product_id": final_result[0],
            "product_name": final_result[1],
            "description": final_result[2],
            "price": final_result[3],
            "company_id": final_result[4],
            "active": final_result[5]
        }

        return jsonify({
            "message": "product created",
            "result": record
        }), 201

    except Exception as e:
        conn.rollback()
        print("Error creating product:", e)
        return jsonify({"message": "unable to create product", "error": str(e)}), 500



def get_all_products():
    result = cursor.execute("""
        SELECT * FROM Products;
    """)
    result = cursor.fetchall()

    record_list = []
    for record in result:
        record = {
            "product_id": record[0],
            "product_name": record[1],
            "description": record[2],
            "price": record[3],
            "company_id": record[4],
            "active": record[5],
        }
        record_list.append(record)
    return jsonify({"message": "products found", "results": record_list}), 200

def get_active_products():
    result = cursor.execute("""
        SELECT * FROM Products WHERE active = TRUE;
    """)
    result = cursor.fetchall()

    record_list = []
    for record in result:
        record = {
            "product_id": record[0],
            "product_name": record[1],
            "description": record[2],
            "price": record[3],
            "company_id": record[4],
            "active": record[5],
        }
        record_list.append(record)
    return jsonify({"message": "active products found", "results": record_list}), 200

def get_product_by_id(product_id):
    result = cursor.execute("""
        SELECT * FROM Products WHERE product_id = %s;
    """, (product_id,))

    result = cursor.fetchone()

    if not result:
        return jsonify({"message": "product does not exist"}), 404

    record = {
        "product_id": result[0],
        "product_name": result[1],
        "description": result[2],
        "price": result[3],
        "company_id": result[4],
        "active": result[5]
    }
    return jsonify({"message": "product found", "result": record}), 200

def update_product_by_id(product_id):
    post_data = request.form if request.form else request.json

    product_name = post_data.get("product_name")
    description = post_data.get("description")
    price = post_data.get("price")
    company_id = post_data.get("company_id")
    active = post_data.get("active")

    result = cursor.execute("""
        SELECT * FROM Products WHERE product_id = %s;
    """, (product_id,))

    result = cursor.fetchone()

    if not result:
        return jsonify({"message": "product does not exist"}), 404

    try:
        cursor.execute("""
            UPDATE Products
            SET product_name = %s,
                description = %s,
                price = %s,
                company_id = %s,
                active = %s
            WHERE product_id = %s;
        """, (product_name, description, price, company_id, active, product_id))
        conn.commit()

        final_result = cursor.execute("""
                SELECT * FROM Products WHERE product_id = %s;
            """, (product_id,))
        final_result = cursor.fetchone()
        
        record = {
                "product_id": final_result[0],
                "product_name": final_result[1],
                "description": final_result[2],
                "price": final_result[3],
                "company_id": final_result[4],
                "active": final_result[5]
            }
        return jsonify({"message": "product updated", "result": record}), 200

    except Exception as e:
        cursor.execute("ROLLBACK;")
        return jsonify({"message": f"{e}: unable to update product"}), 400

    finally:
        conn.commit()


def delete_product_by_id(product_id):
    result = cursor.execute("""
        SELECT * FROM Products WHERE product_id = %s;
    """, (product_id,))

    result = cursor.fetchone()

    if not result:
        return jsonify({"message": "product does not exist"}), 404

    try:
        cursor.execute("""
            DELETE FROM Products WHERE product_id = %s;
        """, (product_id,))

    except Exception as e:
        result = cursor.execute("ROLLBACK;")
        return jsonify({"message": f"{e}: unable to delete product"}), 400

    finally:
        conn.commit()

    return jsonify({"message": "product deleted"}), 200

def get_products_by_company_id(company_id):
    result = cursor.execute("""
        SELECT * FROM Products WHERE company_id = %s;
    """, (company_id,))

    result = cursor.fetchall()

    if not result:
        return jsonify({"message": "no products found for this company"}), 404

    records_list = []
    for record in result:
        record = {
            "product_id": record[0],
            "product_name": record[1],
            "description": record[2],
            "price": record[3],
            "company_id": record[4],
            "active": record[5]
        }
        records_list.append(record)

    return jsonify({"message": "products for this company found", "results": records_list}), 200
   