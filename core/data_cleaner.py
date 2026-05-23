# core/data_cleaner.py
import pandas as pd

def clean_and_format_data(df):
    """
    Mengubah format teks Indonesia (Rp14.979,00 atau 5,28) 
    menjadi format angka standar global (14979.00 atau 5.28)
    """
    df_clean = df.copy()
    numeric_cols = ['Inflasi', 'Bunga', 'Kurs', 'Oil', 'Gold']
    
    for col in numeric_cols:
        if col in df_clean.columns:
            # 1. Pastikan tipe datanya string agar bisa dimanipulasi teksnya
            df_clean[col] = df_clean[col].astype(str)
            
            # 2. Hapus simbol mata uang dan spasi kosong
            df_clean[col] = df_clean[col].str.replace('Rp', '', regex=False)
            df_clean[col] = df_clean[col].str.replace(' ', '', regex=False)
            
            # 3. Handle penulisan desimal koma (Format ID) vs desimal titik (Format EN)
            if df_clean[col].str.contains(',').any():
                df_clean[col] = df_clean[col].str.replace('.', '', regex=False)  # Hapus titik ribuan
                df_clean[col] = df_clean[col].str.replace(',', '.', regex=False)  # Koma jadi titik desimal
            
            # 4. Cast menjadi numeric float
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
            
    return df_clean