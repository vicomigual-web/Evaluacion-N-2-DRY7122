import requests

# API Key proporcionada para OpenRouteService
api_key = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImJhNDcxZDA1N2Y0MDQ1M2VhODRmNzdlYWQ2YjY2YTQzIiwiaCI6Im11cm11cjY0In0="

while True:
    origen = input("Ingrese Ciudad Origen (o 'q' para salir): ")
    if origen.lower() == 'q':
        print("Saliendo del programa...")
        break
    
    destino = input("Ingrese Ciudad Destino (o 'q' para salir): ")
    if destino.lower() == 'q':
        print("Saliendo del programa...")
        break

    try:
        # 1. Obtener coordenadas de la Ciudad de Origen
        url_origen = f"https://api.openrouteservice.org/geocode/search?api_key={api_key}&text={origen}"
        res_origen = requests.get(url_origen).json()
        coord_origen = res_origen['features']['geometry']['coordinates']

        # 2. Obtener coordenadas de la Ciudad de Destino
        url_destino = f"https://api.openrouteservice.org/geocode/search?api_key={api_key}&text={destino}"
        res_destino = requests.get(url_destino).json()
        coord_destino = res_destino['features']['geometry']['coordinates']

        # 3. Calcular la Ruta entre ambas coordenadas
        url_ruta = f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={api_key}&start={coord_origen},{coord_origen[1]}&end={coord_destino},{coord_destino[1]}"
        res_ruta = requests.get(url_ruta).json()

        # 4. Extraer datos y realizar cálculos solicitados
        if 'features' in res_ruta:
            distancia_m = res_ruta['features']['properties']['summary']['distance']
            duracion_s = res_ruta['features']['properties']['summary']['duration']
            pasos = res_ruta['features']['properties']['segments']['steps']

            # Conversiones (km, horas/minutos/segundos y litros)
            distancia_km = distancia_m / 1000
            horas = int(duracion_s // 3600)
            minutos = int((duracion_s % 3600) // 60)
            segundos = int(duracion_s % 60)
            litros = distancia_km / 12.0  # Rendimiento referencial de 12 km por litro

            # 5. Imprimir resultados con exactamente dos decimales
            print("\n" + "="*60)
            print(f"Viaje desde {origen.title()} hasta {destino.title()}")
            print(f"Distancia: {distancia_km:.2f} kilómetros")
            print(f"Duración del viaje: {horas:02d} horas, {minutos:02d} minutos y {segundos:02d} segundos")
            print(f"Combustible requerido: {litros:.2f} litros")
            print("="*60 + "\n")

            # 6. Imprimir la narrativa del viaje
            print("--- Narrativa del viaje ---")
            for paso in pasos:
                instruccion = paso['instruction']
                dist_paso_km = paso['distance'] / 1000
                print(f"{instruccion} ({dist_paso_km:.2f} km)")
            print("="*60 + "\n")
            
        else:
            print("Error: No se pudo trazar una ruta válida entre estas ciudades.")

    except Exception:
        print("Error de conexión o las ciudades ingresadas no son válidas. Intente nuevamente.\n")