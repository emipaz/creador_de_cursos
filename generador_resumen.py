from prompt import system_markdown
import os
import openai
from dotenv import load_dotenv , find_dotenv
load_dotenv(find_dotenv())
from langchain_community.document_loaders import TextLoader
# from langchain_community.document_loaders import PyMuPDFLoader
cliente = openai.Client()

def crear_resumen(texto :str ) -> str:
    mensaje = [
        {
            "role": "system",
            "content": system_markdown},
        {
            "role": "user",
            "content": f"Trascripción del video : {texto}"
        }
    ]
    chat = cliente.chat.completions.create(
            model = "gpt-4o-mini", # modelo a usar
            messages = mensaje,    # lista de mensajes
            temperature = 0,)
    return chat.choices[0].message.content

