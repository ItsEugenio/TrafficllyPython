from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List

app = FastAPI()

class TrafficData(BaseModel):
    week1: List[int] = Field(..., example=[10, 20, 30, 40, 50, 60, 70])
    week2: List[int] = Field(..., example=[15, 25, 35, 45, 55, 65, 75])

@app.post("/max_traffic_day/")
def get_max_traffic_day(data: TrafficData):
    # Validar que ambas semanas tienen 7 días
    if len(data.week1) != 7 or len(data.week2) != 7:
        return {"error": "Cada semana debe tener exactamente 7 días."}
    
    # Calcular el promedio de tráfico para cada día
    average_traffic = [(data.week1[i] + data.week2[i]) / 2 for i in range(7)]
    
    # Encontrar el día con el mayor promedio de tráfico
    max_traffic_day_index = average_traffic.index(max(average_traffic))
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    return {"day": days_of_week[max_traffic_day_index], "average_traffic": average_traffic[max_traffic_day_index]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
