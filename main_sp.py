import os
import shutil
from pyspark.sql import SparkSession
from langchain_community.document_loaders import TextLoader
from gen_ppt import crear_resumen, crear_slide, crear_ppt, base_sp
from gen_ppt import markdown_to_html_with_math, guardar_html, guardar_mark
from config import DESTINO_WEB, DESTINO_PPT, DESTINO_BASES, DESTINO_MK
import logging


# Variables de entorno para workers de spark
os.environ["PYSPARK_PYTHON"] = r"C:\Users\Usuario\Desktop\Bots\env\Scripts\python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = r"C:\Users\Usuario\Desktop\Bots\env\Scripts\python.exe"
os.environ["PYSPARK_LOG_LEVEL"] = "INFO"

# Configura el logger de Python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def procesar_archivo(index, path, curso, carpeta, carpeta_bases):
    logger.info(f"procesando : {path}")
    resumen = ""
    slides = {"slides": []}
    documentos = []

    if path.endswith(".txt"):
        doc = TextLoader(path, autodetect_encoding=True).load()
        for d in doc:
            d.metadata["id"] = curso + " " + carpeta
            documentos.append(d)
            res = crear_resumen(d.page_content) + "\n___\n"
            slides["slides"].extend(crear_slide(res).get("slides", []))
            resumen += res
    
    base_sp(carpeta_bases, documentos, carpeta)
    html = markdown_to_html_with_math(resumen)
    return (index, {
        "modulo": carpeta,
        "html": html,
        "slides": slides,
        "documentos": documentos,
        "resumen": resumen
    })

def copiar_archivos_estaticos(source, dest):
    shutil.copytree(source, dest, dirs_exist_ok=True)
    print(f"Archivos copiados a {dest}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--carpeta', type=str, help="Carpeta del curso")
    parser.add_argument('--unique_bot', action='store_true', help='Genera un mismo bot para todos los módulos')
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    carpeta_html  = os.path.join(args.carpeta, DESTINO_WEB)
    carpeta_mark  = os.path.join(args.carpeta, DESTINO_MK)
    carpeta_ppts  = os.path.join(args.carpeta, DESTINO_PPT)
    carpeta_bases = os.path.join(args.carpeta, DESTINO_BASES)

    os.makedirs(carpeta_ppts, exist_ok=True)
    os.makedirs(carpeta_mark, exist_ok=True)

    copiar_archivos_estaticos(os.path.join(base_dir, DESTINO_WEB), carpeta_html)
    copiar_archivos_estaticos(os.path.join(base_dir, "api"), args.carpeta)

    curso, carpetas, _ = next(os.walk(args.carpeta))
    curso = curso.strip("\\").lstrip(".\\")
    carpetas_ordenadas = sorted([
        c for c in carpetas
        if c not in {".ipynb_checkpoints", "__pycache__", "import_bot", ".git", DESTINO_WEB, DESTINO_PPT, DESTINO_BASES, DESTINO_MK}
    ])

    archivos_indexados = []
    for carpeta in carpetas_ordenadas:
        carpeta_path = os.path.join(args.carpeta, carpeta)
        for archivo in sorted(os.listdir(carpeta_path)):
            if archivo.endswith(".txt"):
                path = os.path.join(carpeta_path, archivo)
                archivos_indexados.append((len(archivos_indexados), path, curso, carpeta, carpeta_bases))

    spark = SparkSession.builder.appName("CursoDistribuido").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    sc = spark.sparkContext

    rdd = sc.parallelize(archivos_indexados)
    resultados = rdd.map(lambda args: procesar_archivo(*args)).collect()
    resultados_ordenados = sorted(resultados, key=lambda x: x[0])

    index = 1
    resumen = ""

    resumen_total = ""
    html = ""
    documentos_total = []
    slides_total = []

    for idx, resultado in resultados_ordenados:
        modulo = resultado["modulo"]
        resumen = resultado["resumen"]
        html_mod = resultado["html"]
        slides = resultado["slides"]
        # documentos = resultado["documentos"]

        # Acumula para la base
        resumen_total += resumen
        # html = resultado["html"]
        html += html_mod + "\n"
        # documentos_total.extend(documentos)
        slides_total.extend(slides["slides"])

    
    guardar_html(html, carpeta_html, modulo, index)
    guardar_mark(resumen_total, carpeta_mark, modulo)
    crear_ppt(slides, carpeta_ppts, modulo)
    # print(base(carpeta_bases, index, resultados_ordenados))
