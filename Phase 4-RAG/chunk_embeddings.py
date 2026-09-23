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


model =SentenceTransformer("all-MiniLM-L6-v2")
chunk_embeddings=model.encode(chunks)

print(chunk_embeddings.shape)


