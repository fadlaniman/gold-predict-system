import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model


class GoldPredictor:

    def __init__(
        self,
        data_path,
        model_path,
        sheet_name='dataset',
        n_steps=30
    ):

        self.data_path = data_path
        self.model_path = model_path
        self.sheet_name = sheet_name
        self.n_steps = n_steps

        self.scaler_X = MinMaxScaler()
        self.scaler_y = MinMaxScaler()

        self.model = load_model(self.model_path)

        self.load_data()


    # =========================
    # LOAD DATA
    # =========================
    def load_data(self):

        df = pd.read_excel(
            self.data_path,
            sheet_name=self.sheet_name
        )

        df['Periode'] = pd.to_datetime(df['Periode'])
        df = df.sort_values(by='Periode')
        df.set_index('Periode', inplace=True)

        self.df = df
        self.X = df
        self.y = df[['Gold']]


    # =========================
    # SCALE DATA
    # =========================
    def scale_data(self):

        self.X_scaled = self.scaler_X.fit_transform(self.X)
        self.y_scaled = self.scaler_y.fit_transform(self.y)


    # =========================
    # CREATE SEQUENCE
    # =========================
    def create_sequence(self):

        X_seq = []
        y_seq = []

        for i in range(len(self.X_scaled) - self.n_steps):

            X_seq.append(
                self.X_scaled[i:i + self.n_steps]
            )

            y_seq.append(
                self.y_scaled[i + self.n_steps]
            )

        self.X_seq = np.array(X_seq)
        self.y_seq = np.array(y_seq)


    # =========================
    # PREPARE DATA
    # =========================
    def prepare(self):

        self.scale_data()
        self.create_sequence()


    # =========================
    # PREDICT ALL DATA
    # =========================
    def predict_all(self):

        predictions = self.model.predict(self.X_seq)

        predictions = self.scaler_y.inverse_transform(predictions)

        actual = self.scaler_y.inverse_transform(
            self.y_seq.reshape(-1, 1)
        )

        return {
            'actual': actual.flatten().tolist(),
            'predicted': predictions.flatten().tolist()
        }


    # =========================
    # GET LAST SEQUENCE
    # =========================
    def get_last_sequence(self):

        return self.X_scaled[-self.n_steps:].reshape(
            1,
            self.n_steps,
            self.X_scaled.shape[1]
        )


    # =========================
    # FORECAST FUTURE
    # =========================
    def forecast(self, forecast_days=3):

        last_sequence = self.get_last_sequence()

        future_predictions = []

        target_index = self.df.columns.get_loc('Gold')

        for _ in range(forecast_days):

            predicted_price = self.model.predict(last_sequence)

            future_predictions.append(predicted_price[0, 0])

            new_step = last_sequence[:, -1:, :].copy()

            # update only GOLD column
            new_step[0, 0, target_index] = predicted_price[0, 0]

            # shift window
            last_sequence = np.concatenate(
                [last_sequence[:, 1:, :], new_step],
                axis=1
            )

        # inverse scaling
        future_predictions = self.scaler_y.inverse_transform(
            np.array(future_predictions).reshape(-1, 1)
        )

        return future_predictions.flatten().tolist()