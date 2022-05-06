from crypt import methods
import uuid
from flask import Flask, render_template, request, session
import pymongo
app = Flask('app')
app.secret_key = 'eticaret icin cok gizli anahtar'

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["EticaretDB"]
urunler_tablosu = mydb["urunler"]
sepet_tablosu = mydb["sepet"]


@app.route('/deneme')
def deneme():
    urunlistesi = urunler_tablosu.find({})
    for urun in urunlistesi:
        print(urun["urun_adi"])
    return "OK"


@app.route('/')
def ana_sayfa():
    if session.get('oturum_id') is None:
        session['oturum_id'] = str(uuid.uuid1())
    oturum_id = session.get('oturum_id')
    print(str(oturum_id))        

    urunlistesi = urunler_tablosu.find({})
    return render_template("anasayfa.html", urun_listesi=urunlistesi)


@app.route('/telefon')
def telefon_goster():
  return render_template("telefon.html")


@app.route('/sepeteekle', methods=["POST"])
def sepete_ekle():
    #oturum bilgisi gerekli
    #ürün bilgisi gerekli
    if session.get('oturum_id') is None:
        session['oturum_id'] = str(uuid.uuid1())
    oturum_id = session.get('oturum_id')
    print(str(oturum_id))
    
    urun_id =  request.form["urun_id"]
    sepet_bilgisi = {"oturum_id": oturum_id, "urun_id": urun_id}
    sepet_tablosu.save(sepet_bilgisi)
    #return render_template("sepet.html", sepet_urun_listesi=sepet_urun_listesi)
    #return "Sepete eklendi: oturum:" + oturum_id + " , ürün:" + urun_id
    oturum_urun_listesi = list(sepet_tablosu.find({"oturum_id":oturum_id}))
    sepet_urun_listesi = []
    for oturum_urun in oturum_urun_listesi:
        urun_detay = dict(urunler_tablosu.find_one({"_id": oturum_urun["urun_id"]}))
        sepet_urun_listesi.append(urun_detay)

    print("sepet_urun_listesi:", sepet_urun_listesi)
    return render_template("sepet.html", sepet_urun_listesi=sepet_urun_listesi)



@app.route('/sepet')
def sepet_goster():
    oturum_id = session.get('oturum_id')
    oturum_urun_listesi = list(sepet_tablosu.find({"oturum_id":oturum_id}))
    sepet_urun_listesi = []
    for oturum_urun in oturum_urun_listesi:
        urun_detay = dict(urunler_tablosu.find_one({"_id": oturum_urun["urun_id"]}))
        sepet_urun_listesi.append(urun_detay)

    print("sepet_urun_listesi:", sepet_urun_listesi)
    return render_template("sepet.html", sepet_urun_listesi=sepet_urun_listesi)



app.run(debug=True, host='0.0.0.0', port=5000)