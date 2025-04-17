import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import tempfile
import os
import requests

# =====================
# CONFIGURACIÓN API KEYS
# =====================
API_KEY_OPENWEATHER = "TU_API_KEY_OPENWEATHER"
HUGGINGFACE_TOKEN = "TU_TOKEN_DE_HUGGINGFACE"

# =====================
# HABLAR (voz realista con gTTS)
# =====================
def hablar(texto):
    print("Asistente:", texto)
    tts = gTTS(text=texto, lang='es')
    temp_path = "temp_audio.mp3"  # Archivo temporal
    tts.save(temp_path)  # Guarda el archivo temporal
    playsound(temp_path)  # Reproduce el archivo
    os.remove(temp_path)  # Elimina el archivo después de reproducirlo

# =====================
# ESCUCHAR (voz a texto)
# =====================
def escuchar():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            #playsound("beep.mp3")
            print("🎙️ Escuchando...")
            audio = r.listen(source)
            texto = r.recognize_google(audio, language='es-ES')
            print("Tu dijiste:", texto)
            return texto.lower()
    except sr.UnknownValueError:
        hablar("No entendi eso, ¿puedes repetir?")
    except sr.RequestError as e:
        hablar(f"Hubo un problema con el reconocimiento de voz: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrio un error {e}.")
    return ""

# =====================
# CLIMA
# =====================
def obtener_clima(ciudad):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={API_KEY_OPENWEATHER}&units=metric&lang=es"
    try:
        respuesta = requests.get(url)
        datos = respuesta.json()

        if datos["cod"] != 200:
            return "No pude encontrar el clima de esa ciudad."

        temp = datos["main"]["temp"]
        descripcion = datos["weather"][0]["description"]
        return f"En {ciudad} hay {descripcion} y una temperatura de {temp} grados."
    except:
        return "Ocurrió un error al obtener el clima."

# =====================
# HUGGING FACE
# =====================
def preguntar_a_huggingface(pregunta):
    url = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"  # Modelo de Hugging Face
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_TOKEN}"  # Reemplaza con tu token
    }
    
    payload = {
        "inputs": pregunta,
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        respuesta = response.json()

        if isinstance(respuesta, list) and 'generated_text' in respuesta[0]:
            return respuesta[0]['generated_text'].strip()
        else:
            return "No pude entender la respuesta."
    except Exception as e:
        return f"Ocurrió un error al consultar Hugging Face: {e}"

# =====================
# RESPONDER
# =====================
def responder(comando):
    try:
        if "hola" in comando:
            hablar("¡Hola! ¿En que te puedo ayudar?")
        elif "abre el navegador" in comando:
            hablar("Abriendo el navegador.")
            os.system("start chrome")
        elif "clima" in comando:
            hablar("¿De que ciudad quieres saber el clima?")
            ciudad = escuchar()
            if ciudad:
                clima = obtener_clima(ciudad)
                hablar(clima)
        elif "salir" in comando or "adios" in comando:
            hablar("Hasta luego.")
            exit()
        else:
            respuesta = preguntar_a_huggingface(comando)
            hablar(respuesta)
    except Exception as e:
        messagebox.showerror("Error en responder", f"Ocurrio un error: {e}")
# =====================
# INTERFAZ GRÁFICA
# =====================
def iniciar_asistente():
    def on_enviar_comando():
        comando = entrada_comando.get()
        texto_output.insert(tk.END, "Tu: " + comando + "\n")
        responder(comando)
        entrada_comando.delete(0, tk.END)
    
    def on_escuchar_comando():
        
        comando = escuchar()
        if comando:
            texto_output.insert(tk.END, "Tu: " + comando + "\n")
            responder(comando)

    # Crear la ventana principal
    ventana = tk.Tk()
    ventana.title("Asistente Virtual")
    ventana.geometry("500x400")
    
    # Crear área de texto para mostrar las respuestas
    texto_output = scrolledtext.ScrolledText(ventana, width=60, height=15, wrap=tk.WORD)
    texto_output.grid(row=0, column=0, padx=10, pady=10)
    
    # Crear cuadro de texto para ingresar comandos
    entrada_comando = tk.Entry(ventana, width=40)
    entrada_comando.grid(row=1, column=0, padx=10, pady=10)
    
    # Botones
    boton_enviar = tk.Button(ventana, text="Enviar", command=on_enviar_comando)
    boton_enviar.grid(row=2, column=0, padx=10, pady=5)
    
    boton_escuchar = tk.Button(ventana, text="Escuchar", command=on_escuchar_comando)
    boton_escuchar.grid(row=3, column=0, padx=10, pady=5)

    # Iniciar la interfaz gráfica
    ventana.mainloop()

# =====================
# PROGRAMA PRINCIPAL
# =====================
if __name__ == "__main__":
    iniciar_asistente()
