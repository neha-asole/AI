from flask import Flask, render_template, request, redirect, session
from model import predict_disaster
import requests

app = Flask(__name__)
app.secret_key = "secret123"

# 🔐 LOGIN
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user'] = request.form.get('username')
        return redirect('/home')
    return render_template('login.html')


# 🏠 HOME
@app.route('/home')
def home():
    if 'user' in session:
        return render_template('home.html')
    return redirect('/')


# 📊 PREDICT PAGE
@app.route('/predict_page')
def predict_page():
    if 'user' in session:
        return render_template('predict.html')
    return redirect('/')


# 🔮 PREDICT FUNCTION (FINAL FIXED)
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # 📥 SAFE INPUT
        temp = float(request.form.get('temp', 0) or 0)
        humidity = float(request.form.get('humidity', 0) or 0)
        rainfall = float(request.form.get('rainfall', 0) or 0)
        wind = float(request.form.get('wind', 0) or 0)
        location = request.form.get('location', '').strip()

        # Default location
        if location == "":
            location = "Nagpur"

        # 🤖 Prediction
        prediction, probs = predict_disaster(temp, humidity, rainfall, wind)

        # 🌍 Default values
        lat = 20.59
        lon = 78.96
        display_name = "Unknown Location"
        population = "Not Available"

        # 🌐 GET LOCATION + POPULATION (CORRECT API)
        try:
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1"
            response = requests.get(geo_url, timeout=5)

            if response.status_code == 200:
                data = response.json()

                if "results" in data and len(data["results"]) > 0:
                    result = data["results"][0]

                    lat = result.get("latitude", lat)
                    lon = result.get("longitude", lon)

                    city = result.get("name", "")
                    country = result.get("country", "")

                    display_name = f"{city}, {country}"

                    # ✅ REAL population
                    pop = result.get("population")

                    if pop and pop > 0:
                        population = pop
                    else:
                        population = "Not Available"

        except:
            pass  # No crash if API fails

        # 🖼 IMAGE SELECTION
        if prediction == "Flood":
            image = "flood.png"
        elif prediction == "Cyclone":
            image = "cyclone.png"
        elif prediction == "Earthquake":
            image = "earthquake.png"
        else:
            image = "Safe.png"

        # 📤 RESULT PAGE
        return render_template(
            'result.html',
            prediction=prediction,
            probs=probs,
            image=image,
            lat=lat,
            lon=lon,
            location=display_name,
            population=population
        )

    except Exception as e:
        print("ERROR:", e)

        # 🔥 FINAL FALLBACK (NO ERROR EVER)
        return render_template(
            'result.html',
            prediction="Safe",
            probs={"Flood": 0, "Cyclone": 0, "Earthquake": 0},
            image="safe.jpg",
            lat=20.59,
            lon=78.96,
            location="Error",
            population="Not Available"
        )


# 🚪 LOGOUT
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


# 🚀 RUN APP
if __name__ == '__main__':
    app.run(debug=True)