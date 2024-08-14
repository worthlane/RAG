import sys
import time
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import MetadataMode

import logging
import sys

PROMPT_FILE = "prompt.txt"
OUTPUT_FILE = "out.txt"

STAR_LINE   = "**************************************"

def log(name: str) -> None:
    print(STAR_LINE)
    print(name)
    print(STAR_LINE)


#logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
#logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

log("reading directory")
documents = SimpleDirectoryReader("quad", recursive=True).load_data()

log("setting model")
# bge-base embedding model
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

log("setting llm")
# ollama
Settings.llm = Ollama(model="llama3", request_timeout=360.0) #, max_tokens=512)
#Settings.num_output = 512

log("setting parser")
text_splitter = SentenceSplitter(separator=" ", chunk_size=512, chunk_overlap=10)
Settings.text_splitter = text_splitter

log("indexing")
start_index_time = time.time()
# per-index
index = VectorStoreIndex.from_documents(documents, transformations=[text_splitter])
index_time = time.time() - start_index_time

#retriever = index.as_retriever()
#nodes = retriever.retrieve("Who is Paul Graham?")

log("building query engine")
query_engine = index.as_query_engine(streaming=False)

log("asking question")
in_stream = open(PROMPT_FILE, "r")
prompt = in_stream.read()
in_stream.close()

start_query_time = time.time()
response = query_engine.query(prompt)
query_time = time.time() - start_query_time


#response = query_engine.query("What did the author do growing up?")

#log("giving response")
#response.print_response_stream()

out_stream = open(OUTPUT_FILE, "w")
out_stream.write(response.__str__())
out_stream.close()

print("INDEXING TIME: ", index_time)
print("QUERY    TIME: ", query_time)

#print("--------------------------------------------------------\n",
#       response,
#      "\n--------------------------------------------------------")
