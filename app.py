from flask import Flask
from flask import render_template
from testing import GoldPredictor

app = Flask(__name__)

@app.route("/")
def main():
    predictor = GoldPredictor('data/data.xlsx', 'model.keras', 'dataset')
    predictor.prepare()
    
    prediction = predictor.forecast()
    historical_prediction = predictor.predict_all()

    data = predictor.df.reset_index().to_dict(orient='records')

    return render_template('index.html', data=data, predicted=prediction,historical_prediction=historical_prediction)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )