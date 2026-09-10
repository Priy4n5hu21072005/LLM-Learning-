from transformers import AutoTokenizer
tokenizer=AutoTokenizer.from_pretrained("bert-base-uncased")

text="AI TAKE SOFTWARE ENGINEER JOBS "
token=tokenizer.tokenize(text)



tokens_id=tokenizer.convert_tokens_to_ids(token)

output=tokenizer(text)
print(output)

