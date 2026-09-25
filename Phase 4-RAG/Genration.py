import os  
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm =ChatGroq(
    api_key=os.getenv("API_KEY"),
    model="openai/gpt-oss-120b",
    temperature=0
)




import chromadb

client=chromadb.Client()

collection=client.create_collection(
    name="OrgX_Rag"
)

from pypdf import PdfReader
from pathlib import Path
from sentence_transformers import SentenceTransformer

Base_dir=Path(__file__).resolve().parent
pdf_path=Base_dir/"Sample_Data"/"OrgX_Sample_Project_Requirement.pdf"

reader=PdfReader(pdf_path)

text=""

for page in reader.pages:
    text+=page.extract_text() + "\n"


######### Chuncking ######################

chunk_size=500
overlap=100
chunks=[]

start=0

while start<len(text):
    end=start+chunk_size
    chunk=text[start:end]
    chunks.append(chunk)

    start += chunk_size-overlap



####################### Embedding #####################################
model =SentenceTransformer("all-MiniLM-L6-v2")
chunk_embeddings=model.encode(chunks)

print(chunk_embeddings.shape)


#########################################################
metadatas=[]
for i in range(len(chunks)):
    metadatas.append({
        "source":"CampusConnect",
        "chunk":i
    })
ids=[f"chunk_{i}" for i in range(len(chunks))]
collection.add(
    ids=ids,
    documents=chunks,
    embeddings=chunk_embeddings.tolist(),
    metadatas=metadatas
)

query = "What is the payment gateway used by CampusConnect?"

query_embedding = model.encode(query)

results = collection.query(
    query_embeddings=[query_embedding.tolist()],
    n_results=2,
    
)



context = "\n\n".join(results["documents"][0])

prompt = f"""
Answer the question using ONLY the provided context.

Context:
{context}

Question:
{query}

Answer
"""

response=llm.invoke(prompt)
print(response.content)