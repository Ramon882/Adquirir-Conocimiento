import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect("chatbot.db")
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS respuestas (
        pregunta TEXT PRIMARY KEY,
        respuesta TEXT
    )
''')
conn.commit()

# Respuestas precargadas
respuestas_base = {
    "hola": "¡Hola! ¿Cómo estás?",
    "como estas?": "Estoy bien, gracias por preguntar. ¿De qué te gustaría hablar?",
    "de que te gustaria hablar?": "Podemos hablar sobre cualquier tema que desees."
}

# Insertar respuestas precargadas si no existen
for pregunta, respuesta in respuestas_base.items():
    cursor.execute("INSERT OR IGNORE INTO respuestas (pregunta, respuesta) VALUES (?, ?)", (pregunta, respuesta))
conn.commit()

def obtener_respuesta(pregunta):
    cursor.execute("SELECT respuesta FROM respuestas WHERE pregunta = ?", (pregunta.lower(),))
    resultado = cursor.fetchone()
    return resultado[0] if resultado else None

def aprender_respuesta(pregunta, respuesta):
    cursor.execute("INSERT INTO respuestas (pregunta, respuesta) VALUES (?, ?)", (pregunta.lower(), respuesta))
    conn.commit()

print("Chatbot iniciado. Escribe 'salir' para terminar.")
while True:
    entrada = input("Tú: ").strip().lower()
    if entrada == "salir":
        break
    
    respuesta = obtener_respuesta(entrada)
    if respuesta:
        print("Bot:", respuesta)
    else:
        print("Bot: No sé la respuesta. ¿Cómo debería responder a eso?")
        nueva_respuesta = input("Ingresa la respuesta: ").strip()
        aprender_respuesta(entrada, nueva_respuesta)
        print("Bot: ¡Gracias! Ahora he aprendido una nueva respuesta.")

# Cerrar la conexión
conn.close()
