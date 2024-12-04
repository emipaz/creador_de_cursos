from dotenv import load_dotenv , find_dotenv
load_dotenv(find_dotenv())

import openai
import os
from config import (MODELO, MEMORIA, DOCUMENTOS)
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from collections import deque
from prompt import get_system , get_prompt_system
from textwrap import fill
from utils import create_logger, html_text
import json
logger = create_logger('bot.py')

class Chatbot:
    def __init__(self, sec):
        # from config import BASES_PATH
        match sec:
            case 1:
                from config import BASE_1 as BASE
                from config import CURSO_1 as CURSO
                from config import ALIAS_1 as ALIAS
                from config import TEMARIO_1 as TEMARIO
                from config import DESCRIPCION_1 as DESCRIPCION
            case 2:
                from config import BASE_2 as BASE
                from config import CURSO_2 as CURSO
                from config import ALIAS_2 as ALIAS
                from config import TEMARIO_2 as TEMARIO
                from config import DESCRIPCION_2 as DESCRIPCION
            case 3:
                from config import BASE_3 as BASE
                from config import CURSO_3 as CURSO
                from config import ALIAS_3 as ALIAS
                from config import TEMARIO_3 as TEMARIO
                from config import DESCRIPCION_3 as DESCRIPCION
            case 4:
                from config import BASE_4 as BASE
                from config import CURSO_4 as CURSO
                from config import ALIAS_4 as ALIAS
                from config import TEMARIO_4 as TEMARIO
                from config import DESCRIPCION_4 as DESCRIPCION
              
        self.cliente = openai.Client()
        self.embedding = OpenAIEmbeddings()
        self.datadb = Chroma(persist_directory= BASE, embedding_function=self.embedding)
        self.mem = MEMORIA
        self.modelo = MODELO
        self.historial = deque(maxlen=self.mem ) # memoria que viene del cliente
        self.documentos = DOCUMENTOS
        self.service = None
        self.memoria = [] # memoria del bot durante la conversacion
        self.curso = CURSO
        self.alias = ALIAS
        self.temario = TEMARIO
        self.descripcion = DESCRIPCION
           
    def consulta_base(self, query):
        fragmentos = self.datadb.max_marginal_relevance_search(
            query, 
            k = self.documentos,)
        st = "---\n"
        metadata =""
        for doc in fragmentos:
            source = doc.metadata["source"]
            titulo = doc.metadata.get("title", "")
            time = doc.metadata.get("start_timestamp", "")
            metadata += f"Fuente : {source} --- titulo : {titulo} -- \n"
            st += f"Fuente  : {source}\ntitulo : {titulo} -- \n"
            st += fill(doc.page_content,80)  + "\n\n---\n"
        return st, metadata
    
    def consulta(self):
        return self.cliente.chat.completions.create(
                                    model = self.modelo,
                                    temperature = 0,
                                    messages=list(self.memoria),
    )
    
    def genera_mem(self,historial):
        self.memoria = [] # limpio la memoria
        for mensaje in historial:
            self.historial.append({
                "role": mensaje["role"], 
                "content": html_text(mensaje["content"])})
        self.memoria.append({"role": "system", "content": get_system(
            self.curso, self.alias, self.descripcion, self.temario)})
        self.memoria.extend(list(self.historial))
        
    def generar_respuesta_system (self, pregunta, historial):
        self.genera_mem(historial)
        contexto, metadata = self.consulta_base(pregunta) 
        prompt = get_prompt_system(pregunta, contexto, self.curso)
        self.memoria.append({"role":"user","content":prompt})
        
        return pregunta, prompt , self.consulta().choices[0].message.content
    
          