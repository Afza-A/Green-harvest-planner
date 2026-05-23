def calculate_sustainability_score(rainfall, fertilizer, pesticide, area):
    score = 100

    fertilizer_per_area = fertilizer / area
    pesticide_per_area = pesticide / area

    if rainfall < 300:
        score -= 35
    elif rainfall < 500:
        score -= 25
    elif rainfall > 1800:
        score -= 25
    elif rainfall > 1300:
        score -= 15

    if fertilizer_per_area > 10:
        score -= 35
    elif fertilizer_per_area > 5:
        score -= 25
    elif fertilizer_per_area > 1:
        score -= 15

    if pesticide_per_area > 1:
        score -= 40
    elif pesticide_per_area > 0.5:
        score -= 30
    elif pesticide_per_area > 0.1:
        score -= 20

    return max(score, 0)


def get_yield_category(predicted_yield):
    if predicted_yield < 1:
        return "Needs a Little Care"
    elif predicted_yield < 3:
        return "Steady Harvest"
    else:
        return "Happy Harvest"



def get_score_message(score):
    if score >= 80:
        return "Lovely balance! Your farm inputs look gentle and well planned."
    elif score >= 50:
        return "Nice start! A few small changes can make this plan even greener."
    else:
        return "This field may need extra care. Let’s tune water, fertilizer, and pest control wisely."

def get_recommendations(rainfall, fertilizer, pesticide, area, predicted_yield):
    recommendations = []

    fertilizer_per_area = fertilizer / area
    pesticide_per_area = pesticide / area

    if rainfall < 500:
        recommendations.append(
            "The field looks a bit thirsty. Plan careful irrigation, drip watering, or rainwater harvesting."
        )
    elif rainfall > 1200:
        recommendations.append(
            "There is plenty of rain here. Keep an eye on drainage and protect the crop from fungal trouble."
        )
    else:
        recommendations.append(
            "Rainfall looks friendly. A regular irrigation schedule should keep the crop comfortable."
        )

    if fertilizer_per_area > 0.2:
        recommendations.append(
            "Fertilizer use is on the heavier side. A soil test can help feed the crop without tiring the soil."
        )
    else:
        recommendations.append(
            "Fertilizer use looks calm and balanced for this area."
        )

    if pesticide_per_area > 0.05:
        recommendations.append(
            "Pesticide use feels a little strong. Try neem-based sprays, trap crops, or integrated pest management."
        )
    else:
        recommendations.append(
            "Pesticide use looks light. That is a kinder choice for soil, water, and helpful insects."
        )

    if predicted_yield < 1:
        recommendations.append(
            "The harvest may be modest. Better water timing, soil nutrition, and crop monitoring can help."
        )
    elif predicted_yield < 3:
        recommendations.append(
            "The harvest looks steady. Fine-tuning irrigation and nutrients may lift it further."
        )
    else:
        recommendations.append(
            "The harvest forecast looks cheerful. Keep following balanced farming practices."
        )

    return recommendations 
