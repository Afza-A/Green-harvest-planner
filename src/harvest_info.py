BASE_HARVEST_MONTHS = {
    "Rice": 4,
    "Wheat": 4,
    "Maize": 3,
    "Sugarcane": 12,
    "Cotton(lint)": 6,
    "Groundnut": 4,
    "Black pepper": 36,
    "Arecanut": 60,
    "Coconut": 72,
    "Banana": 12,
    "Mango": 60,
    "Grapes": 18,
    "Onion": 4,
    "Potato": 4,
    "Tomato": 3,
    "Turmeric": 8,
    "Ginger": 8,
    "Jute": 4,
    "Sesamum": 3,
    "Sunflower": 4,
    "Soyabean": 4,
    "Rapeseed &Mustard": 4,
    "Peas & beans (Pulses)": 3,
}


def get_base_harvest_months(crop):
    return BASE_HARVEST_MONTHS.get(crop, 4)


def estimate_harvest_duration(crop, rainfall, fertilizer, pesticide, area, predicted_yield):
    base_months = get_base_harvest_months(crop)

    fertilizer_per_area = fertilizer / area
    pesticide_per_area = pesticide / area

    delay = 0
    risks = []

    if rainfall < 400:
        delay += 1
        risks.append("low rainfall may slow crop growth")
    elif rainfall > 1600:
        delay += 1
        risks.append("heavy rainfall may delay harvest and increase disease risk")

    if fertilizer_per_area > 0.25:
        delay += 1
        risks.append("heavy fertilizer use may stress the soil")

    if pesticide_per_area > 0.08:
        delay += 1
        risks.append("high pesticide use may disturb field health")

    crop_risk = False

    if rainfall < 150:
        crop_risk = True
        risks.append("rainfall is extremely low, so crop survival may be difficult")

    if predicted_yield < 0.5:
        crop_risk = True
        risks.append("predicted yield is very low, so the crop may need urgent care")

    estimated_months = base_months + delay

    if crop_risk:
        status = "At Risk"
        message = (
            f"{crop} normally takes around {base_months} months, but this plan looks risky. "
            f"The crop may not reach a healthy harvest unless water, soil, and pest care are improved."
        )
    elif delay == 0:
        status = "On Time"
        message = (
            f"{crop} looks likely to be ready in about {estimated_months} months "
            f"under these conditions."
        )
    else:
        status = "Delayed"
        message = (
            f"{crop} normally takes around {base_months} months, but these conditions may push it "
            f"to about {estimated_months} months."
        )

    return {
        "base_months": base_months,
        "estimated_months": estimated_months,
        "status": status,
        "message": message,
        "risks": risks,
    }