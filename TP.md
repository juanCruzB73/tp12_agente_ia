Trabajo Práctico de Evaluación N.º 12

Desarrollo de un Agente de IA

a) Objetivo
Diseñar e implementar un agente de IA funcional utilizando Python y la API de Claude (Anthropic), Gemini, ChatGPT, Groq, etc, aplicando los conceptos de agentes inteligentes, programas inteligentes y sistemas de procesamiento del lenguaje natural desarrollados a lo largo de la materia.

Al finalizar el TP, el grupo habrá construido un sistema conversacional capaz de mantener contexto, especializarse en un dominio, ejecutar acciones reales mediante herramientas y —opcionalmente— persistir información entre sesiones.

b) Producto tangible
El grupo entrega los siguientes artefactos:

• Código fuente completo del agente en Python (repositorio GitHub o carpeta comprimida .zip)

• Archivo README.md con instrucciones claras de instalación, configuración de la API key y ejecución

• Informe técnico en PDF que documente: decisiones de diseño, arquitectura del agente, dificultades encontradas y conclusiones

• Demo en vivo de 5 a 10 minutos durante la clase de entrega

c) Dominio de aplicación
Cada grupo define libremente el dominio de su agente. El dominio determina la personalidad, el conocimiento especializado y las herramientas que el agente va a usar. Algunos ejemplos:

Dominio

Descripción del agente

Asistente académico

Responde consultas sobre materias, ayuda a estudiar, genera preguntas de repaso

Atención al cliente

Atiende consultas, gestiona reclamos, verifica estado de pedidos

Tutor de programación

Explica conceptos, revisa código, sugiere correcciones

Asistente gastronómico

Sugiere recetas, calcula porciones, adapta a restricciones alimentarias

Asesor financiero básico

Calcula intereses, convierte monedas, explica conceptos financieros

Asistente de salud

Responde dudas generales de salud, sugiere turnos, explica estudios

💡 El dominio elegido debe ser coherente con las herramientas implementadas en la Etapa 3. Cuanto más específico es el dominio, más interesante y evaluable resulta el agente.

d) Etapas acumulativas
El TP se desarrolla en cuatro etapas. Cada etapa suma funcionalidad al agente construido en la etapa anterior. La nota final depende de cuántas etapas se completan correctamente.

ℹ️ Cada etapa es autosuficiente: un agente que llega hasta la Etapa 3 es completamente funcional y digno de presentar. La Etapa 4 es el desafío adicional para los grupos más avanzados.

ETAPA 1 — Agente conversacional básico | 25 puntos

¿Qué se construye?
Un agente que mantiene una conversación coherente con el usuario usando la API de Claude. El agente tiene una personalidad y dominio definidos por el grupo, y recuerda todo lo dicho durante la sesión.

Requisitos técnicos
• Conexión a la API de Anthropic usando el SDK oficial de Python (librería anthropic)

• System prompt que define la personalidad, el rol y el dominio del agente

• Historial de mensajes que preserva el contexto completo de la conversación (memoria de sesión)

• Interfaz por consola con loop de conversación — el usuario escribe, el agente responde

Ejemplo de interacción esperada
Usuario: Hola, ¿qué podés hacer?

Agente: Soy tu asistente gastronómico. Puedo sugerirte recetas,

         ayudarte con ingredientes y calcular porciones.

Usuario: ¿Qué puedo hacer con pollo, limón y ajo?

Agente: Te sugiero pollo al limón con ajo: [receta detallada...]

Usuario: ¿Y si soy celíaco?

Agente: Perfecto, esa receta es naturalmente libre de gluten.

         Solo asegurate de que el caldo que uses esté certificado...

⚠️ La memoria de sesión es el requisito más importante de esta etapa. El agente debe recordar lo que el usuario dijo antes dentro de la misma conversación.

ETAPA 2 — Personalidad, contexto y robustez | 25 puntos

¿Qué se agrega?
El agente deja de ser genérico y se convierte en un asistente especializado con comportamiento robusto ante situaciones inesperadas.

Requisitos técnicos
• System prompt elaborado con rol específico, restricciones de dominio y tono definido

• El agente rechaza educadamente consultas fuera de su dominio (con una respuesta coherente, no un error)

• Manejo de errores de la API: timeout, rate limit, problemas de conexión — el programa no debe cerrarse abruptamente

• Comando /salir para terminar la sesión con un mensaje de despedida

• Comando /limpiar para reiniciar el historial y comenzar una conversación nueva

Ejemplo de system prompt elaborado
Sos un asistente gastronómico especializado en cocina mediterránea.

Tu nombre es Olivia. Respondés siempre en español, con un tono

amigable y entusiasta. Solo respondés preguntas relacionadas con

cocina, recetas, ingredientes y técnicas culinarias.

Si te preguntan algo fuera de ese tema, explicás amablemente que

tu especialidad es la gastronomía y ofrecés redirigir la consulta.

Nunca inventés recetas con ingredientes que puedan ser peligrosos.

ETAPA 3 — Herramientas externas (Function Calling) | 25 puntos

¿Qué se agrega?
El agente puede ejecutar acciones reales. Deja de ser solo conversacional y empieza a actuar en el mundo: consulta datos, hace cálculos, accede a servicios externos. El modelo decide de forma autónoma cuándo llamar a cada herramienta.

Requisitos técnicos
• Implementación de al menos 2 herramientas usando function calling de la API de Anthropic

• El modelo decide autónomamente cuándo invocar cada herramienta y con qué parámetros

