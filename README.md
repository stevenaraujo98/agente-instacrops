# 🌾 Agente Instacrops: Asistente Agrícola Inteligente

## 📋 Objetivo
Este proyecto implementa un **Chatbot Orquestador** diseñado para asistir a agricultores y agrónomos. El sistema cruza datos en tiempo real para ofrecer alertas inteligentes sobre el estado de los cultivos, integrando:
1.  **Clima en tiempo real** (API Externa).
2.  **Sensores de campo** (Base de datos local SQLite).

---

## 🏗️ Arquitectura del Proyecto

### Estructura de Directorios
```bash
/agente-instacrops
├── langgraph.json       # Configuración del grafo
├── .env                 # Variables de entorno (API Keys)
├── setup_database.py    # Script de gestión de DB
├── database/            # Scripts SQL y de inicialización
├── notebooks/           # Pruebas exploratorias
├── src/                 # Código fuente principal
│   ├── agents/          # Lógica de Agentes y Sub-agentes
│   └── ui/              # Interfaz de usuario (Streamlit)
└── tests/               # Pruebas unitarias
```

## Flujo de LangGraph (Lógica)
1.  **Nodo Orquestador:** Recibe el input, consulta el historial y decide a qué sub-agente llamar.
2.  **Sub-agente 1 (Clima):** Usa `weatherapi`. Herramienta: `get_current_weather(lat, lon)`.
3.  **Sub-agente 2 (Sensores):** Consulta una base de datos SQLite local.
    * *Tabla:* `sensores` (id, tipo, valor, fecha, ubicacion).
    * *Herramienta:* `query_sensor_data(tipo_sensor, ciudad, rango_fecha)`.
4.  **Memoria:** Mantiene el estado y contexto de la conversación entre turnos.

## Modelos que se utilizan:
1. gpt-5-nano: en el agente extractor de información estructurada .
2. gpt-4o-mini: en el agente sensor worker y weather worker.
3. gpt-5-mini: en el agente ruteador.

## Instalación y Configuración
Pasos para levantar el entorno de desarrollo usando Conda y UV.

1. Preparar el Entorno (Conda)
```bash
conda create -n agentInstaChallenge python=3.11 openssl cryptography grpcio -y
conda activate agentInstaChallenge

# Instalar dependencias base del sistema
conda install -c conda-forge protobuf rust pip
```

2. Gestión de Dependencias (UV)
```bash
# Inicializar UV e instalar dependencias del proyecto
pip install uv
uv init
uv --version

# Dependencias principales
uv add langgraph langchain langchain-openai langchain[google-genai] langchain-deepseek
uv add streamlit

# Dependencias de desarrollo
uv add "langgraph-cli[inmem]" --dev
uv add ipykernel grandalf pytest --dev

# Reinstalar ipykernel para compatibilidad con Conda
conda install -n langgraph ipykernel --update-deps --force-reinstall

# Instalar el proyecto en modo editable
uv pip install -e .
```

## Base de Datos (Sensores)
El proyecto utiliza SQLite para simular datos de sensores históricos.  

Inicialización  
Ejecuta el script para crear la tabla y poblarla con datos de prueba (database/db_init.py):
```
python -m database.db_init 
```


Verificación  
Para validar que los datos se cargaron correctamente:
```
python setup_database.py show
python setup_database.py check
```


## Ejecución
1. Interfaz de Usuario (Recomendado)
Para iniciar el Chatbot en el navegador:
```bash
uv run streamlit run src/ui/app.py
```

2. Servidor de Desarrollo LangGraph
Para depurar el flujo del agente:
```bash
uv run langgraph dev
```

3. recompile the project
```bash
uv pip install -e .
```

## Referencia Técnica
### Api clima
Endpoints configurados para la consulta de datos:
- Histórico: /history.json (dt, location)
- Actual: /current.json (location, aqi)
- Pronóstico: /forecast.json (days, location)

### Modelo de Datos (SQLite)
```sql
CREATE TABLE sensores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,      -- Ej: 'humedad_suelo', 'ph_suelo'
    value REAL,     -- Valor numérico
    date TEXT,      -- Formato ISO
    ubication TEXT, -- Ej: 'Sector A'
    city TEXT       -- Ej: 'Guayaquil'
);
```

### Ejemplo de Consulta SQL (Tool):
```sql
SELECT type, value, date, ubication
FROM sensores
WHERE type = 'humedad_suelo'
  AND date BETWEEN '2025-12-07' AND '2025-12-14'
  AND city = 'Guayaquil'
ORDER BY date ASC;
```


