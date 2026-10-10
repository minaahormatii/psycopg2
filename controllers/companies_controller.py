from flask import jsonify, request

from db import conn, cursor

def create_company():
    post_data = request.form if request.form else request.json

    company_name = post_data.get("company_name")

    if not company_name:
        return jsonify({"message": "company_name is required"}), 400

    result = cursor.execute("""
        SELECT * FROM companies WHERE company_name = %s 
    """, (company_name,))

    result = cursor.fetchone()

    if result:
        return jsonify({"message": "Company already exists"}), 400

    cursor.execute("""
        INSERT INTO companies (company_name) VALUES (%s)
    """, (company_name,))
    conn.commit()

    final_result = cursor.execute("""
        SELECT * FROM companies WHERE company_name = %s
    """, (company_name,))

    final_result = cursor.fetchone()

    record = {
        "company_id": final_result[0],
        "company_name": final_result[1]
    }
    return jsonify({"message": "Company created successfully", "result": record}), 201

def get_all_companies():
    result = cursor.execute("""
        SELECT * FROM companies
    """)
    result = cursor.fetchall()

    record_list = []
    for record in result:
        record = {
            "company_id": record[0],
            "company_name": record[1]
        }
        record_list.append(record)
    return jsonify({"message": "Companies found", "results": record_list}), 200

def get_company_by_id(company_id):
    result = cursor.execute("""
        SELECT * FROM companies WHERE company_id = %s
    """, (company_id,))

    result = cursor.fetchone()

    if not result:
        return jsonify({"message": "Company not found"}), 404

    record = {
        "company_id": result[0],
        "company_name": result[1]
    }
    return jsonify({"message": "Company found", "result": record}), 200

def update_company_by_id(company_id):
    post_data = request.form if request.form else request.json

    company_name = post_data.get("company_name")

    result = cursor.execute("""
        SELECT * FROM companies WHERE company_id = %s
    """, (company_id,))

    result = cursor.fetchone()

    if not result:
        return jsonify({"message": "Company not found"}), 404

    try:
        cursor.execute("""
            UPDATE companies SET company_name = %s WHERE company_id = %s
        """, (company_name, company_id))
        conn.commit()

        final_result = cursor.execute("""
            SELECT * FROM companies WHERE company_id = %s
        """, (company_id,))
        final_result = cursor.fetchone()

        record = {
            "company_id": final_result[0],
            "company_name": final_result[1]
        }
        return jsonify({"message": "Company updated successfully", "result": record}), 200

    except Exception as e:
        cursor.execute("ROLLBACK;")
        return jsonify({"message": f"{e}: Failed to update company"}), 400

    finally:
        conn.commit()

def delete_company_by_id(company_id):
    result = cursor.execute("""
        SELECT * FROM companies WHERE company_id = %s
    """, (company_id,))

    result = cursor.fetchone()

    if not result:
        return jsonify({"message": "Company not found"}), 404

    try:
        cursor.execute("""
            DELETE FROM companies WHERE company_id = %s
        """, (company_id,))

    except Exception as e:
        result = cursor.execute("ROLLBACK;")
        return jsonify({"message": f"{e}: Failed to delete company"}), 400

    finally:
        conn.commit()

    return jsonify({"message": "Company deleted successfully"}), 200