from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core.node_parser import SentenceSplitter

text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=10)

# global

Settings.text_splitter = text_splitter

documents = SimpleDirectoryReader("data", recursive=True).load_data()

# bge-base embedding model
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

# ollama
Settings.llm = Ollama(model="llama3", request_timeout=360.0)

# per-index
index = VectorStoreIndex.from_documents(documents, transformations=[text_splitter])

query_engine = index.as_query_engine()
response = query_engine.query("What did the author do growing up?")
print(response)
