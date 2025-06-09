import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from create_prompt import create_image, create_human
load_dotenv()

llm = ChatOpenAI(model = os.environ['OPENAI_LLM_MODEL'], temperature=0.2)
embeddings = OpenAIEmbeddings(model=os.environ['OPENAI_EMBEDDING_MODEL'])

vector_stroe = PineconeVectorStore(
    index_name = os.environ['PINECONE_INDEX_NAME'],
    embedding = embeddings,
    pinecone_api_key = os.environ['PINECONE_API_KEY']
)

# 이미지 정보 추출
def describe_dish_flavor(image_bytes, query):
    data_url = f'data:image/jpeg;base64,{image_bytes}'
    messages = [
        {'role' : 'system', 
         'content' : create_image()},
         {'role' : 'user', 'content' : [
             {'type' : 'text', 'text' : query},
             {'type' : 'image_url', 'image_url' : {'url':data_url}}
         ]}
    ]

    return llm.invoke(messages).content

# 벡터DB에서 검색
def search_wine(dish_flavor):
    results_with_score = vector_stroe.similarity_search_with_score(
        dish_flavor, 
        k = 2
    )
    
    # 결과 유사도와 함께 처리
    wine_reviews = []
    
    for doc, score in results_with_score:
        review_text = f'유사도 : {score:.4f}\n 내용 : {doc.page_content}'
        wine_reviews.append(review_text)

    return {
        'dish_flavor' : dish_flavor,
        'wine_reviews' : '\n\n'.join(wine_reviews) 
    }

# 추천하는 이유 llm으로 생성
def recommand_wine(inputs):
    human_ = create_human()
    prompt = ChatPromptTemplate.from_messages([
        ('system', 'you are good wine sommelier'),
        ('human', human_)
    ])

    chain = prompt | llm | StrOutputParser()
    return chain.invoke(inputs)