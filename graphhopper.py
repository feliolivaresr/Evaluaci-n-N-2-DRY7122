import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "53847bad-fa1b-4895-8c37-2d1131e97d65"  # Reemplaza por tu clave real si es necesario

def geocoding(location, key):
    while location == "":
        location = input("Ingresa la ubicación nuevamente: ")
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code

    if json_status == 200 and len(json_data["hits"]) != 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        country = json_data["hits"][0].get("country", "")
        state = json_data["hits"][0].get("state", "")
        new_loc = f"{name}, {state}, {country}" if state and country else f"{name}, {country}"
    else:
        lat = "null"
        lng = "null"
        new_loc = location
        print("Error al geocodificar:", json_data.get("message", "Respuesta inválida"))
    return json_status, lat, lng, new_loc

def calcular_combustible(dist_km, eficiencia_km_l=12):
    return round(dist_km / eficiencia_km_l, 2)

while True:
    print("\n================ VIAJE ENTRE CIUDADES =================")
    origen = input("Ciudad de Origen (o 'q' para salir): ")
    if origen.lower() in ['q', 'quit']:
        break
    destino = input("Ciudad de Destino (o 'q' para salir): ")
    if destino.lower() in ['q', 'quit']:
        break

    orig = geocoding(origen, key)
    dest = geocoding(destino, key)

    if orig[0] == 200 and dest[0] == 200:
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
        full_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": "car"}) + op + dp

        response = requests.get(full_url)
        if response.status_code == 200:
            data = response.json()
            path = data["paths"][0]
            dist_km = round(path["distance"] / 1000, 2)
            time_ms = path["time"]
            hrs = int(time_ms / 1000 / 60 / 60)
            mins = int((time_ms / 1000 / 60) % 60)
            secs = int((time_ms / 1000) % 60)
            litros = calcular_combustible(dist_km)

            print("\n================ RESULTADO DEL VIAJE =================")
            print(f"Desde: {orig[3]}")
            print(f"Hasta: {dest[3]}")
            print(f"Distancia: {dist_km:.2f} km")
            print(f"Duración: {hrs:02d}:{mins:02d}:{secs:02d} (hh:mm:ss)")
            print(f"Combustible estimado requerido: {litros:.2f} litros")
            print("\n================ NARRATIVA DEL VIAJE =================")
            for step in path["instructions"]:
                texto = step["text"]
                distancia = step["distance"] / 1000
                print(f"{texto} ({distancia:.2f} km)")
            print("======================================================\n")
        else:
            print("Error en la API de rutas:", response.json().get("message", "Respuesta inválida"))
    else:
        print("No se pudo obtener la información geográfica correctamente.")
