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

            df_clean[col] = df_clean[col].astype(str)
            
            # 2. Hapus simbol mata uang dan spasi kosong
            df_clean[col] = df_clean[col].str.replace('Rp', '', regex=False)
            df_clean[col] = df_clean[col].str.replace(' ', '', regex=False)       

            if df_clean[col].str.contains(',').any():
                df_clean[col] = df_clean[col].str.replace('.', '', regex=False)
                df_clean[col] = df_clean[col].str.replace(',', '.', regex=False)
            
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
            
    return df_clean