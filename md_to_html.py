import markdown
from mdx_math import MathExtension # pip install python-markdown-math

def markdown_to_html_with_math(markdown_text, titulo):
    # Configurar las extensiones
    md = markdown.Markdown(extensions=['extra', MathExtension(enable_dollar_delimiter=True)])
    
    # Convertir Markdown a HTML
    html = md.convert(markdown_text)
    
    # Script de MathJax para renderizar las fórmulas
    mathjax_script = '''
    <script type="text/javascript" async
      src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
    </script>
    '''
    
    # Crear HTML completo
    full_html = f'''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{titulo}</title>
        <link rel="stylesheet" href="styles.css">
        {mathjax_script}
    </head>
    <body>
        {html}
    </body>
    </html>
    '''
    
    return html

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("markdown", type=str, help="Archivo markdown .md")
    parser.add_argument("html", type=str, help="Archivo salida .html")
    parser.add_argument("-t", type=str, help="titulo del html", default="Sin Titulo")
    args = parser.parse_args()
    print(args)
    # archivo Markdown y html a convertir
    

    try:
        with open(args.markdown, 'r', encoding='utf-8') as f:
            markdown_text = f.read()

        html_output = markdown_to_html_with_math(markdown_text, args.t)

        # Guardar el resultado en un archivo HTML
        with open(args.html + ".html" , 'w', encoding='utf-8') as f:
            f.write(html_output)

        print(f"El archivo HTML ha sido generado como : \"{args.html + '.html'}\"")
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{args.markdown}'.")
    except Exception as e:
        print(f"Ocurrió un error: {str(e)}")
