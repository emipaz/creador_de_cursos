import os
import shutil
from tqdm import tqdm as tqdm
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader

from gen_ppt import crear_resumen
from gen_ppt import crear_slide, crear_ppt
from gen_ppt import markdown_to_html_with_math
from gen_ppt import guardar_html
from gen_ppt import base

from config import DESTINO_WEB , DESTINO_PPT , DESTINO_BASES


def carga_extras(path):
    carpeta_base = os.path.abspath(os.getcwd())
    documentos = []
    path = path.rstrip("/") 
    print("cargando extras desde:", path)
    if path == ".ipynb_chekpoints": return []
    for extra in os.listdir(path):
        extra_path = os.path.join(carpeta_base, path, extra)
        print(f"Cargando : {extra}")
        if extra.endswith('.pdf'):
            loader = PyMuPDFLoader(extra_path)
        if extra.endswith('.txt') or extra.endswith('.md'):
            loader = TextLoader(extra_path)
        documents = loader.load()
        documentos.extend(documents)
    return documentos 

def crear_material(curso, carpeta):
    slides = {"slides":[]}
    html = ""
    documentos_base = []
    for archivo in os.listdir(os.path.join(curso, carpeta)):
        print(archivo)
        path = os.path.join(curso, carpeta, archivo)
        print("cargando", path)
        if archivo == "extras":
            print("detecto carpeta extras")
            extras = os.path.join(curso, carpeta , archivo)
            carpetas = os.walk(extras)
            for raiz ,_,__ in carpetas:
                print("Explorando :",raiz)
                documentos_base.extend(carga_extras(raiz))
        elif not str.endswith(archivo,".txt"): continue
        else:
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
    base_dir      = os.path.dirname(os.path.abspath(__file__))
    carpeta_html  = os.path.join(args.carpeta, DESTINO_WEB)
    carpeta_ppts  = os.path.join(args.carpeta, DESTINO_PPT)
    carpeta_bases = os.path.join(args.carpeta, DESTINO_BASES)
    
    os.makedirs(carpeta_html, exist_ok=True)
    os.makedirs(carpeta_ppts, exist_ok=True)
    estilos_js = os.path.join(base_dir, DESTINO_WEB)
    archivo_py = os.path.join(base_dir, "api")

    curso , carpetas, _ = next(os.walk(args.carpeta))
    curso = curso.strip("\\").lstrip(".\\")
    
    print("curso",curso)
    index = 1
    htmls = []
    for carpeta in carpetas:
        if carpeta in {".ipynb_checkpoints",DESTINO_WEB,DESTINO_PPT,DESTINO_BASES}:
            continue
        modulo = carpeta
        print("Crando Html de ",modulo)
        html, slides, documentos = crear_material(curso, carpeta)
        guardar_html(html, carpeta_html, modulo, index)
        crear_ppt(slides, carpeta_ppts, modulo)
        print(base(carpeta_bases ,index, documentos))
        index += 1
        # TODO Crear base de datos con los documantos fragmentados
        
            


