from flask import Flask, render_template
import pymongo
app = Flask('app')

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["EticaretDB"]
urunler_tablosu = mydb["urunler"]


@app.route('/deneme')
def deneme():
    urunlistesi = urunler_tablosu.find({})
    for urun in urunlistesi:
        print(urun["urun_adi"])
    return "OK"



@app.route('/')
def ana_sayfa():
    urunlistesi = urunler_tablosu.find({})
    return render_template("anasayfa.html", urun_listesi=urunlistesi)

@app.route('/telefon')
def telefon_goster():
  return render_template("telefon.html")

app.run(debug=True, host='0.0.0.0', port=5000)