import os
from tqdm import tqdm as tqdm
from langchain_community.document_loaders import TextLoader

from gen_ppt import crear_resumen
from gen_ppt import crear_slide, crear_ppt
from gen_ppt import markdown_to_html_with_math
from gen_ppt import guardar_html
from gen_ppt import base

from config import DESTINO_WEB , DESTINO_PPT , DESTINO_BASES

def crea_material(curso, carpeta):
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
      

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("carpeta", type=str, help="Carpeta del curso")
    args = parser.parse_args()
    print(args)
    carpeta_html  = os.path.join(args.carpeta, DESTINO_WEB)
    carpeta_ppts  = os.path.join(args.carpeta, DESTINO_PPT)
    carpeta_bases = os.path.join(args.carpeta, DESTINO_BASES)
    os.makedirs(ruta, exist_ok=True)
    os.makedirs(pres, exist_ok=True)
    curso , carpetas, _ = next(os.walk(args.carpeta))
    curso = curso.strip("\\").lstrip(".\\")
    
    print("curso",curso)
    index = 1
    for carpeta in carpetas:
        if carpeta in {".ipynb_checkpoints",DESTINO_WEB,DESTINO_PPT,DESTINO_BASES}:
            continue
        modulo = carpeta
        print("Crando Html de ",modulo)
        html, slides, documentos = crear_material(curso, carpeta)
        guardar_html(html, carpeta_html, modulo)
        crear_ppt(slides, carpeta_ppts, modulo)
        print(base(carpeta_bases ,index, documentos))
        index += 1
        # TODO Crear base de datos con los documantos fragmentados
        
            


