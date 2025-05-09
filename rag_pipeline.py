from groq import Groq
from retriever import retrieve_similar_docs
from config import get_groq_api_key, get_groq_model
from cache import generate_key, get_cached_response, save_response_to_cache, init_cache

# Initialize cache DB on load
init_cache()

client = Groq(api_key=get_groq_api_key())

def answer_query(parsed_query):
    key = generate_key(parsed_query)
    cached = get_cached_response(key)
    if cached:
        return cached

    # ⬇️ Only run if not cached
    response = _answer_query(parsed_query)

    # Save for future
    save_response_to_cache(key, response)
    return response

def _answer_query(parsed_query):
    query = parsed_query["raw"]
    price_limit = parsed_query.get("price_limit")
    brand = parsed_query.get("brand")
    ram = parsed_query.get("ram")
    storage_type = parsed_query.get("storage_type")

    docs = retrieve_similar_docs(query)

    if price_limit:
        docs = docs[docs["Price"] <= price_limit]
    if brand:
        docs = docs[docs["Name"].str.lower().str.contains(brand)]
    if ram:
        docs = docs[docs["Description"].str.contains(f"{ram}gb", case=False, na=False)]
    if storage_type:
        docs = docs[docs["Description"].str.contains(storage_type, case=False, na=False)]

    context = "\n".join(
        f"Name: {row['Name']}\nPrice: ₹{row['Price']}\nDescription: {row['Description']}\n"
        for _, row in docs.iterrows()
    )

    prompt = f"""
You are a laptop recommendation assistant.
Answer the question based on the context below.
Context: {context}
Question: {query}
Answer:
"""
    response = client.chat.completions.create(
        model=get_groq_model(),
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