• Las herramientas deben ser coherentes con el dominio elegido en la Etapa 1

• El resultado de cada herramienta se integra naturalmente en la respuesta del agente

Ejemplos de herramientas por dominio
Dominio

Herramienta 1

Herramienta 2

Gastronómico

Buscar receta por ingredientes

Calcular porciones para N personas

Académico

Buscar definición en Wikipedia (API)

Generar preguntas de repaso sobre un tema

Financiero

Calcular interés compuesto

Convertir moneda (API pública)

Atención al cliente

Consultar estado de pedido (mock)

Registrar reclamo en archivo local

Programación

Ejecutar código Python en sandbox

Buscar documentación de una función

Salud

Calcular IMC

Consultar interacción entre medicamentos (mock)

💡 Una herramienta puede ser una función Python simple — no necesita llamar a una API externa. Lo importante es que el modelo la invoque de forma autónoma cuando corresponde.

ETAPA 4 — Persistencia y contexto externo | 25 puntos

¿Qué se agrega?
El agente tiene memoria entre sesiones o puede trabajar con información propia del dominio. El grupo elige una de las dos opciones.

Opción A — Memoria persistente entre sesiones
• El historial de conversaciones se guarda en un archivo JSON o base de datos SQLite al finalizar cada sesión

• Al iniciar, el agente recupera y muestra las conversaciones anteriores disponibles

• El usuario puede retomar una conversación previa seleccionándola por fecha o identificador

Opción B — Base de conocimiento propia (RAG básico)
• El agente responde basándose en documentos propios del dominio (archivos PDF o TXT)

• Implementa búsqueda por similitud o por palabras clave para encontrar fragmentos relevantes

• Las respuestas hacen referencia explícita a la fuente del documento consultado

ℹ️ La Etapa 4 no es requisito para aprobar el TP. Es el desafío adicional para grupos que quieran profundizar. Ambas opciones tienen el mismo puntaje.

e) Criterios de evaluación

Criterio

Descripción

Puntaje

Funcionalidad

Etapas completadas correctamente y agente funcional en la demo

Según etapas

Calidad del código

Código legible, comentado, estructura clara, sin errores innecesarios

Incluido en etapas

README

Instrucciones claras para instalar y ejecutar el agente desde cero

Incluido en etapas

Informe técnico

Documenta decisiones de diseño, arquitectura, dificultades y conclusiones

Incluido en etapas

Demo y defensa oral

El agente funciona en vivo y el grupo puede responder preguntas técnicas

Incluido en etapas

Puntaje por etapas completadas

Etapas completadas

Puntaje total

Nota aproximada

Solo Etapa 1

25 puntos

5

Etapas 1 + 2

50 puntos

6

Etapas 1 + 2 + 3

75 puntos

8

Etapas 1 + 2 + 3 + 4

100 puntos

10

⚠️ Una etapa se considera completada si todos sus requisitos técnicos funcionan correctamente durante la demo. Una etapa parcialmente implementada no suma puntaje.

f) Entorno técnico sugerido
Componente

Opción sugerida

Alternativa

Lenguaje

Python 3.10+

No hay alternativa — el TP es en Python

API de IA

Anthropic (Claude) — anthropic SDK

OpenAI, Gemini (requiere adaptar el código

Entorno de desarrollo

VS Code

PyCharm, cualquier editor

Gestión de dependencias

pip + requirements.txt

conda, poetry

Control de versiones

Git + GitHub

GitLab, Bitbucket

Base de datos (Etapa 4A)

SQLite (incluido en Python)

JSON plano

Instalación mínima

# 1. Clonar el repositorio o descomprimir la carpeta

# 2. Crear entorno virtual

python -m venv venv

venv\Scripts\activate # Windows

source venv/bin/activate # Mac/Linux

# 3. Instalar dependencias

pip install anthropic

# 4. Configurar la API key

# Windows PowerShell:

$env:ANTHROPIC_API_KEY = 'sk-ant-...'

# Mac/Linux:

export ANTHROPIC_API_KEY='sk-ant-...'

# 5. Ejecutar el agente

python agente.py

g) Estructura del informe técnico
El informe en PDF debe incluir las siguientes secciones:

1.         Introducción: dominio elegido, problema que resuelve el agente y justificación de la elección

2.         Arquitectura del agente: diagrama o descripción del flujo de procesamiento de mensajes

3.         Decisiones de diseño: por qué se eligió ese system prompt, esas herramientas, esa estructura de código

4.         Etapas implementadas: descripción de cada etapa completada con fragmentos de código representativos

5.         Dificultades encontradas: qué salió mal, cómo lo resolvieron, qué aprendieron del proceso

6.         Conclusiones: qué es un agente de IA según su experiencia, limitaciones del sistema desarrollado

💡 El informe no es un manual de usuario. Es un documento técnico que muestra comprensión profunda de lo que se construyó y por qué se tomaron esas decisiones.
h) Checklist de entrega
Antes de entregar, verificar que el repositorio o carpeta .zip contiene:

• agente.py (o equivalente) — archivo principal ejecutable

• requirements.txt — lista de dependencias con versiones

• README.md — instrucciones de instalación y ejecución

• informe.pdf — informe técnico completo

• El agente se puede ejecutar desde cero siguiendo el README

• El agente no tiene la API key hardcodeada en el código

⚠️ La API key nunca debe estar en el código fuente. Usar variables de entorno. Un repositorio con la API key expuesta implica descuento de puntos.
