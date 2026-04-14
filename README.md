# Prueba Técnica: API de Búsqueda de Estaciones de Combustible

API REST desarrollada en Python la cual permite buscar estaciones de combustible en Chile en base a la ubicación geográfica y filtrar por cercanía, precio y disponibilidad de tienda.

Decisiones Técnicas
implemente la formula haversine para calcular las distancias greograficas, al igual que se normalizaron los productos para facilitar la busqueda al igual que el manejo de excepciones para controlar las respuestas. 

⚠️ Consideraciones y limitaciones
La api utilizada no siempre presenta el campo "marca", por lo que el nombre de las compañias puede que no sea exacto en todos los casos
 No se dispone de información detallada sobre tiendas (codigo, nombre,tipo) por lo que la mayoria de las veces lo devolvio como null
 a fecha 14/04 sigo trabajando para ver como obtener esos datos sin tener que forzarlos.
---

## Tecnologías utilizadas

- Python 3.13
- FastAPI
- Uvicorn
- Requests

---

## Fuente de datos

Se utilizo la API encontrada en la pagina de https://www.bencinaenlinea.cl/ luego de inspeccionar la pagina, los criterios usados para seleccionarla fue su peso(kb) con respecto a las otras presentes, además del metodo que presentaba.

https://api.bencinaenlinea.cl/api/busqueda_estacion_filtro

---

## ⚙️ Instalación y ejecución

1. Clonar el repositorio

```bash
git clone https://github.com/LocoStratos/prueba-tecnica-api.git
cd prueba-tecnica-api

2. Crear el entorno virtual (opcional)
python -m venv venv
venv\Scripts\activate   # Windows

3. instalar dependencias (muy importante, sino no funciona)
pip install -r requirements.txt

4. Ejecutar la API
python -m uvicorn app.main:app --reload

5. Abrir en el navegador
http://127.0.0.1:8000 #igualmente en la terminal aparecera el link

6. Buscar estaciones
GET /api/stations/search

Parametros que maneja la api
| Parámetro | Tipo   | Descripción                                        |
| --------- | ------ | -------------------------------------------------- |
| lat       | float  | Latitud                                            |
| lng       | float  | Longitud                                           |
| product   | string | Tipo de combustible (93, 95, 97, diesel, kerosene) |
| nearest   | bool   | Buscar la más cercana                              |
| store     | bool   | Filtrar por estaciones con tienda                  |
| cheapest  | bool   | Buscar menor precio                                |

---

Ejemplo de uso 
http://127.0.0.1:8000/api/stations/search?lat=-33.45&lng=-70.6&product=93&nearest=true

Respuesta 
{
  "success": true,
  "data": {
    "id": "1804",
    "compania": "Terpel",
    "direccion": "Avenida Pedro de Valdivia 3014",
    "comuna": "Ñuñoa",
    "region": "Metropolitana de Santiago",
    "latitud": -33.4501,
    "longitud": -70.6051,
    "distancia(lineal)": 0.479,
    "precios93": 1516,
    "tienda": {
      "codigo": null,
      "nombre": null,
      "tipo": null
    },
    "tiene_tienda": true
  }
}
---
