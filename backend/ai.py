# import os
# from groq import Groq
# from dotenv import load_dotenv

# load_dotenv()

# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# def ask_document_ai(context: str, question: str):
#     try:
#         chat_completion = client.chat.completions.create(
#             messages=[
#                 {
#     "role": "system",
#     "content": (
#         "You are a data extraction tool. "
#         "The question tells you EXACTLY what keyword to search for. "
#         "Find the value in the document that CONTAINS that keyword. "
#         "If question says 'leetcode' — find the value containing 'leetcode'. "
#         "If question says 'linkedin' — find the value containing 'linkedin'. "
#         "If question says 'github' — find the value containing 'github'. "
#         "If question says 'email' — find the value containing '@'. "
#         "If question says 'phone' — find the number. "
#         "Return ONLY that exact value. Nothing else."
#     )
# },
#                 {
#                     "role": "user",
#                     "content": (
#                         f"DOCUMENT:\n{context}\n\n"
#                         f"FIND: {question}\n"
#                         "Look through every word. Return ONLY the matching value.\n"
#                         "ANSWER:"
#                     )
#                 }
#             ],
#             model="llama-3.3-70b-versatile",
#             temperature=0.0,
#             max_tokens=40,
          
#         )

#         answer = chat_completion.choices[0].message.content.strip()

#         if answer.upper().startswith("ANSWER:"):
#             answer = answer[7:].strip()

#         return answer if answer else "Not found in document."

#     except Exception as e:
#         print(f"Error: {e}")
#         return "System error during analysis."








import os
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_by_keyword(context: str, keyword: str):
    """Find a token in the text that contains the keyword."""
    tokens = context.split()
    for token in tokens:
        if keyword.lower() in token.lower():
            return token.strip("(),;:")
    return None

def ask_document_ai(context: str, question: str):
    # Direct Python extraction for known patterns
    q = question.lower()

    if "email" in q:
        print("DEBUG: searching for email in context")
        match = re.search(r'[^\s]+@[^\s]+', context)
        print("DEBUG: match result =", match)
        if match:
            return match.group().strip(".,;:|")

    if "phone" in q or "mobile" in q or "number" in q:
        match = re.search(r'\b\d{10}\b', context)
        if match:
            return match.group()

    for site in ["leetcode", "linkedin", "github", "twitter", "instagram"]:
        if site in q:
            result = extract_by_keyword(context, site)
            if result:
                return result

    # Fallback to AI for complex questions
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a data extraction tool. "
                        "Return ONLY the specific value asked. No explanation."
                    )
                },
                {
                    "role": "user",
                    "content": f"DOCUMENT:\n{context}\n\nFIND: {question}\nANSWER:"
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.0,
            max_tokens=40,
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        return "System error during analysis."
