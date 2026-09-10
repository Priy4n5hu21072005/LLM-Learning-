# Practical LLM & Transformer Roadmap

## Goal

I have already completed the **theoretical basics of LLMs and Transformers**.  
The goal is to build practical understanding first and then move toward **LLM fine-tuning/training by the end of September**.

The learning path will focus on:

- Tokenization
- Embeddings
- Similarity search
- Vector databases
- RAG
- Hugging Face ecosystem
- Dataset preparation
- LoRA / QLoRA / PEFT
- Practical fine-tuning
- Basic LLM training concepts

---

# Roadmap

## Phase 1 — Tokenization
**Target: 10–12 September**

### Topics
- What tokenization does in an LLM pipeline
- Text → tokens → token IDs
- Token vocabulary
- Special tokens
- Padding
- Truncation
- Attention masks
- BPE
- WordPiece
- SentencePiece
- Hugging Face `AutoTokenizer`
- Inspecting tokens and token IDs
- Understanding what actually goes into a Transformer

### Practical Work
Build a small tokenizer experiment:

```text
Text
 ↓
Tokenizer
 ↓
Tokens
 ↓
Token IDs
 ↓
Attention Mask
```

---

## Phase 2 — Embeddings
**Target: 13–15 September**

### Topics
- Token embeddings vs text/document embeddings
- What an embedding represents
- Text → vector
- Embedding models
- Vector dimensions
- Cosine similarity
- Semantic similarity

### Practical Work
Build a small **semantic search system**:

```text
Documents
   ↓
Embeddings
   ↓
Vectors
   ↓
User Query
   ↓
Similarity Search
   ↓
Most Relevant Documents
```

---

## Phase 3 — Vector Databases
**Target: 16–18 September**

### Topics
- Why vector databases are needed
- Vector storage
- Similarity search
- Top-k retrieval
- Metadata
- Metadata filtering
- Collections
- Distance metrics
- ChromaDB
- FAISS
- Introduction to Qdrant

### Practical Work
Store document embeddings in a vector database and retrieve the most relevant documents for a query.

---

## Phase 4 — RAG
**Target: 19–22 September**

### Topics
- What RAG solves
- RAG architecture
- Document loading
- Document cleaning
- Chunking
- Chunk size
- Chunk overlap
- Embedding
- Vector database
- Retriever
- Context retrieval
- Prompt construction
- LLM response generation
- Top-k retrieval
- Metadata filtering
- Naive RAG
- Common RAG problems
- Hallucination
- Basic RAG evaluation

### Practical Project — RAG Chatbot

```text
PDF / Documents
       ↓
   Load & Clean
       ↓
     Chunking
       ↓
    Embeddings
       ↓
   Vector Database
       ↓
      Retriever
       ↓
Relevant Context
       ↓
       LLM
       ↓
     Answer
```

---

## Phase 5 — Hugging Face + Dataset Pipeline
**Target: 23–24 September**

### Topics
- Hugging Face ecosystem
- `transformers`
- `datasets`
- `tokenizers`
- Loading pretrained models
- Loading tokenizers
- Dataset loading
- Dataset cleaning
- Dataset formatting
- Train/validation split
- Tokenizing datasets
- Causal Language Modeling
- Model inference
- Text generation
- Generation parameters

### Practical Work

Build the complete preprocessing pipeline:

```text
Raw Dataset
    ↓
Cleaning
    ↓
Formatting
    ↓
Train / Validation Split
    ↓
Tokenization
    ↓
Tokenized Dataset
    ↓
Model
```

---

# Phase 6 — LoRA / QLoRA / PEFT
**Target: 25–27 September**

## Topics

### LoRA
- Why full fine-tuning is expensive
- Frozen base model
- Trainable adapter layers
- Low-rank adaptation
- LoRA parameters
- Rank
- Alpha
- Dropout

Conceptually:

```text
Base LLM
   ↓
Frozen Weights
   ↓
LoRA Adapter
   ↓
Train only adapter
```

