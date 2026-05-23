def get_climate_condition(rainfall):
    if rainfall < 250:
        return "Severe Drought", "Rainfall is extremely low. Crop survival may be difficult without irrigation."
    elif rainfall < 500:
        return "Drought Stress", "Low rainfall can slow growth and reduce yield."
    elif rainfall <= 1200:
        return "Comfortable Rainfall", "Rainfall looks suitable for many crop cycles."
    elif rainfall <= 1800:
        return "Heavy Rainfall", "High rainfall may increase fungal disease and drainage problems."
    else:
        return "Flood Risk", "Very high rainfall can cause waterlogging, root damage, and crop loss." 