import requests
from crewai.tools import tool

@tool("Useless Facts Tool")
def get_random_fact() -> str:
    """Obtiene un hecho aleatorio e inútil de internet."""
    try:
        response = requests.get(
            "https://uselessfacts.jsph.pl/api/v2/facts/random",
            params={"language": "en"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        return data.get("text", "No se pudo obtener el hecho")
    except Exception as e:
        return f"Error al obtener el hecho: {str(e)}"
