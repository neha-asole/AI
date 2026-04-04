def predict_disaster(temp, humidity, rainfall, wind_speed):
    # Avoid zero values (IMPORTANT FIX)
    humidity = max(humidity, 1)
    rainfall = max(rainfall, 1)
    wind_speed = max(wind_speed, 1)

    P_flood = 0.3
    P_cyclone = 0.2
    P_earthquake = 0.1

    flood_prob = P_flood * (rainfall / 100) * (humidity / 100)
    cyclone_prob = P_cyclone * (wind_speed / 100) * (humidity / 100)
    earthquake_prob = P_earthquake * (1 - rainfall / 100)

    total = flood_prob + cyclone_prob + earthquake_prob

    # 🔥 Safety check
    if total == 0:
        return "Safe", {"Flood": 0, "Cyclone": 0, "Earthquake": 0}

    flood_prob /= total
    cyclone_prob /= total
    earthquake_prob /= total

    result = {
        "Flood": round(flood_prob, 2),
        "Cyclone": round(cyclone_prob, 2),
        "Earthquake": round(earthquake_prob, 2)
    }

    prediction = max(result, key=result.get)

    # ✅ SAFE condition
    if result[prediction] < 0.4:
        prediction = "Safe"

    return prediction, result