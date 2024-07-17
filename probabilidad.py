from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
import numpy as np
import scipy.stats as stats

app = FastAPI()

class TrafficData(BaseModel):
    week1: List[int] = Field(..., example=[10, 20, 30, 40, 50, 60, 70])
    week2: List[int] = Field(..., example=[15, 25, 35, 45, 55, 65, 75])

@app.post("/max_traffic_day/")
def get_prob_max_traffic_day(data: TrafficData):
    # Validar que ambas semanas tienen 7 días
    if len(data.week1) != 7 or len(data.week2) != 7:
        return {"error": "Cada semana debe tener exactamente 7 días."}
    
    means = [(data.week1[i] + data.week2[i]) / 2 for i in range(7)]
    variances = [((data.week1[i] - means[i])**2 + (data.week2[i] - means[i])**2) / 2 for i in range(7)]
    
    probabilities = [0] * 7
    for i in range(7):
        total_probability = 1
        for j in range(7):
            if i != j:
                # Manejar el caso donde la varianza es cero
                if variances[i] == 0 and variances[j] == 0:
                    prob_ij = 0.5 if means[i] == means[j] else (1 if means[i] > means[j] else 0)
                else:
                    prob_ij = stats.norm.cdf(0, loc=means[i] - means[j], scale=np.sqrt(variances[i] + variances[j]))
                total_probability *= prob_ij
        probabilities[i] = total_probability
    
    days_of_week = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
    max_prob_day_index = probabilities.index(max(probabilities))
    
    return {
        "day": days_of_week[max_prob_day_index],
        "probability": probabilities[max_prob_day_index],
        "probabilities": {days_of_week[i]: probabilities[i] for i in range(7)}
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
