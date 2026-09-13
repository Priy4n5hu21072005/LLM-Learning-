from dotenv import load_dotenv
from groq import Groq


load_dotenv()
api_key="YOUR_GROQ_API_KEY"

client = Groq(
    api_key=api_key
)

models = client.models.list()

for model in models.data:
    print(model.id)
