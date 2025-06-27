# from src.helper import load_pdf_file, text_split, download_hugging_face_embeddings
# from pinecone.grpc import PineconeGRPC as Pinecone
# from pinecone import ServerlessSpec
# from langchain_pinecone import PineconeVectorStore
# from dotenv import load_dotenv
# import os


# load_dotenv()

# PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')
# os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY


# extracted_data=load_pdf_file(data='C:/Users/abhis/Desktop/Projects/web/proj/New folder/MediBot-AI/Data')
# text_chunks=text_split(extracted_data)
# embeddings = download_hugging_face_embeddings()


# pc = Pinecone(api_key=PINECONE_API_KEY)

# index_name = "medibot"

# pc.create_index_for_model(
#         name=index_name,
#         cloud="aws",
#         region="us-east-1",
#         embed={
#             "model":"llama-text-embed-v2",
#             "field_map":{"text": "chunk_text"}
#         }
#     )
# # pc.create_index(
# #     name=index_name,
# #     dimension=384, 
# #     metric="cosine", 
# #     spec=ServerlessSpec(
# #         cloud="aws", 
# #         region="us-east-1"
# #     ) 
# # ) 

# docsearch = PineconeVectorStore.from_documents(
#     documents=text_chunks,
#     index_name=index_name,
#     embedding=embeddings, 
# )



from src.helper import load_pdf_file, text_split, download_hugging_face_embeddings
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os
import time

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

extracted_data = load_pdf_file(data='C:/Users/abhis/Desktop/Projects/web/proj/New folder/MediBot-AI/Data')
text_chunks = text_split(extracted_data)
embeddings = download_hugging_face_embeddings()

pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "medibot"

# Check if index exists, if not create it
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,  # Make sure this matches your embedding model
        metric="cosine", 
        spec=ServerlessSpec(
            cloud="aws", 
            region="us-east-1"
        ) 
    )
    
    # Wait for index to be ready
    while not pc.describe_index(index_name).status['ready']:
        time.sleep(1)

docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings, 
)