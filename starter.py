import sys
import time
import logging
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import MetadataMode
from transformers import AutoModel, AutoTokenizer

#from transformers import CodeT5p_Embedding
#model = CodeT5p_Embedding.from_pretrained("Salesforce/codet5p-110m-embedding", trust_remote_code=True)

DEVICE = "cpu"  # for GPU usage or "cpu" for CPU usage

#tokenizer = AutoTokenizer.from_pretrained(CODET5_EMB, trust_remote_code=True)
#model = AutoModel.from_pretrained(CODET5_EMB, trust_remote_code=True).to(DEVICE)

PROMPT_FILE = "prompt.txt"
OUTPUT_FILE = "out.txt"
RAG_RESULT_FILE = "ragprompt.txt"

LLAMA_LLM     = "llama3"
MOONDREAM_LLM = "moondream"
DEEPSEEK_LLM  = "deepseek-coder-v2"
CODELLAMA_LLM = "codellama"

CODET5_EMB = "Salesforce/codet5p-110m-embedding"
BGE_EMB    = "BAAI/bge-base-en-v1.5"
SFR_EMB    = "Salesforce/SFR-Embedding-2_R"

CHUNK = 512

STAR_LINE = "**************************************"

#logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
#logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

log("reading directory")
documents = SimpleDirectoryReader("quad", recursive=True).load_data()
#print(documents)

#inputs = tokenizer.encode(documents, return_tensors="pt").to(DEVICE)
#embedding = model(inputs)[0]

log("setting model")
Settings.embed_model = HuggingFaceEmbedding(model_name="codesage/codesage-small", trust_remote_code=True)

#Settings.embed_model = model
#Settings.tokenizer = tokenizer

log("setting llm")
Settings.llm = Ollama(model=LLAMA_LLM, request_timeout=360.0)
#Settings.num_output = 512

log("setting parser")
text_splitter = SentenceSplitter(separator=" ", chunk_size=CHUNK, chunk_overlap=10)
Settings.text_splitter = text_splitter

log("indexing")
start_index_time = time.time()
index = VectorStoreIndex.from_documents(documents, transformations=[text_splitter])
index_time = time.time() - start_index_time

#retriever = index.as_retriever()
#nodes = retriever.retrieve("Who is Paul Graham?")

log("building query engine")
query_engine = index.as_query_engine(streaming=True)

log("asking question")
in_stream = open(PROMPT_FILE, "r")
prompt = in_stream.read()
in_stream.close()

out_stream = open(OUTPUT_FILE, "w")
rag_stream = open(RAG_RESULT_FILE, "w")


for i in range(1):
    start_query_time = time.time()
    response = query_engine.query(prompt)
    query_time = time.time() - start_query_time

    response.print_response_stream()
    out_stream.write(response.__str__())
    rag_stream.write(response.get_formatted_sources(CHUNK))

    print("\nQUERY TIME: ", query_time)


out_stream.close()
rag_stream.close()

print("INDEXING TIME: ", index_time)

def log(name: str) -> None:
    print(STAR_LINE)
    print(name)
    print(STAR_LINE)
