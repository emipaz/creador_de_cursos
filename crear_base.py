from dotenv import load_dotenv , find_dotenv
load_dotenv(find_dotenv())
import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import openai
cliente = openai.Client()
emb = OpenAIEmbeddings()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 2000,
    chunk_overlap = 250
)
def base(curso, index, documentos):
    path = os.path.join(curso,f"base_{index}")
    bs = Chroma(embedding_function = emb, persist_directory = path)
    fragmentos = text_splitter.split_documents(documents=documentos)
    return bs.add_documents(documents=fragmentos)
