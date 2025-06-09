import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()

OPENAI_LLM_MODEL = 'GPT-4o-mini'
OPENAI_EMBED_MODEL = 'text-embedding-3-small'
PINECONE_API_KEY = ''
PINECONE_INDEX_NAME= ''