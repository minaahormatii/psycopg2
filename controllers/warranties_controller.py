from flask import jsonify, request

from db import conn, cursor

def create_warranty():
    post_data = request.form if request.form else request.json

    warranty_months = post_data.get("warranty_months")
    product_id = post_data.get("product_id")

    if not warranty_months:
        return jsonify({"message": "warranty_months is required"}), 400

    result = cursor.execute("""
        SELECT * FROM warranties WHERE warranty_months = %s 
    """, (warranty_months,))

    result = cursor.fetchone()

    if result:
        return jsonify({"message": "Warranty already exists"}), 400

    cursor.execute("""
        INSERT INTO warranties (warranty_months, product_id) VALUES (%s, %s)
    """, (warranty_months, product_id))
    conn.commit()

    final_result = cursor.execute("""
        SELECT * FROM warranties WHERE warranty_months = %s
    """, (warranty_months,))

    final_result = cursor.fetchone()

    record = {
        "warranty_id": final_result[0],
        "warranty_months": final_result[1],
        "product_id": final_result[2]
    }
    return jsonify({"message": "Warranty created successfully", "result": record}), 201

def get_all_warranties():
    result = cursor.execute("""
        SELECT * FROM warranties
    """)
    result = cursor.fetchall()

    record_list = []
    for record in result:
        record = {
            "warranty_id": record[0],
            "warranty_months": record[1],
            "product_id": record[2]
        }
        record_list.append(record)
    return jsonify({"message": "Warranties found", "results": record_list}), 200

def get_warranty_by_id(warranty_id):
    result = cursor.execute("""
        SELECT * FROM warranties WHERE warranty_id = %s
    """, (warranty_id,))

    result = cursor.fetchone()

    if not result:
        return jsonify({"message": "Warranty not found"}), 404

    record = {
        "warranty_id": result[0],
        "warranty_months": result[1],
        "product_id": result[2]
    }
    return jsonify({"message": "Warranty found", "result": record}), 200

def update_warranty_by_id(warranty_id):
    post_data = request.form if request.form else request.json

    warranty_months = post_data.get("warranty_months")
    product_id = post_data.get("product_id")

    result = cursor.execute("""
        SELECT * FROM warranties WHERE warranty_id = %s
    """, (warranty_id,))

    result = cursor.fetchone()

    if not result:
        return jsonify({"message": "Warranty not found"}), 404

    try:
        cursor.execute("""
            UPDATE warranties SET warranty_months = %s, product_id = %s WHERE warranty_id = %s
        """, (warranty_months, product_id, warranty_id))
        conn.commit()

        final_result = cursor.execute("""
            SELECT * FROM warranties WHERE warranty_id = %s
        """, (warranty_id,))
        final_result = cursor.fetchone()

        record = {
            "warranty_id": final_result[0],
            "warranty_months": final_result[1],
            "product_id": final_result[2]
        }
        return jsonify({"message": "Warranty updated successfully", "result": record}), 200

    except Exception as e:
        cursor.execute("ROLLBACK;")
        return jsonify({"message": f"{e}: Failed to update warranty"}), 400

    finally:
        conn.commit()

def delete_warranty_by_id(warranty_id):
    result = cursor.execute("""
        SELECT * FROM warranties WHERE warranty_id = %s
    """, (warranty_id,))

    result = cursor.fetchone()

    if not result:
        return jsonify({"message": "Warranty not found"}), 404

    try:
        cursor.execute("""
            DELETE FROM warranties WHERE warranty_id = %s
        """, (warranty_id,))

    except Exception as e:
        result = cursor.execute("ROLLBACK;")
        return jsonify({"message": f"{e}: Failed to delete warranty"}), 400

    finally:
        conn.commit()

    return jsonify({"message": "Warranty deleted successfully"}), 200