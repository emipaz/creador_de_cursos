import os
import openai
from dotenv import load_dotenv , find_dotenv
from langchain_community.document_loaders import TextLoader
#from langchain_chroma import Chroma
#from langchain_openai import OpenAIEmbeddings

from utils import markdown_to_html_with_math
from tqdm import tqdm as tqdm
from gen_ppt import crear_resumen
from gen_ppt import crear_slide, crear_ppt
from prompt import get_full_html
from config import DESTINO_WEB

def crear_html_ppt(curso, carpeta):
    slides = {"slides":[]}
    html = ""
    # documentos_base = []
    for archivo in tqdm(os.listdir(os.path.join(curso, carpeta))):
        path = os.path.join(curso, carpeta, archivo)
        # print(path)
        if archivo == ".ipynb_checkpoints" : continue
        doc = TextLoader(path).load()
        # TODO fragmentar con rescursive para la busqueda semantica documentos_base.extend(doc)
        resumen = ""
        for d in doc:
            res = crear_resumen(d.page_content) + "\n___\n"
            slides["slides"].extend(crear_slide(res).get("slides",[]))
            resumen += res
        
        html += markdown_to_html_with_math(resumen) + "\n"
    return html, slides, # documentos_base
    
def guardar_html(html, modulo):
    des_html = os.path.join(DESTINO_WEB, modulo + ".html")
    full_html = get_full_html(html, modulo)
    with open(des_html, "w", encoding= "utf-8") as f:
        f.write(full_html)
    print("Se guardo en : ", des_html)
      

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("carpeta", type=str, help="Carpeta del curso")
    args = parser.parse_args()
    print(args)
    
    curso , carpetas, _ = next(os.walk(args.carpeta))
    curso = curso.strip("\\").lstrip(".\\")
    
    print("curso",curso)
    for carpeta in carpetas:
        if carpeta == ".ipynb_checkpoints" : continue
        modulo = carpeta
        print("Crando Html de ",modulo)
        html, slides = crear_html_ppt(curso, carpeta)
        guardar_html(html, modulo)
        crear_ppt(slides, curso, modulo)
        # TODO Crear base de datos con los documantos fragmentados
        
            


