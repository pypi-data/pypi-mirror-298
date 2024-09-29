
## **ABOUT**

#### `verba` is a framework for working with LLMs and performing NLP tasks. It is designed to offer an alternative to the overly-abstracted methods found in commercialized packages such as **langchain**.


### ----------------------------


####  **LICENSE**
***GPL-3 Summary:***

_You may copy, distribute and modify the software as long as you track changes/dates in source files. Any modifications to or software including (via compiler) GPL-licensed code must also be made available under the GPL along with build & install instructions. In other words, **any derivative work of this software shall be released under the same GPL license as the original software, meaning the modified code must be exactly as free and open-source as the original**._


### ----------------------------


## **INSTALL**

#### **verba** is installed using pip:

`pip install verba`

### **NOTE**: In order to utilize LLM functionality you need ***Ollama*** and the ***Ollama Python*** package installed on your machine.

#### SEE: 
- `https://ollama.com/download`
- `https://github.com/ollama/ollama-python`


### ----------------------------


## **Ragby**: **R**etrieval-**A**ugmented **G**eneration (RAG) **B**y **Y**ourself
- #### A collection of RAG-related methods

### -----------

### **STEP 1) Import & Initialize:**

```
from verba.OllamaHelper import Ragby

ragby = Ragby(chat_model = "llama3", embedding_model = "llama3")
```

### **STEP 2) Create Chunks:**
- First place your input data file (.txt or .pdf) in a directory named **data**
- Run:

```
# for .txt files:
chunks_obj, chunks_path = ragby.make_chunks("my-txt-file.txt")

# for .pdf files:
chunks_obj, chunks_path = ragby.make_chunks_pdf("my-pdf-file.pdf")
```
- A directory named **chunks** will be created, containing the two returned objects

### **STEP 3) Create Embeddings:**
- Run:

```
embeddings_path = ragby.make_embeddings(chunks_obj, "my-txt-file.txt")
```
- A directory named **embeddings** will be created, containing the returned object

### **STEP 4) Create a System Prompt that is relevant to your output:**

```
SYSTEM_PROMPT = "You are a helpful assistant who answers questions using only the provided CONTEXT. Be as concise as possible. If you are unsure, just say 'I don't know'.\n\nCONTEXT:\n"
```

### **STEP 5) Run:**

```
CHAT = ragby.chat(
    user_prompt = "What is the summary of this article?", 
    system_prompt = SYSTEM_PROMPT, 
    text_chunks_path = chunks_path, 
    text_embeddings_path = embeddings_path, 
)

print(CHAT)
```


