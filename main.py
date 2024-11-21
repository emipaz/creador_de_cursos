import os
import openai
from dotenv import load_dotenv , find_dotenv
from langchain_community.document_loaders import TextLoader

from utils import markdown_to_html_with_math
from tqdm import tqdm as tqdm
from gen_ppt import crear_resumen
from gen_ppt import crear_slide, crear_ppt
from prompt import get_full_html
from config import DESTINO_WEB , DESTINO_PPT
from crear_base import base

def crear_html_ppt(curso, carpeta):
    slides = {"slides":[]}
    html = ""
    documentos_base = []
    for archivo in tqdm(os.listdir(os.path.join(curso, carpeta))):
        path = os.path.join(curso, carpeta, archivo)
        # print(path)
        if archivo == ".ipynb_checkpoints" : continue
        doc = TextLoader(path).load()
        documentos_base.extend(doc)
        resumen = ""
        for d in doc:
            res = crear_resumen(d.page_content) + "\n___\n"
            slides["slides"].extend(crear_slide(res).get("slides",[]))
            resumen += res
        
        html += markdown_to_html_with_math(resumen) + "\n"
    return html, slides, documentos_base


def guardar_html(html,curso, modulo):
    des_html = os.path.join(curso, modulo + ".html")
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
    ruta = os.path.join(args.carpeta, DESTINO_WEB)
    pres = os.path.join(args.carpeta, DESTINO_PPT)
    os.makedirs(ruta, exist_ok=True)
    os.makedirs(pres, exist_ok=True)
    curso , carpetas, _ = next(os.walk(args.carpeta))
    curso = curso.strip("\\").lstrip(".\\")
    
    print("curso",curso)
    for index, carpeta in enumerate(carpetas,1):
        if carpeta == ".ipynb_checkpoints" : continue
        if carpeta == DESTINO_WEB: continue
        if carpeta == DESTINO_PPT: continue
        modulo = carpeta
        print("Crando Html de ",modulo)
        html, slides, documentos = crear_html_ppt(curso, carpeta)
        guardar_html(html, ruta, modulo)
        crear_ppt(slides, pres, modulo)
        print(base(args.carpeta ,index, documentos))
        # TODO Crear base de datos con los documantos fragmentados
        
            


