# agente-instacrops

### Arquitectura del proyecto
- main.py: Código del agente
- langgraph.json: Configuración de LangGraph
- .env: Variables de entorno (API Keys)
- README.md: Documentación del proyecto
- notebooks: Notebooks de prueba

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

# Api clima
- WEATHER_API
Endpoint:
- http://api.weatherapi.com/v1/history.json?key={{weather_api}}&q=Guayaquil&aqi=n&dt=2025-11-30&days=2&hour=15
- http://api.weatherapi.com/v1/current.json?key={{weather_api}}&q=Guayaquil&aqi=n
- http://api.weatherapi.com/v1/forecast.json?key={{weather_api}}&q=Guayaquil&aqi=n&days=5
