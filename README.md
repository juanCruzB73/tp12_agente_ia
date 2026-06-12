# Piloto — Agente IA de Programación

Agente conversacional especializado en programación, desarrollado con Python y la API de Groq (modelo llama-3.3-70b-versatile). Trabajo Práctico N.º 12 — Sistemas Inteligentes, UDA.

## Instalación y configuración

**1. Clonar el repositorio**
```
git clone https://github.com/juanCruzB73/tp12_agente_ia
cd tp12_agente_ia
```

**2. Crear y activar el entorno virtual**
```
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
```

**3. Instalar dependencias**
```
pip install -r requirements.txt
```

**4. Configurar la API key**

Crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:
```
GROQ_API_KEY=tu_api_key_aqui
```

La API key se obtiene gratis en https://console.groq.com

**5. Ejecutar**
```
python main.py
```

## Uso

Al iniciar por primera vez, Piloto pide el nombre del usuario y genera un título para la sesión basado en la primera pregunta. En sesiones siguientes muestra las conversaciones anteriores para retomar o iniciar una nueva.

Comandos disponibles durante la conversación:
- `/salir` — termina la sesión
- `/limpiar` — borra el historial de la conversación actual

## Estructura del proyecto

```
├── main.py                        # Punto de entrada y loop principal
├── .env                           # API key (no se sube al repo)
├── requirements.txt               # Dependencias
│
├── agent/
│   └── __init__.py                # PilotoAgent: llama a la API, maneja herramientas y genera títulos
│
├── chat/
│   ├── __init__.py
│   ├── session.py                 # Carga el historial desde la BD y gestiona la conversación activa
│   └── commands.py                # Manejo de comandos /salir y /limpiar
│
├── tools/
│   ├── code_runner.py             # Herramienta: ejecuta código Python en un subprocess
│   └── doc_search.py              # Herramienta: busca documentación oficial de Python
│
├── persistance/
│   ├── __init__.py                # Exports del módulo
│   ├── user_repo.py               # Operaciones sobre la tabla user
│   ├── chat_repo.py               # Operaciones sobre la tabla chat
│   ├── message_repo.py            # Operaciones sobre la tabla message
│   ├── session_repo.py            # Operaciones sobre la tabla session
│   └── db/
│       └── db.py                  # Conexión SQLite y creación de tablas
│
└── utils/
    ├── config.py                  # Carga variables de entorno
    └── error_handler.py           # Manejo de errores de la API
```

## Etapas implementadas

| Etapa | Descripcion |
|-------|-------------|
| 1 — Conversacional basico | Conexion a la API, system prompt, historial de sesion, loop por consola |
| 2 — Personalidad y robustez | Rechazo de temas fuera de dominio, comandos /salir y /limpiar, manejo de errores de API |
| 3 — Function calling | Herramienta ejecutar_codigo y buscar_documentacion, invocadas autonomamente por el modelo |
| 4 — Persistencia | Historial guardado en SQLite, recuperacion de conversaciones previas, tracking de sesiones |
