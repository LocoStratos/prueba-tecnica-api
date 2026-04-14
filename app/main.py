from fastapi import FastAPI, HTTPException
from app.services.stations import search_stations

app = FastAPI(title="Fuel Stations API")

@app.get("/")
def root():
    return {"message": "API funcionando 🚀"}

@app.get("/api/stations/search")
def search(
    lat: float,
    lng: float,
    product: str,
    nearest: bool = True,
    store: bool = False,
    cheapest: bool = False
):
    try:
        result = search_stations(lat, lng, product, nearest, store, cheapest)
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))