from typing import Dict, Annotated, List
from fastapi import FastAPI, Depends
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

import requests
import datetime
import os

app = FastAPI()

class Settings(BaseSettings):
    api_key: str = "No Key"

    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings():
    return Settings()

def kelvin_to_fahrenheit(kelvin: float) -> float:
    return round((kelvin - 273.15) * 9 / 5 + 32)

@app.get("/weather.json")
def read_root(lat: float, lon: float, settings: Annotated[Settings, Depends(get_settings)]) -> Dict[str, str]:
    today = datetime.datetime.now()
    start = today.replace(hour=0, minute=0, second=0, microsecond=0)
    end = today.replace(hour=23, minute=59, second=59, microsecond=999999)
    response = requests.get("https://api.openweathermap.org/data/2.5/weather", 
        params = {
            "lat": lat,
            "lon": lon,
            "appid": settings.api_key
        }
    )

    json: dict[str, str | dict[str, float] | List[dict[str, str]]] = response.json()
    if (json.get("main") == None):
        return {"Error": "Response Failed", "info": str(json)}
    name: str = json.get("name", "Middle of Nowhere")
    weather_icon_id: str = json.get("weather", [{}])[0].get("id", 801)

    main_section: dict[str, float] = json.get("main", {})
    temp: float = main_section.get("temp", 0.00)
    if (temp == 0.00):
        return {"Error": "Something went wrong", "Info": response.text}
    temp = kelvin_to_fahrenheit(temp)
    html = f"""<h1> Today in {name} </h1>
<div style='float: left; width: 50%'>
  <i class='owf owf-{weather_icon_id} owf-5x'></i>
</div>
<div style='float: left; width: 50%'>
  <p> Current </p>
  <h1> {temp:.1f} &deg;F </h1>
  <p>{"‎"*100}</p>
</div>
"""
    return {
        "name": "Updated Weather",
        "type": "RichText",
        "render_as": "html",
        "start_time": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "end_time": end.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "text": html
    }

