import json
import requests

json_file_name = './data.json'

# Leer datos del archivo JSON
with open(json_file_name, "r", encoding="utf-8") as file:
    data = json.load(file)

# Definir función para obtener coordenadas geográficas
def get_coordinates(locate):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={locate}&key=AIzaSyDNkH7VWTtOIJ2PGnFYxCBV018pG74rGeI"
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        return None

# Agregar coordenadas a cada documento
for book in data:
    publisher_location = book['ubicacion_editorial']
    coordinates = get_coordinates(publisher_location)
    if coordinates:
        book['coordenadas_editorial'] = coordinates

# Guardar los datos actualizados en un nuevo archivo JSON
with open('data_with_coordinates.json', 'w',  encoding="utf-8") as file:
    json.dump(data, file, indent=4)