from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

from flask_migrate import Migrate

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kullanici_model_owner:o1Ba0DtgARUp@ep-lively-block-a57av5fv.us-east-2.aws.neon.tech/kullanici_model?sslmode=require'
db = SQLAlchemy(app)

class Kullanici(db.Model):
    __tablename__ = 'Kullanicilar'

    id = db.Column(db.Integer, primary_key=True)
    isim = db.Column(db.String(80), nullable=False)
    soyisim = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telno = db.Column(db.String(20), nullable=False)

@app.route('/kayit', methods=['POST'])
def kayit():
    try:
        data = request.get_json()
        isim = data.get('isim')
        soyisim = data.get('soyisim')
        email = data.get('email')
        telno = data.get('telefon numarasi')

        yeni_kullanici = Kullanici(isim=isim, soyisim=soyisim, email=email, telno=telno)
        db.session.add(yeni_kullanici)
        db.session.commit()

        return jsonify({"message": "Kayıt oldun"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/kayitgetir', methods=['GET'])
def kayitgetir():
    try:  
        kullanicilar = Kullanici.query.all()
        sonuc = []

        for kullanici in kullanicilar:
            sonuc.append({
                "isim": kullanici.isim,
                "soyisim": kullanici.soyisim,
                "email": kullanici.email,
                "telefon numarasi": kullanici.telno
            })

        return jsonify({"content": sonuc})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
        app.run(debug=True)
