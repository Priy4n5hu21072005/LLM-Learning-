import os
from dotenv import load_dotenv

load_dotenv()
from pathlib import Path
from llama_index.readers.file import PDFReader
from llama_index.core.node_parser import SentenceSplitter
Base_dir=Path(__file__).resolve().parent
pdf_path=Base_dir/".."/"Phase 4-RAG"/"Sample_Data"/"OrgX_Sample_Project_Requirement.pdf"
reader=PDFReader()
document=reader.load_data(file=pdf_path)

splitter=SentenceSplitter(
    chunk_size=100,
    chunk_overlap=30
)

nodes=splitter.get_nodes_from_documents(document)



from llama_index.embeddings.huggingface import HuggingFaceEmbedding

embed_model=HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
for node in nodes:
    node.embedding=embed_model.get_text_embedding(node.text)


from llama_index.llms.groq import Groq
from llama_index.core import VectorStoreIndex

index=VectorStoreIndex(nodes,embed_model=embed_model)

llm =Groq(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY")
)

from llama_index.core import Settings

Settings.llm=llm
Settings.embed_model=embed_model

query_engine=index.as_query_engine()

response=query_engine.query(
    "who can create and manage events? "
)

print(response)