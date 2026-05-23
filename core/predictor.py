# core/predictor.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model

# Impor komponen modular yang sudah kita pisahkan tadi
from core.data_cleaner import clean_and_format_data
from core.sequence_helper import create_lstm_sequences

class GoldPredictor:

    def __init__(self, data_path, model_path, sheet_name='dataset', n_steps=30):
        self.data_path = data_path
        self.model_path = model_path
        self.sheet_name = sheet_name
        self.n_steps = n_steps

        # LOAD MODEL & SCALERS
        self.model = load_model(self.model_path)
        self.scaler_X = MinMaxScaler()
        self.scaler_y = MinMaxScaler()

        # STATE MANAGEMENTS
        self.forecast_scaled_input = None
        self.active_df = None

        # BOOTSTRAP DATA LOADING
        self.load_data()
        self.prepare()

    def load_data(self):
        df = pd.read_excel(self.data_path, sheet_name=self.sheet_name)
        df.columns = df.columns.str.strip()

        if 'Periode' not in df.columns or 'Gold' not in df.columns:
            raise ValueError("Kolom wajib 'Periode' atau 'Gold' tidak ditemukan di dataset.")

        df['Periode'] = pd.to_datetime(df['Periode'], dayfirst=True, errors='coerce')
        
        # Eksekusi fungsi eksternal pembersih data
        df = clean_and_format_data(df)
        
        df = df.sort_values(by='Periode').set_index('Periode')

        self.df = df
        self.X = df
        self.y = df[['Gold']]

    def scale_data(self):
        self.X_scaled = self.scaler_X.fit_transform(self.X)
        self.y_scaled = self.scaler_y.fit_transform(self.y)

    def prepare(self):
        self.scale_data()
        if self.X_scaled.shape[0] <= self.n_steps:
            raise ValueError(f"Baris data ({self.X_scaled.shape[0]}) terlalu sedikit. Butuh > {self.n_steps}.")
        
        # Eksekusi fungsi eksternal pembuat sekuens LSTM
        self.X_seq, self.y_seq = create_lstm_sequences(self.X_scaled, self.y_scaled, self.n_steps)

    def predict_all(self):
        if len(self.X_seq) == 0:
            return {"actual": [], "predicted": []}

        preds = self.model.predict(self.X_seq)
        return {
            "actual": self.scaler_y.inverse_transform(self.y_seq).flatten().tolist(),
            "predicted": self.scaler_y.inverse_transform(preds).flatten().tolist()
        }

    def set_forecast_source(self, uploaded_file):
        filename = uploaded_file.filename.lower()
        df_new = pd.read_csv(uploaded_file, sep=';') if filename.endswith('.csv') else pd.read_excel(uploaded_file)
        
        df_new.columns = df_new.columns.str.strip()
        df_new['Periode'] = pd.to_datetime(df_new['Periode'], dayfirst=True, errors='coerce')
        
        # Eksekusi pembersihan data upload
        df_new = clean_and_format_data(df_new)
        df_new = df_new.sort_values('Periode').set_index('Periode')

        if len(df_new) < self.n_steps:
            raise ValueError(f"Data unggahan minimum harus berisi {self.n_steps} baris historis.")

        self.active_df = df_new
        scaled = self.scaler_X.transform(df_new)
        self.forecast_scaled_input = scaled[-self.n_steps:]

    def get_active_df(self):
        return self.active_df if self.active_df is not None else self.df

    def forecast(self, forecast_days=3):
        base_sequence = self.forecast_scaled_input if self.forecast_scaled_input is not None else self.X_scaled[-self.n_steps:]
        last_sequence = base_sequence.reshape(1, self.n_steps, self.X_scaled.shape[1])

        future_predictions = []
        target_index = self.df.columns.get_loc('Gold')

        for _ in range(forecast_days):
            predicted_price = self.model.predict(last_sequence)
            future_predictions.append(predicted_price[0, 0])

            new_step = last_sequence[:, -1:, :].copy()
            new_step[0, 0, target_index] = predicted_price[0, 0]
            last_sequence = np.concatenate([last_sequence[:, 1:, :], new_step], axis=1)

        self.forecast_scaled_input = None
        inverted_preds = self.scaler_y.inverse_transform(np.array(future_predictions).reshape(-1, 1))
        return inverted_preds.flatten().tolist()

    def reset_active_data(self):
        self.forecast_scaled_input = None
        self.active_df = None