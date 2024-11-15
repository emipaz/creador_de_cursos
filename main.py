import os
import openai
from dotenv import load_dotenv , find_dotenv
from langchain_community.document_loaders import TextLoader
#from langchain_chroma import Chroma
#from langchain_openai import OpenAIEmbeddings

from generador_resumen import crear_resumen
from md_to_html import markdown_to_html_with_math
from tqdm import tqdm as tqdm

DESTINO = "public_html"

#load_dotenv(find_dotenv())

#cliente = openai.Client()

mathjax_script = '''
    <script type="text/javascript" async
      src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
    </script>
    '''
    

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("carpeta", type=str, help="Carpeta del curso")
    args = parser.parse_args()
    # print(args)
    curso , carpetas, _ = next(os.walk(args.carpeta))
    curso = curso.strip("\\").lstrip(".\\")
    # print("curso",curso)
    for carpeta in carpetas:
        if carpeta == ".ipynb_checkpoints" : continue
        modulo = carpeta
        print("Crando Html de ",modulo)
        
        html = ""
        for archivo in tqdm(os.listdir(os.path.join(curso, carpeta))):
            path = os.path.join(curso, carpeta, archivo)
            doc = TextLoader(path).load()
            resumen = ""
            for d in doc:
                resumen += crear_resumen(d.page_content) + "\n___\n"
            html += markdown_to_html_with_math(resumen,modulo) + "\n"
        full_html = f'''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{modulo}</title>
        <link rel="stylesheet" href="styles.css">
        {mathjax_script}
    </head>
    <body>
        {html}
    </body>
    </html>
    '''
        des_html = os.path.join(DESTINO, modulo + ".html")
        with open(des_html, "w", encoding= "utf-8") as f:
            f.write(full_html)
        print("Se guardo en : ", des_html)
            


