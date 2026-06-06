# 🤖 Piloto — Agente IA de Programación

## 📁 Estructura del proyecto

```
agente/
│
├── main.py                   # Punto de entrada, loop principal
├── .env                      # API key (gitignoreado)
├── .env.example              # Plantilla sin valores reales (sí va al repo)
├── requirements.txt          # Dependencias del proyecto
├── README.md
│
├── agent/
│   ├── __init__.py
│   ├── piloto.py             # Orquestador: une todo, decide qué hacer
│   └── prompts.py            # System prompt y constantes de texto
│
├── chat/
│   ├── __init__.py
│   ├── session.py            # Historial en memoria, add_message, clear
│   └── commands.py           # /salir, /limpiar, /historial, etc.
│
├── tools/
│   ├── __init__.py
│   ├── registry.py           # Lista de tools que se pasan a la API
│   ├── executor.py           # Despacha la tool_call al handler correcto
│   ├── code_runner.py        # Herramienta: ejecutar código Python (sandbox)
│   └── doc_search.py         # Herramienta: buscar docs / explicar función
│
├── persistance/
│  ├── __init__.py          # exports de todo el módulo
│  ├── user_repo.py         # create_user, get_user, get_or_create_user
│  ├── chat_repo.py         # create_chat, list_chats, get_chat, update_chat_title, delete_chat
│  ├── message_repo.py      # save_message, get_messages, delete_messages
│  ├── session_repo.py      # start_session, end_session, get_session, list_sessions
│  └── db/
│      └── db.py            # get_connection(), init_db() + schema SQL
│
└── utils/
    ├── __init__.py
    ├── config.py             # Carga .env, expone settings
    └── error_handler.py      # Manejo de excepciones de la API
```

utils/config.py — carga el .env
agent/prompts.py — el system prompt de Piloto
chat/session.py — el historial
agent/piloto.py — el orquestador que llama a la API
main.py — el loop de consola
