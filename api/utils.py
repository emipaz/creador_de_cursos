import re
import logging
import markdown
from html2text import html2text
from mdx_math import MathExtension # pip install python-markdown-math

def create_logger(app, name_file = 'registro.log',):
    logging.basicConfig(
        filename=name_file, 
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s',
        encoding='utf-8'    
    )
    # Registrar mensajes a medida que el script va ejecutándose
    logger = logging.getLogger(app)
    return logger

def make_links_clickable(text):
    # Regex para detectar enlaces HTTP y HTTPS
    url_pattern = re.compile(r'(https?://\S+)')
    
    # Función para reemplazar el enlace con una versión HTML clicable
    def replace_url_with_html(match):
        url = match.group(0)
        # Si el enlace termina en un punto, eliminarlo
        if url[-1] == '.':
            url = url[:-1]
        return f'<a href="{url}" target="_blank">{url}</a>'
    
    # Usar sub para reemplazar los enlaces en el texto
    clickable_text = re.sub(url_pattern, replace_url_with_html, text)
    return clickable_text
  
def add_target_blank_to_links(html):
    # Regex para detectar etiquetas <a> y agregar target="_blank"
    def replace_anchor_tag(match):
        anchor_tag = match.group(0)
        if 'target="_blank"' not in anchor_tag:
            anchor_tag = anchor_tag.replace('<a ', '<a target="_blank" ')
        return anchor_tag
    
    # Detectar todas las etiquetas <a> y modificar su contenido
    anchor_pattern = re.compile(r'<a\s+(?![^>]*\btarget=)[^>]*href=["\'](https?://\S+)["\']')
    modified_html = anchor_pattern.sub(replace_anchor_tag, html)
    return modified_html

def markdown2html(text):
    html = markdown.markdown(text)
    return html
 
def html_text(html):
    return html2text(html)


def markdown_to_html_with_math(markdown_text):
    # Configurar las extensiones
    md = markdown.Markdown(extensions=['extra', MathExtension(enable_dollar_delimiter=True)])
    
    # Convertir Markdown a HTML
    html = md.convert(markdown_text)
    return html
