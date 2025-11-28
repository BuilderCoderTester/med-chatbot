import json
import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
from langchain_cohere import CohereRerank
from langchain_classic.retrievers.contextual_compression import ContextualCompressionRetriever

from querry.query_rewrite import rewrite_query, check_question_type_llm


load_dotenv()


def create_rag_chain(vector_store, question_type, subject, disease, search_k: int = 20):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2,
        max_output_tokens=1024
    )

    base_retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": search_k}
    )

    cohere_api_key = os.getenv("COHERE_API_KEY")
    reranker = CohereRerank(cohere_api_key=cohere_api_key,
                            model="rerank-multilingual-v3.0",
                            top_n=5)

    retriever = ContextualCompressionRetriever(
        base_compressor=reranker,
        base_retriever=base_retriever
    )

    system_prompt = f"""
You are a highly reliable medical assistant.

Question Type: {question_type}
Medical Subject: {subject}
Disease/Condition: {disease}

Use ONLY the retrieved context to answer the question.

Answer Requirements:
- The answer MUST match the question type.
- Keep the explanation medically safe and reliable.
- Do not hallucinate beyond the retrieved context.

If the context does not contain the answer, reply exactly:
"I don't have enough information in the medical database to answer this."

{{context}}
"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    print("RAG chain ready with: Gemini + Pinecone + Cohere Reranking 🔥")
    return rag_chain


def query_rag_chain(vector_store, question: str):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2,
        max_output_tokens=1024
    )

    # 1️⃣ Classify question
    classification = check_question_type_llm(question, llm)
    classification_json_string = classification.content  # <-- FIX
    classification_json_string = classification_json_string.replace("```json", "").replace("```", "").strip()

    classification = json.loads(classification_json_string)
    question_type = classification["question_type"]
    subject = classification["subject"]
    disease = classification["disease"]
    print("step -1")
    print("\n📌 Classification =", classification)

    # 2️⃣ Rewrite question for search
    rewritten_query = rewrite_query(question,llm,disease,question_type)
    print("step -2")

    print("\n🔍 Rewritten search query =", rewritten_query)

    # 3️⃣ Build RAG chain using classification
    rag_chain = create_rag_chain(vector_store, question_type, subject, disease)

    # 4️⃣ Invoke RAG
    response = rag_chain.invoke({"input": rewritten_query})
    return response
