import requests
from app.utils.distance import haversine

API_URL = "https://api.bencinaenlinea.cl/api/busqueda_estacion_filtro" #Asumiré que esta es la api correcta
BRANDS = {
    1: "COPEC",
    2: "Shell",
    3: "Petrobras",
    4: "Terpel"
}


def normalize_product(product: str):
    mapping = {
        "93": "93",
        "95": "95",
        "97": "97",
        "diesel": "diesel",
        "kerosene": "kerosene",
        "glp": "GLP"
    }
    return mapping.get(product.lower())

def get_data():
    response = requests.get(API_URL)
    if response.status_code != 200:
        raise Exception("Error al obtener datos externos")
    
    return response.json()["data"]

def search_stations(lat, lng, product, nearest, store, cheapest):
    data = get_data()
    product_name = normalize_product(product)

    if not product_name:
        raise Exception("Producto inválido")

    stations = []

    for station in data:
        try:
            station_lat = float(station["latitud"])
            station_lng = float(station["longitud"])

            distance = haversine(lat, lng, station_lat, station_lng)

            # Precio del producto
            price = None

            for p in station.get("combustibles", []):
                nombre = (
                    p.get("nombre_corto", "") + " " + p.get("nombre_largo", "")
                ).lower()

                if product_name in nombre:
                    try:
                        price = int(float(p["precio"]))
                        break
                    except:
                        continue
            print("Combustibles:", station.get("combustibles", []))

            if price is None:
                continue

            #has_store = True  #Sino tenemos info, se documenta.
            has_store = len(station.get("servicios", [])) > 0

            # Filtro por tienda
            if store and not has_store:
                continue
            
            tienda_info = {
                            "codigo": None,
                            "nombre": None,
                            "tipo": None
            }

            brand = BRANDS.get(station.get("marca"), f"Marca ID {station.get('marca')}")
            stations.append({
                "id": str(station["id"]),
                #"id": station["id"],
                "compania": brand,
                #"compania": BRANDS.get(station.get("marca"), "Desconocida"),
                #"compania": str(station.get("marca")),
                #"compania": station["marca"], de esta manera me los devolvia por el id y no por el nombre.
                "direccion": station["direccion"],
                "comuna": station["comuna"],
                "region": station["region"],
                "latitud": station_lat,
                "longitud": station_lng,
                "distancia(lineal)": round(distance, 3),
                #"distancia": round(distance, 3),
                #"distancia": distance,
                #"precio": price,
                f"precios{product_name}": price,
                "tienda": tienda_info,
                "tiene_tienda": has_store,
            })

        except:
            continue

    if not stations:
        raise Exception("No se encontraron estaciones")

    # Orden
    #if cheapest and nearest:
        stations.sort(key=lambda x: (x["precio"], x["distancia"]))
    #elif cheapest:
        stations.sort(key=lambda x: x["precio"])
    #else:
        stations.sort(key=lambda x: x["distancia"])
    if cheapest and nearest:
        stations.sort(key=lambda x: (x[f"precios{product_name}"], x["distancia(lineal)"]))
    elif cheapest:
        stations.sort(key=lambda x: x[f"precios{product_name}"])
    else:
        stations.sort(key=lambda x: x["distancia(lineal)"])
    return stations[0]
