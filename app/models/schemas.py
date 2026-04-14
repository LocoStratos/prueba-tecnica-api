from pydantic import BaseModel

class StationResponse(BaseModel):
    id: str
    compania: str
    direccion: str
    comuna: str
    region: str
    latitud: float
    longitud: float
    distancia: float
    precio: int
    tiene_tienda: bool