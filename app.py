from flask import Flask, render_template, request
import os

from core.predictor import GoldPredictor

app = Flask(__name__)


DATA_PATH = os.path.join('data', 'data.xlsx')
MODEL_PATH = 'model.keras'

predictor = GoldPredictor(
    data_path=DATA_PATH,
    model_path=MODEL_PATH,
    sheet_name='dataset'
)


@app.route("/", methods=['GET', 'POST'])
def main():

    
    error_message = None
    success_message = None 

    original_df = predictor.get_active_df().reset_index()
    
    highest_row = original_df.loc[original_df['Gold'].idxmax()]
    lowest_row = original_df.loc[original_df['Gold'].idxmin()]

    try:

        if request.method == 'POST':
            uploaded_file = request.files.get('file')
            if uploaded_file and uploaded_file.filename != '':
                
                allowed_extensions = {'csv', 'xlsx', 'xls'}
                file_ext = uploaded_file.filename.split('.')[-1].lower()

                if file_ext not in allowed_extensions:
                    raise ValueError("Format file tidak didukung! Gunakan .csv, .xlsx, atau .xls")

                predictor.set_forecast_source(uploaded_file)
                success_message = f"Berhasil melakukan forecasting menggunakan data dari file '{uploaded_file.filename}'!"

    except Exception as e:
        error_message = str(e)
        success_message = None

    historical_prediction = predictor.predict_all()

    prediction = predictor.forecast()


    active_df = predictor.get_active_df().reset_index()
    latest_row = active_df.iloc[-1]  


    predictor.reset_active_data()

 
    return render_template(
        'index.html',
        historical_chart_data=original_df.to_dict(orient='records'),
        data=original_df.to_dict(orient='records'), 
        highest=highest_row.to_dict(),
        lowest=lowest_row.to_dict(),
        
        active_last_row=active_df.to_dict(orient='records'), 
        predicted=prediction,
        latest=latest_row.to_dict(), 
        
        historical_prediction=historical_prediction,
        error_message=error_message,
        success_message=success_message  
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)