### PEFT
- Parameter Efficient Fine-Tuning
- Hugging Face PEFT
- Adapter-based training

### QLoRA
- Quantization
- 4-bit models
- Why quantization reduces memory usage
- QLoRA vs LoRA
- Practical constraints

---

# Phase 7 — Actual LLM Fine-Tuning
**Target: 28–30 September**

### Topics
- Choosing a small open-source model
- Preparing the training dataset
- Tokenization
- Training configuration
- Batch size
- Learning rate
- Gradient accumulation
- Epochs
- Checkpoints
- Evaluation
- Loss
- Validation
- Saving adapters
- Loading the fine-tuned model
- Testing the model

### Complete Pipeline

```text
Dataset
   ↓
Cleaning
   ↓
Formatting
   ↓
Tokenization
   ↓
Base LLM
   ↓
LoRA / QLoRA
   ↓
Training
   ↓
Evaluation
   ↓
Adapter
   ↓
Inference
```

---

# Phase 8 — Basic LLM Training Concepts

After practical fine-tuning, understand the complete training picture.

### Topics
- Pretraining vs fine-tuning
- Next-token prediction
- Causal Language Modeling
- Training loss
- Cross-entropy
- Backpropagation
- Gradients
- Optimizers
- Learning rate
- Batch size
- Gradient accumulation
- Epochs
- Checkpointing
- Validation
- Perplexity
- Overfitting
- Underfitting

---

# Timeline

| Date | Focus |
|---|---|
| 10–12 Sep | Tokenization |
| 13–15 Sep | Embeddings + Similarity |
| 16–18 Sep | Vector Databases |
| 19–22 Sep | RAG |
| 23–24 Sep | Hugging Face + Dataset Pipeline |
| 25–27 Sep | LoRA / QLoRA / PEFT |
| 28–30 Sep | Practical Fine-Tuning |

---

# Technology Stack

## Core
- Python
- PyTorch
- Hugging Face Transformers

## NLP / LLM
- Hugging Face Tokenizers
- Hugging Face Datasets
- Sentence Transformers

## Vector Search
- ChromaDB
- FAISS
- Qdrant (later)

## Fine-Tuning
- PEFT
- LoRA
- QLoRA
- BitsAndBytes

---

# Hardware Strategy

Around **50 GB free storage** is available locally.

Important distinction:

```text
Storage → Models, datasets, cache, checkpoints
RAM     → Loading models and data
VRAM    → GPU training/inference memory
```

Therefore:

- Do not download unnecessarily large models.
- Start with small models.
- Use LoRA/QLoRA instead of full fine-tuning.
- If local hardware is insufficient, use Google Colab/Kaggle GPU.
- Keep large model caches and unnecessary checkpoints under control.

### Model-size strategy

| Model Size | Approach |
|---|---|
| 0.5B–1B | Best starting point |
| 1B–3B | Depends on RAM/GPU |
| 7B QLoRA | Hardware dependent |
| 7B Full Fine-Tuning | Not practical locally |
| 13B+ | Avoid for local training |

---

# Final Practical Goal

By the end of the roadmap, I should be able to understand and implement this complete pipeline:

```text
                    LLM WORKFLOW

Raw Text
   ↓
Tokenization
   ↓
Token IDs
   ↓
Embeddings
   ↓
Vector Representation
   ↓
Vector Database
   ↓
RAG / Retrieval
   ↓
LLM
   ↓
Generation


For Fine-Tuning:

Dataset
   ↓
Cleaning
   ↓
Tokenization
   ↓
Base LLM
   ↓
LoRA / QLoRA
   ↓
Training
   ↓
Evaluation
   ↓
Fine-Tuned Adapter
   ↓
Inference
```

## Learning Philosophy

Do not just memorize the concepts.

For every major topic:

1. Understand the concept
2. See the actual data flow
3. Implement it in Python
4. Inspect the output
5. Build a small practical project
6. Connect it to the next stage

The final objective is not just to know **what LoRA, RAG, embeddings, or vector databases are**, but to understand how they fit together in a real LLM system.
