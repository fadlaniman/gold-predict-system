from flask import Flask, render_template, request
import pandas as pd
import os

# Menyesuaikan dengan struktur folder modular 'core' yang baru
from core.predictor import GoldPredictor

app = Flask(__name__)

# ==========================================
# INIT MODEL ONLY ONCE (DI LUAR ROUTE)
# ==========================================
DATA_PATH = os.path.join('data', 'data.xlsx')
MODEL_PATH = 'model.keras'

predictor = GoldPredictor(
    data_path=DATA_PATH,
    model_path=MODEL_PATH,
    sheet_name='dataset'
)
# Catatan: `predictor.prepare()` sudah otomatis dipanggil di dalam 
# __init__ GoldPredictor baru Anda, jadi baris prepare manual bisa dihemat.

# ==========================================
# MAIN ROUTE
# ==========================================
@app.route("/", methods=['GET', 'POST'])
def main():
    # Menghapus 'global predictor' karena kita hanya membaca/memanggil 
    # method dari instance, bukan mengisinya ulang (re-assign) dengan objek baru.
    
    error_message = None
    success_message = None 

    # 1. AMBIL DATA MASTER/HISTORIS ASLI (Keadaan Awal/Default)
    original_df = predictor.get_active_df().reset_index()
    
    # Kalkulasi metrik Highest dan Lowest murni dari seluruh data asli Excel
    highest_row = original_df.loc[original_df['Gold'].idxmax()]
    lowest_row = original_df.loc[original_df['Gold'].idxmin()]

    try:
        # ==========================================
        # HANDLE FILE UPLOAD (POST REQUEST)
        # ==========================================
        if request.method == 'POST':
            uploaded_file = request.files.get('file')
            if uploaded_file and uploaded_file.filename != '':
                
                # VALIDASI EKSTENSI FILE
                allowed_extensions = {'csv', 'xlsx', 'xls'}
                file_ext = uploaded_file.filename.split('.')[-1].lower()

                if file_ext not in allowed_extensions:
                    raise ValueError("Format file tidak didukung! Gunakan .csv, .xlsx, atau .xls")

                # UPDATE FORECAST SOURCE 
                # (Mengubah state internal predictor.active_df menjadi data baru)
                predictor.set_forecast_source(uploaded_file)
                success_message = f"Berhasil melakukan forecasting menggunakan data dari file '{uploaded_file.filename}'!"

    except Exception as e:
        error_message = str(e)
        success_message = None

    # 2. HISTORICAL PREDICTION (Membaca data static training)
    historical_prediction = predictor.predict_all()

    # 3. FORECAST RESULT (Metode sekuensial berjalan di sini)
    # Jika POST -> membaca data upload. Jika GET -> membaca data asli.
    prediction = predictor.forecast()

    # 4. AMBIL DATA AKTIF UNTUK METRIK TERBARU (LATEST)
    # Diambil SETELAH proses upload agar bisa menangkap record terakhir data baru.
    active_df = predictor.get_active_df().reset_index()
    latest_row = active_df.iloc[-1]  

    # ==========================================
    # RESET TEMP DATA (KEMBALI KE STATE SEMULA)
    # ==========================================
    predictor.reset_active_data()

    # ==========================================
    # RENDER TEMPLATE (PAYLOAD PACKAGING)
    # ==========================================
    return render_template(
        'index.html',
        # Data master asli untuk grafik evaluasi dan tabel dataset training
        historical_chart_data=original_df.to_dict(orient='records'),
        data=original_df.to_dict(orient='records'), 
        highest=highest_row.to_dict(),
        lowest=lowest_row.to_dict(),
        
        # Data dinamis (bisa berubah jika user melakukan POST file baru)
        active_last_row=active_df.to_dict(orient='records'), 
        predicted=prediction,
        latest=latest_row.to_dict(), 
        
        # Hasil evaluasi model & flash messages
        historical_prediction=historical_prediction,
        error_message=error_message,
        success_message=success_message  
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)