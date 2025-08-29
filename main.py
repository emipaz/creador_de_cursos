import os
import shutil
from tqdm import tqdm as tqdm
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader

from gen_ppt import crear_resumen
from gen_ppt import crear_slide, crear_ppt
from gen_ppt import markdown_to_html_with_math
from gen_ppt import guardar_html , guardar_mark
from gen_ppt import base

from config import DESTINO_WEB , DESTINO_PPT , DESTINO_BASES, DESTINO_MK


def carga_extras(path):
    carpeta_base = os.path.abspath(os.getcwd())
    documentos_extras = []
    path = path.rstrip("/") 
    print("cargando extras desde:", path)
    if path == ".ipynb_chekpoints": return []
    for extra in os.listdir(path):
        extra_path = os.path.join(carpeta_base, path, extra)
        print(f"Cargando : {extra}")
        if extra.endswith('.pdf'):
            loader = PyMuPDFLoader(extra_path)
        elif extra.endswith('.txt') or extra.endswith('.md') or extra.endswith(".py"):
            loader = TextLoader(extra_path, autodetect_encoding=True)
        else:
            continue
        documents = loader.load()
        for d in documents:
            d.metadata["id"] = extra + "-" + str(d.metadata.get("page",""))
        documentos_extras.extend(documents)
        print("extras:",len(documentos_extras))
    return documentos_extras

def crear_material(curso, carpeta):
    slides = {"slides":[]}
    html = ""
    mark = ""
    # resumen = ""
    documentos_base = []
    for archivo in sorted(os.listdir(os.path.join(curso, carpeta))):
        print(archivo)
        path = os.path.join(curso, carpeta, archivo)
        print("cargando", path)
        if archivo == "extras":
            print("detecto carpeta extras")
            extras_path = os.path.join(curso, carpeta , archivo)
            carpetas_extras = os.walk(extras_path)
            for raiz ,_,__ in carpetas_extras:
                print("Explorando :",raiz)
                documentos_base.extend(carga_extras(raiz))
                print("documentos_base",len(documentos_base))
        elif not str.endswith(archivo,".txt"): 
            continue
        else:
            resumen=""
            doc = TextLoader(path,autodetect_encoding=True).load()
            for d in doc:
                d.metadata["id"] = curso + " " + carpeta
            documentos_base.extend(doc)
            print("documentos_base",len(documentos_base))
            for d in doc:
                res = crear_resumen(d.page_content) + "\n___\n"
                slides["slides"].extend(crear_slide(res).get("slides",[]))
                resumen += res
        
        html += markdown_to_html_with_math(resumen) + "\n"
        mark += resumen + "\n"
    return html, slides, documentos_base, mark

def copiar_archivos_estaticos(source, dest): 
    shutil.copytree(source, dest, dirs_exist_ok = True) 
    print(f"Archivos copiados a {dest}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--carpeta', type=str, help="Carpeta del curso")
    parser.add_argument('--unique_bot', action='store_true', help='Genera un mismo bot para todos los modulos con el material completo')
    args = parser.parse_args()
    print(args)
    base_dir      = os.path.dirname(os.path.abspath(__file__))
    carpeta_html  = os.path.join(args.carpeta, DESTINO_WEB)
    carpeta_mark  = os.path.join(args.carpeta, DESTINO_MK)
    carpeta_ppts  = os.path.join(args.carpeta, DESTINO_PPT)
    carpeta_bases = os.path.join(args.carpeta, DESTINO_BASES)
    
    # os.makedirs(carpeta_html, exist_ok=True)
    os.makedirs(carpeta_ppts, exist_ok=True)
    os.makedirs(carpeta_mark, exist_ok=True)
    estilos_js = os.path.join(base_dir, DESTINO_WEB)
    archivo_py = os.path.join(base_dir, "api")
    copiar_archivos_estaticos(estilos_js, carpeta_html)
    copiar_archivos_estaticos(archivo_py, args.carpeta)
    
    
    curso , carpetas, _ = next(os.walk(args.carpeta))
    curso = curso.strip("\\").lstrip(".\\")
    
    print("curso",curso)
    print("Carpetas", carpetas)
    index = 1
    htmls = []
    for carpeta in carpetas:
        print(carpeta)
        if carpeta in {".ipynb_checkpoints","__pycache__","import_bot",".git",DESTINO_WEB,DESTINO_PPT,DESTINO_BASES, DESTINO_MK }:
            continue
        modulo = carpeta
        print("Crando Html de ",modulo)
        html, slides, documentos , resumen = crear_material(curso, carpeta)
        print("documentos:",len(documentos))
        guardar_html(html, carpeta_html, modulo, index)
        guardar_mark(resumen, carpeta_mark, modulo)
        crear_ppt(slides, carpeta_ppts, modulo)
        print(base(carpeta_bases ,index, documentos))
        if not args.unique_bot:
            index += 1
        # TODO Crear base de datos con los documantos fragmentados
        
            


