from flask import Flask, render_template, request
import pickle
from pymongo import MongoClient
from datetime import datetime
import numpy as np

# Fungsi untuk mengonversi tipe data NumPy
def convert_numpy(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj

# Koneksi MongoDB
client = MongoClient("mongodb+srv://egip3961:kuYAbaTOX@cluster0.ouoabdi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.dbspam
collection = db.predictions

app = Flask(__name__)

# Load model
pipe = pickle.load(open("Naive_model.pkl", "rb"))

@app.route('/', methods=["GET", "POST"])
def main_function():
    if request.method == "POST":
        text = request.form
        emails = text['email']
        
        list_email = [emails]
        output = pipe.predict(list_email)[0]
        
        # Konversi output jika diperlukan
        output = convert_numpy(output)
        
        # Simpan ke MongoDB
        collection.insert_one({
            "email": emails,
            "prediction": output,
            "timestamp": datetime.now()
        })

        return render_template("show.html", prediction=output)

    else:
        return render_template("index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

