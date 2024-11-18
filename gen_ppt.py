import os
import json

from dotenv import load_dotenv , find_dotenv
load_dotenv(find_dotenv())
import openai
cliente = openai.Client()


from langchain_community.document_loaders import TextLoader
from prompt import SYSTEM_MD , SYSTEM_PPT
from config import DESTINO_PPT

def crear_resumen(texto :str ) -> str:
    mensaje = [
        {
            "role": "system",
            "content": SYSTEM_MD},
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

def crear_slide(mark : str, ) -> str:
    mensaje = [
        {
            "role": "system",
            "content": SYSTEM_PPT},
        {
            "role": "user",
            "content": f"Convierte el siguiente markdown : {mark} eb una presentacion"
        }
    ]
    chat = cliente.chat.completions.create(
            model = "gpt-4o-mini", # modelo a usar
            response_format={ "type": "json_object" },
            messages = mensaje,    #t lista de mensajes
            temperature = 0,)

    return json.loads(chat.choices[0].message.content)

def crear_ppt(material, curso, modulo):
    from pptx import Presentation
    titulo    = curso
    subtitulo = modulo
    slides    = material.get("slides", [] )
    nombre = curso + "_" +modulo +".ppt"
    path = os.path.join(DESTINO_PPT,nombre)
    prs = Presentation()
    
    # Diapositiva 1: Título
    slide_layout = prs.slide_layouts[0]  # Diseño de diapositiva de título
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    title.text = titulo
    subtitle.text = subtitulo

    for slide in slides:
        titulo    = slide.get("titulo", "")
        # subtitulo = slide.get("subtitulo", "")
        contenido = slide.get("contenido", [] )
        hoja      = prs.slides.add_slide(slide_layout)
        title     = hoja.shapes.title
        content   = hoja.shapes.placeholders[1]
        title.text = titulo
        
        if isinstance (contenido, list):
            contenido = [str(x) for x in contenido]
            texto = "\n".join(contenido)
        else:
            texto = contenido
        content.text = texto

    prs.save(path)
    print("presentacion guardada en :", path)