from flask import jsonify, request

from db import conn, cursor

def create_category():
    post_data = request.form if request.form else request.json

    category_name = post_data.get("category_name")

    if not category_name:
        return jsonify({"message": "category_name is required"}), 400

    result = cursor.execute("""
        SELECT * FROM categories WHERE category_name = %s
    """, (category_name,))

    result = cursor.fetchone()

    if result:
        return jsonify({"message": "Category already exists"}), 400

    cursor.execute("""
        INSERT INTO categories (category_name) VALUES (%s)
    """, (category_name,))
    conn.commit()

    final_result = cursor.execute("""
        SELECT * FROM categories WHERE category_name = %s
    """, (category_name,))

    final_result = cursor.fetchone()

    record = {
        "category_id": final_result[0],
        "category_name": final_result[1]
    }
    return jsonify({"message": "Category created successfully", "result": record}), 201

def get_all_categories():
    result = cursor.execute("""
        SELECT * FROM categories
    """)
    result = cursor.fetchall()

    record_list = []
    for record in result:
        record = {
            "category_id": record[0],
            "category_name": record[1]
        }
        record_list.append(record)
    return jsonify({"message": "Categories found", "results": record_list}), 200

def get_category_by_id(category_id):
    result = cursor.execute("""
        SELECT * FROM categories WHERE category_id = %s
    """, (category_id,))

    result = cursor.fetchone()

    if not result:
        return jsonify({"message": "Category not found"}), 404

    record = {
        "category_id": result[0],
        "category_name": result[1]
    }
    return jsonify({"message": "Category found", "result": record}), 200

def update_category_by_id(category_id):
    post_data = request.form if request.form else request.json

    category_name = post_data.get("category_name")

    result = cursor.execute("""
        SELECT * FROM categories WHERE category_id = %s
    """, (category_id,))

    result = cursor.fetchone()

    if not result:
        return jsonify({"message": "Category not found"}), 404

    try:
        cursor.execute("""
            UPDATE categories SET category_name = %s WHERE category_id = %s
        """, (category_name, category_id))
        conn.commit()

        final_result = cursor.execute("""
            SELECT * FROM categories WHERE category_id = %s
        """, (category_id,))
        final_result = cursor.fetchone()

        record = {
            "category_id": final_result[0],
            "category_name": final_result[1]
        }
        return jsonify({"message": "Category updated successfully", "result": record}), 200

    except Exception as e:
        cursor.execute("ROLLBACK;")
        return jsonify({"message": f"{e}: Failed to update category"}), 400

    finally:
        conn.commit()

def delete_category_by_id(category_id):
    result = cursor.execute("""
        SELECT * FROM categories WHERE category_id = %s
    """, (category_id,))

    result = cursor.fetchone()

    if not result:
        return jsonify({"message": "Category not found"}), 404

    try:
        cursor.execute("""
            DELETE FROM categories WHERE category_id = %s
        """, (category_id,))

    except Exception as e:
        result = cursor.execute("ROLLBACK;")
        return jsonify({"message": f"{e}: Failed to delete category"}), 400

    finally:
        conn.commit()

    return jsonify({"message": "Category deleted successfully"}), 200