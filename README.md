# Futbol Proyecto CLI

Aplicacion de linea de comandos (CLI) escrita en Python para consultar
partidos recientes y tablas de posiciones de las principales ligas de
futbol. Obtiene los datos en tiempo real desde la API de football-data.org
con su plan gratuito.

## Funcionalidades

- Partidos recientes: muestra los partidos disputados en los ultimos 7
  dias y los programados para el dia siguiente.
- Tabla de posiciones: consulta la clasificacion actualizada usando la
  bandera --tabla.
- 12 competiciones disponibles: La Liga, Premier League, Champions League,
  Bundesliga, Serie A y mas.
- Totalmente desde la terminal: elige la liga y el modo sin salir de la
  consola.

## Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalacion

Clona el repositorio:

git clone https://github.com/TU_USUARIO/Futbol-Proyecto-cli.git
cd Futbol-Proyecto-cli

Crea y activa un entorno virtual (opcional pero recomendado):

python -m venv venv
source venv/Scripts/activate      # En Windows con Git Bash

Instala las dependencias:

pip install -r requerimientos.txt

## Configuracion de la API Key

1. Registrate gratis en football-data.org (https://www.football-data.org/).
2. Copia tu API Key del dashboard.
3. Crea un archivo .env en la raiz del proyecto con este contenido:

API_KEY=TU_CLAVE_AQUI

Tambien puedes copiar la plantilla:

cp .env.ejemplo .env

Luego edita .env y pega tu clave real.

## Uso

# Partidos recientes de La Liga (por defecto)
python main.py

# Partidos recientes de la Premier League
python main.py PL

# Tabla de posiciones de la Bundesliga
python main.py BL1 --tabla

# Tabla de posiciones de La Liga
python main.py --tabla

# Ver todos los comandos y codigos disponibles
python main.py --help

## Competiciones disponibles (plan gratuito)

| Codigo | Competicion                    |
|--------|--------------------------------|
| WC     | FIFA World Cup                 |
| CL     | UEFA Champions League          |
| BL1    | Bundesliga                     |
| DED    | Eredivisie                     |
| BSA    | Campeonato Brasileiro Serie A  |
| PD     | Primera Division (La Liga)     |
| FL1    | Ligue 1                        |
| ELC    | Championship                   |
| PPL    | Primeira Liga                  |
| EC     | European Championship          |
| SA     | Serie A                        |
| PL     | Premier League                 |

## Tecnologias utilizadas

- Python 3
- requests (https://pypi.org/project/requests/) - peticiones HTTP
- python-dotenv (https://pypi.org/project/python-dotenv/) - manejo de
  variables de entorno
- API REST de football-data.org v4 (https://www.football-data.org/)

## Estructura del proyecto

Futbol-Proyecto-cli/
├── main.py               # Codigo principal del CLI
├── requerimientos.txt     # Dependencias Python
├── .env.ejemplo           # Plantilla para la API Key (sin secretos)
├── .gitignore             # Archivos ignorados por Git
└── README.md              # Documentacion del proyecto

## Notas

- El plan gratuito de football-data.org tiene un limite de 10 peticiones
  por minuto.
- Los partidos mostrados abarcan 7 dias hacia atras y 1 dia hacia
  adelante.
- Si una competicion no tiene partidos en esa ventana, el programa
  mostrara un mensaje informativo en lugar de fallar.
- La tabla de posiciones funciona para todas las competiciones listadas
  arriba.

## Autor

Joel - https://github.com/TU_USUARIO

---

Este proyecto forma parte de un portafolio de aprendizaje en Python,
consumo de APIs REST y buenas practicas con Git.
