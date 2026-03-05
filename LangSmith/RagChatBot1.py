import os
from dotenv import load_dotenv, find_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)

from langchain_community.vectorstores import Chroma

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda
)

from langchain_core.output_parsers import StrOutputParser

# ---------------------------------------
# Load API key
# ---------------------------------------

load_dotenv(find_dotenv())

# ---------------------------------------
# PDF path
# ---------------------------------------

PDF_PATH = r"F:\Projects\AI-Project\LangGraph\AI-Agent-LangGraph\LangSmith\FineTuningLLM.pdf"

# ---------------------------------------
# 1. Load PDF
# ---------------------------------------

loader = PyPDFLoader(PDF_PATH)
docs = loader.load()

print(f"Loaded {len(docs)} pages")


# ---------------------------------------
# 2. Split into chunks
# ---------------------------------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=200
)

splits = splitter.split_documents(docs)

print(f"Created {len(splits)} chunks")


# ---------------------------------------
# 3. Create Embeddings
# ---------------------------------------

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001"
)


# ---------------------------------------
# 4. Create Vector Database
# ---------------------------------------

vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)


# ---------------------------------------
# 5. Gemini LLM
# ---------------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2
)


# ---------------------------------------
# 6. Prompt Template
# ---------------------------------------

prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer ONLY using the provided context. If the answer is not in the context, say 'I don't know'."),
    ("human", "Question: {question}\n\nContext:\n{context}")
])


# ---------------------------------------
# Helper function
# ---------------------------------------

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# ---------------------------------------
# 7. Build RAG Chain
# ---------------------------------------

parallel = RunnableParallel({
    "context": retriever | RunnableLambda(format_docs),
    "question": RunnablePassthrough()
})

chain = parallel | prompt | llm | StrOutputParser()


# ---------------------------------------
# 8. Chat Loop
# ---------------------------------------

print("\n RAG Chatbot Ready. Ask questions from your PDF.")
print("Type 'exit' to quit.\n")

while True:

    question = input("Q: ")

    if question.lower() in ["exit", "quit"]:
        break

    answer = chain.invoke(question)

    print("\nA:", answer)
    print("\n" + "-"*60 + "\n")