import streamlit as st
import pickle
import numpy as np
from pymongo import MongoClient
from datetime import datetime

# Load model
pipe = pickle.load(open("Naive_model.pkl", "rb"))

# Fungsi konversi
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

# Streamlit App
st.title("Deteksi Email Spam")

email_input = st.text_area("Masukkan isi email:")

if st.button("Deteksi"):
    result = pipe.predict([email_input])[0]
    result = convert_numpy(result)

    # Simpan ke MongoDB
    collection.insert_one({
        "email": email_input,
        "prediction": result,
        "timestamp": datetime.now()
    })

    st.success(f"Prediksi: {'SPAM' if result == 1 else 'BUKAN SPAM'}")
