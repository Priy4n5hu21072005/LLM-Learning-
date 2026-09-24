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

ids=[f"chunk_{i}" for i in range(len(chunks))]
collection.add(
    ids=ids,
    documents=chunks,
    embeddings=chunk_embeddings.tolist()
)

print("total chunk stored:",collection.count())


query = "Who can create and manage events?"

query_embedding=model.encode(query)

print(query_embedding.shape)



results = collection.query(
    query_embeddings=[query_embedding.tolist()],
    n_results=2
)

for i in range(2):
    print(f"\n--- Result {i+1} ---")
    print("Chunk ID:", results["ids"][0][i])
    print("Distance:", results["distances"][0][i])
    print("Content:")
    print(results["documents"][0][i])