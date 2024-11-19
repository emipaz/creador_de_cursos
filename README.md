# Creador de cursos

# Generador de Presentaciones HTML y PPT

Este proyecto utiliza la API de OpenAI para procesar texto y generar presentaciones en formato HTML y PowerPoint (PPT) a partir de documentos en una carpeta específica.

## Requisitos previos

Antes de ejecutar este proyecto, asegúrate de contar con lo siguiente:

### Herramientas necesarias

- **Python** (versión 3.8 o superior)
- **Pip** (gestor de paquetes de Python)
- Una cuenta de OpenAI con una **clave API válida**
- Archivos de texto (transcripciones de clases o videos de no mas de 20 minutos) en las carpetas que deseas procesar

### Bibliotecas requeridas

El proyecto utiliza las siguientes bibliotecas de Python, que puedes instalar ejecutando el comando `pip install -r requirements.txt`:

- `openai`
- `python-dotenv`
- `tqdm`
- `langchain-community`
- Otras dependencias incluidas en el archivo `requirements.txt`

## Configuración

### 1. Configurar la clave API de OpenAI

1. Crea un archivo `.env` en la raíz del proyecto.
2. Añade tu clave API de OpenAI en el archivo `.env`

   ```bash
   OPENAI_API_KEY=tu_clave_api
   ```

2. Instalar las dependencias
Ejecuta el siguiente comando en el directorio del proyecto para instalar las dependencias necesarias:

 ```bash
pip install -r requirements.txt
```

1. Configurar la estructura de carpetas
El directorio de entrada debe contener carpetas con documentos en formato de texto (.txt). Cada carpeta será tratada como un módulo del curso.

## Uso
Ejecutar el script principal
Para ejecutar el script y generar las presentaciones HTML y PPT, usa el siguiente comando:

```bash
python main.py <directorio_del_curso>
```

Parámetros
directorio_del_curso: Ruta al directorio que contiene las carpetas con documentos de 

texto.

Ejemplo
Si tienes un directorio llamado CursoPython con subcarpetas que contienen archivos .txt, ejecuta:

python main.py CursoPython

#### Salida generada

El script generará los siguientes archivos por módulo (carpeta):

Un archivo HTML con nombre de la carpeta del modulo, ubicado en la carpeta definida en la variable DESTINO_WEB de config.py.

Una presentación PPT con nombre del curso + modulo creada con el contenido procesado.