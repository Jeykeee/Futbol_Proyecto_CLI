import sys
import os
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv, find_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv(find_dotenv())

# Lee la clave de API desde las variables de entorno
API_KEY = os.getenv("API_KEY")

# Si no se encuentra la clave, muestra un error y termina
if not API_KEY:
    print("ERROR: No se encontró API_KEY. Asegúrate de que tu archivo .env contenga API_KEY=tu_token")
    exit(1)

# URL base de la API de football-data.org (versión 4)
URL_BASE = "https://api.football-data.org/v4"

# Encabezados HTTP con el token de autenticación
ENCABEZADOS = {"X-Auth-Token": API_KEY}

# Diccionario de competiciones disponibles en el plan gratuito
COMPETICIONES = {
    "WC":  "FIFA World Cup",
    "CL":  "UEFA Champions League",
    "BL1": "Bundesliga",
    "DED": "Eredivisie",
    "BSA": "Campeonato Brasileiro Série A",
    "PD":  "Primera División",
    "FL1": "Ligue 1",
    "ELC": "Championship",
    "PPL": "Primeira Liga",
    "EC":  "European Championship",
    "SA":  "Serie A",
    "PL":  "Premier League"
}


def obtener_tabla(competicion_id="PD"):
    """
    Devuelve la tabla de posiciones de una competición.
    Funciona con el plan gratuito (al menos para las competiciones listadas).

    Parámetros:
        competicion_id (str): Código de competición (ej. 'PD', 'PL'). Por defecto 'PD'.

    Retorna:
        dict o None: Diccionario con los datos de la tabla si tiene éxito, None si falla.
    """
    # Construye la URL para el endpoint de clasificación
    url = f"{URL_BASE}/competitions/{competicion_id}/standings"

    # Realiza la petición GET con los encabezados de autenticación
    respuesta = requests.get(url, headers=ENCABEZADOS)

    if respuesta.status_code == 200:
        return respuesta.json()
    else:
        print(f"Error al obtener la tabla. Código de estado = {respuesta.status_code}")
        return None


def obtener_partidos(competicion_id="PD", dias_atras=4):
    """
    Obtiene los partidos recientes de una competición.
    Por defecto, busca partidos desde 'dias_atras' días atrás hasta mañana.
    Funciona con el plan gratuito.

    Parámetros:
        competicion_id (str): Código de competición (ej. 'PD', 'PL'). Por defecto 'PD'.
        dias_atras (int): Cuántos días hacia atrás incluir. Por defecto 7.

    Retorna:
        dict o None: Diccionario con los datos de partidos si tiene éxito, None si falla.
    """
    # Calcula el rango de fechas dinámicamente
    hoy = datetime.now().date()
    desde = hoy - timedelta(days=dias_atras)
    hasta = hoy + timedelta(days=1)  # hasta mañana

    # Construye la URL con el endpoint de partidos y los filtros de fecha
    url = (f"{URL_BASE}/matches?"
           f"competitions={competicion_id}"
           f"&dateFrom={desde.isoformat()}"
           f"&dateTo={hasta.isoformat()}")

    # Realiza la petición GET con los encabezados de autenticación
    respuesta = requests.get(url, headers=ENCABEZADOS)

    if respuesta.status_code == 200:
        return respuesta.json()
    else:
        print(f"Error al obtener datos. Código de estado = {respuesta.status_code}")
        return None


if __name__ == "__main__":
    # Si el usuario pide ayuda, muestra el uso y sale
    if len(sys.argv) > 1 and sys.argv[1] in ("--help", "-h", "ayuda"):
        print("Uso: python main.py [codigo_competicion] [--tabla]")
        print("  codigo_competicion : opcional, por defecto 'PD' (La Liga)")
        print("  --tabla            : muestra la tabla de posiciones en lugar de partidos")
        print("\nCompeticiones disponibles (plan gratuito):")
        for code, name in COMPETICIONES.items():
            print(f"  {code:4s} - {name}")
        exit(0)

    # Determina si el usuario quiere la tabla de posiciones
    modo_tabla = "--tabla" in sys.argv

    # Obtiene el código de competición desde la línea de comandos
    # Ignoramos el nombre del script y cualquier bandera (--algo)
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    codigo = args[0] if args else "PD"

    # Verifica si el código es válido
    if codigo not in COMPETICIONES:
        print(f"Código de competición '{codigo}' no reconocido.")
        print("Usa --help para ver los códigos disponibles.")
        exit(1)

    # Elige la función apropiada según la bandera
    if modo_tabla:
        datos = obtener_tabla(codigo)
    else:
        datos = obtener_partidos(codigo)

    if not datos:
        # Las funciones ya imprimen el mensaje de error
        print("No se pudieron obtener los datos.")
        exit(1)

    # Procesa los datos de la respuesta
    if "matches" in datos:
        # ----- Partidos -----
        matches_list = datos["matches"]
        if matches_list:
            nombre_comp = matches_list[0]["competition"]["name"]
            print(f"Partidos recientes de: {nombre_comp}\n")
            for partido in matches_list:
                local = partido["homeTeam"]["name"]
                visitante = partido["awayTeam"]["name"]
                goles_local = partido["score"]["fullTime"]["home"] or 0
                goles_visitante = partido["score"]["fullTime"]["away"] or 0
                estado = partido["status"]
                print(f"{local} {goles_local} - {goles_visitante} {visitante} ({estado})")
        else:
            print(f"No se encontraron partidos para {codigo} en los últimos 7 días ni para mañana.")
            print("Esto puede deberse al plan gratuito o a que no hay jornada en ese rango.")
            print("Prueba con otro código o usa --tabla para ver la clasificación.")

    elif "standings" in datos:
        # ----- Tabla de posiciones -----
        nombre_comp = datos["competition"]["name"]
        print(f"Tabla de posiciones: {nombre_comp}\n")
        tabla = datos["standings"][0]["table"]
        for equipo in tabla:
            pos = equipo["position"]
            team_name = equipo["team"]["name"]
            pts = equipo["points"]
            print(f"{pos:2d}. {team_name:30s} {pts:3d} pts")

    else:
        print("La respuesta de la API no contiene ni partidos ni tabla. Revisa la documentación.")