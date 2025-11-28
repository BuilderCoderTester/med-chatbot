from langchain_google_genai import ChatGoogleGenerativeAI


def rewrite_query(question, llm, disease, question_type):
    prompt = f"""
Rewrite the following medical question ONLY for search retrieval.
Keep the query MEDICAL and SHORT.

Question: "{question}"
Disease: "{disease}"
Question Type: "{question_type}"

Rules:
- Use the disease name at the beginning.
- Add search keywords based on the question type.

Keywords by type:
- what → definition overview description
- symptoms → symptoms signs clinical features
- diagnosis → diagnosis tests investigation identification
- treatment → treatment management therapy medication surgery
- prevention → prevention avoid risk reduction
- side_effects → side effects adverse reaction
- medication → dosage drug safety administration
- risk → complications danger prognosis mortality
- emergency → emergency first aid immediate action

Return ONLY the rewritten query, no explanation.
    """
    return llm.invoke(prompt).content.strip()



def check_question_type_llm(question: str, llm):
    prompt = f"""
You are a medical question classifier. Analyze the user's question.

Question: "{question}"

You must determine THREE things:

1. question_type → what the user is asking for.
Possible types:
- symptoms, treatment, diagnosis, prevention, cause, risk, side_effects,
  medication, diet, test, emergency, what, why, how, other

2. subject → which medical specialty the question relates to.
Possible subjects:
- cardiology, neurology, pulmonology, gastroenterology, nephrology,
  endocrinology, dermatology, pediatrics, gynecology, oncology,
  orthopedics, psychiatry, infectious_disease, general

3. disease → the disease, condition, or medical topic being asked about.
Rules:
- If multiple diseases are mentioned, pick the main one.
- If the disease/condition is not clear, return "unknown".
- For non-disease general terms like "fever", "pain", "headache", treat them as disease keywords.

Return only JSON in this format:
{{
  "question_type": "<type>",
  "subject": "<subject>",
  "disease": "<disease>"
}}
"""
    response = llm.invoke(prompt)
    print("step - 0")
    print(response)
    return response
   