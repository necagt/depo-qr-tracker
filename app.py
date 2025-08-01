from flask import Flask, render_template, request, redirect, url_for
from config import get_db_connection
import qrcode
import os

app = Flask(__name__)
QR_FOLDER = 'static/qrcodes'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_material():
    data = {
        'name': request.form['name'],
        'type': request.form['type'],
        'code': request.form['code'],
        'shelf': request.form['shelf'],
        'shelf_life': int(request.form['shelf_life']),
        'shelf_life_unit': request.form['shelf_life_unit'],
        'warehouse': request.form['warehouse']
    }

    # Veriyi veritabanına ekle
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO materials (name, type, code, shelf, shelf_life, shelf_life_unit, warehouse)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        data['name'], data['type'], data['code'], data['shelf'],
        data['shelf_life'], data['shelf_life_unit'], data['warehouse']
    ))
    conn.commit()
    material_id = cursor.lastrowid
    cursor.close()
    conn.close()

    # QR kod oluştur
    url = request.host_url + 'material/' + str(material_id)
    img = qrcode.make(url)
    path = os.path.join(QR_FOLDER, f"{material_id}.png")
    img.save(path)

    return redirect(f"/material/{material_id}")

@app.route('/material/<int:id>')
def show_material(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM materials WHERE id = %s", (id,))
    material = cursor.fetchone()
    cursor.close()
    conn.close()

    if material:
        return render_template('material.html', material=material)
    else:
        return "Malzeme bulunamadı", 404

@app.route('/track', methods=['GET', 'POST'])
def track_material():
    if request.method == 'POST':
        code = request.form['code']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM materials WHERE code = %s", (code,))
        material = cursor.fetchone()
        cursor.close()
        conn.close()

        if material:
            return redirect(url_for('show_material', id=material['id']))
        else:
            return "Malzeme bulunamadı", 404
    return render_template('track.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)

