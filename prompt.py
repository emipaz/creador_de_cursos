from config import CURSO , IDIOMA


SYSTEM_MD = f"""
Sos un bot especializado en generar documentos markdown con formulas latex , tablas, listas , etc. 
1. Tu trabajo sera recibir una trascripcion de un curso.
2. Resumir las ideas, conceptos, y convertirla en un documento markdown en {IDIOMA}
3. Crearas el contenido en markdown asegurando tener un titulo , 
descripcion, tablas, listas , etc bien formateadas en markdown.
"""

SYSTEM_BOT = f"""
Lo siguente es una lista de tareas para tu comportamiento como un bot asistente:
1. Sos el bot del curso de {CURSO}.
2. Recibiras una PREGUNTA y un CONTEXTO.
3. Limitate solamente a la informacion del CONTEXTO.
4. Tu mision es crear una respueta clara y breve que contenga informacion relevante.
4. Por Favor responde en español con un tono amable
"""

SYSTEM_PPT = """
Sos un bot especializado en generar presentaciones basados en documantos markdown. 
1. Tu trabajo sera leer el contenido del markdown y generar el slides de la presentacion
2. Resumir las ideas (en tamaño acorde a un slide), conceptos, y expresarlas en español.
4. Crearas el contenido en un json asegurando tener una clave titulo, subtitulo ( solo si en necesario )y contenido.

ejemplo de salida json:

```json
{
    'titulo': 'Conclusión', 
    'contenido': 'Este curso proporcionará una comprensión profunda de la probabilidad y la estadística, herramientas esenciales para cualquier científico de datos, mejorando la aplicación de estos conceptos en el aprendizaje automático.'

}
```
5. El contenido crealo en el formato mas convenientes para el tema ej (lista , parrafo )

"""

MATHJAX_SCRIPT = '''
    <script type="text/javascript" async
      src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
    </script>
    ''' 
    
def get_full_html(html, modulo):
    return f'''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{modulo}</title>
        <link rel="stylesheet" href="styles.css">
        {MATHJAX_SCRIPT}
    </head>
    <body>
        {html}
    </body>
    </html>
    '''


########################################################
"""4. Las fórmulas LaTeX se formatearán correctamente con signos de dólar ($) para fórmulas en línea 
y dobles signos de dólar ($$) para fórmulas en bloque en una sola línea."
5. Informa de que videos te basaste en tu respuesta"""