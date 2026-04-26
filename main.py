import os
import requests
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Read the API key from the environment
API_KEY = os.getenv("API_KEY")

# Exit if the API key is not found
if not API_KEY:
    print("ERROR: API_KEY not found. Make sure your .env file contains API_KEY=your_token")
    exit(1)

# Base URL for the football-data.org API (version 4)
URL_BASE = "https://api.football-data.org/v4"

# HTTP headers with the authentication token
ENCABEZADOS = {"X-Auth-Token": API_KEY}


def obtener_tabla(competicion_id="PD"):
    """
    Returns the standings table for a given competition.
    WARNING: This endpoint is NOT available on the Free plan.
    You will receive a 403 Forbidden error.
    Keep this function for future use with a suitable API key or plan.

    Parameters:
        competicion_id (str): Competition code (e.g., 'PD', 'PL'). Default 'PD'.

    Returns:
        dict or None: Dictionary with standings data if successful, None on error.
    """
    # Build the URL for the standings endpoint
    url = f"{URL_BASE}/competitions/{competicion_id}/standings"

    # Make the GET request with the authentication headers
    respuesta = requests.get(url, headers=ENCABEZADOS)

    if respuesta.status_code == 200:
        return respuesta.json()
    else:
        print(f"Error fetching standings data. Status code = {respuesta.status_code}")
        return None


def obtener_partidos(competicion_id="PD"):
    """
    Fetches recent matches for a given competition.
    Works with the Free plan.

    Parameters:
        competicion_id (str): Competition code (e.g., 'PD', 'PL'). Default 'PD'.

    Returns:
        dict or None: Dictionary with matches data if successful, None on error.
    """
    # Build the URL for the matches endpoint
    url = f"{URL_BASE}/matches?competitions={competicion_id}"

    # Make the GET request with authentication headers
    respuesta = requests.get(url, headers=ENCABEZADOS)

    if respuesta.status_code == 200:
        return respuesta.json()
    else:
        print(f"Error fetching data. Status code = {respuesta.status_code}")
        return None


if __name__ == "__main__":
    # =========================================================
    # Change this line to switch between functions:
    #   - obtener_partidos("PD")   -> Shows recent matches (works with Free plan)
    #   - obtener_tabla("PD")      -> Shows standings (requires Tier One or higher)
    # =========================================================
    datos = obtener_partidos("PD")

    if datos:
        # Check if the response contains matches
        if "matches" in datos and datos["matches"]:
            # Extract competition name from the first match
            # (each match contains its own 'competition' object)
            nombre_comp = datos["matches"][0]["competition"]["name"]
            print(f"Recent matches for: {nombre_comp}\n")

            for partido in datos["matches"]:
                local = partido["homeTeam"]["name"]
                visitante = partido["awayTeam"]["name"]
                goles_local = partido["score"]["fullTime"]["home"] or 0
                goles_visitante = partido["score"]["fullTime"]["away"] or 0
                estado = partido["status"]
                print(f"{local} {goles_local} - {goles_visitante} {visitante} ({estado})")
        else:
            print("No matches found in the response.")

        # If you use obtener_tabla in the future, the code for 'standings' will go here
        # elif "standings" in datos: ...
    else:
        print("Could not fetch the data.")