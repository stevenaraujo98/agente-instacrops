# agente-instacrops

## Objetivo
Chatbot para conversar con agentes, que permita a un usuario (agricultor/agrónomo) consultar el estado de sus cultivos y recibir alertas inteligentes cruzando datos de:
1.  **Clima en tiempo real** (API Externa).
2.  **Sensores de campo** (Base de datos local SQLite).

## Arquitectura del proyecto
- `langgraph.json`: Configuración de LangGraph
- `.env`: Variables de entorno (API Keys)
- `README.md`: Documentación del proyecto
- `notebooks`: Notebooks de prueba
- `/src`: Lógica del agente.
- `/tests`: Pruebas unitarias

## Arquitectura (LangGraph)
1.  **Nodo Orquestador:** Recibe el input, consulta el historial y decide a qué sub-agente llamar.
2.  **Sub-agente 1 (Clima):** Usa `weatherapi`. Herramienta: `get_current_weather(lat, lon)`.
3.  **Sub-agente 2 (Sensores):** Consulta una base de datos SQLite local.
    * *Tabla:* `sensores` (id, tipo, valor, fecha, ubicacion).
    * *Herramienta:* `query_sensor_data(tipo_sensor, rango_fecha)`.
4.  **Memoria:** Implementar `MemorySaver` o `SqliteSaver` para mantener el hilo de la conversación (Checkpointer).

## Como instalarlo
### Conda y UV - Instalación de dependencias
```
conda create -n agentInstaChallenge python=3.11 openssl cryptography grpcio -y
conda activate agentInstaChallenge

conda install -c conda-forge protobuf rust pip

pip install uv

# BASE 
uv --version 

## init 
uv init 

# add dependencies 
uv add langgraph langchain langchain-openai langchain[google-genai] langchain-deepseek

# add dev dependencies
uv add "langgraph-cli[inmem]" --dev
uv add ipykernel --dev
conda install -n langgraph ipykernel --update-deps --force-reinstall
uv add grandalf --dev
uv add pytest --dev

```
```
# run the agent 
uv run langgraph dev 
```

```
[tool.setuptools.packages.find]
where = ["src"]
include = ["*"]

# recompile the project
uv pip install -e .
```

## Api clima
- WEATHER_API
Endpoint:
- http://api.weatherapi.com/v1/history.json?key={{weather_api}}&q=Guayaquil&aqi=n&dt=2025-11-30&days=2&hour=15
- http://api.weatherapi.com/v1/current.json?key={{weather_api}}&q=Guayaquil&aqi=n
- http://api.weatherapi.com/v1/forecast.json?key={{weather_api}}&q=Guayaquil&aqi=n&days=5

## Base de datos sensores
- SQLite local
- Tabla: sensores
    - id (INTEGER PRIMARY KEY AUTOINCREMENT)
    - type (TEXT) -- e.g., 'humedad_suelo', 'temperatura_suelo', 'ph_suelo'
    - value (REAL)
    - date (TEXT) -- ISO format date string
    - ubication (TEXT) -- e.g., 'Sector A', 'Sector B', 'Invernadero 1'
    - city (TEXT) -- e.g., 'Guayaquil', 'Santiago de Chile', 'Lima'

### Codigo o script para CRUD de la base de datos
Creacion de la base de datos y tabla sensores, inserción de datos de ejemplo:
Para crear la base ejecutamos el script: database/db_init.py
```
python -m database.db_init 
```

Para revisar el contenido de la base de datos ejecutamos:
```
python setup_database.py show
python setup_database.py check
```

### Estructura de la tabla sensores
```sql
CREATE TABLE sensores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    value REAL,
    date TEXT,
    ubication TEXT,
    city TEXT
);
```

#### Ejemplo de datos en la tabla sensores
```sql
INSERT INTO sensores (type, value, date, ubication, city) VALUES
('humedad_suelo', 23.5, '2025-12-10T10:00:00', 'Sector A', 'Guayaquil'),
('temperatura_suelo', 18.2, '2025-12-10T10:00:00', 'Sector A', 'Guayaquil'),
('ph_suelo', 6.5, '2025-12-10T10:00:00', 'Sector A', 'Guayaquil'),
('humedad_suelo', 25.0, '2025-12-11T10:00:00', 'Sector A', 'Guayaquil'),
('temperatura_suelo', 19.0, '2025-12-11T10:00:00', 'Sector A', 'Guayaquil'),
('ph_suelo', 6.7, '2025-12-11T10:00:00', 'Sector A', 'Guayaquil');
```

#### Ejemplo de consulta SQL para obtener datos de sensores
```sql
SELECT type, value, date, ubication
FROM sensores
WHERE type = 'humedad_suelo' AND date BETWEEN '2025-12-07' AND '2025-12-14' AND city = 'Guayaquil'
ORDER BY date ASC;
```


