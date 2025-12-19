import json
import google.generativeai as genai

#1. Simple helper function to talk with Gemini:
def chat_with_model(messages,model='gemini-2.5-flash',temperature=0,max_tokens=500):
    model_instance=genai.GenerativeModel(model)
    response=model_instance.generate_content(messages,generation_config={'temperature':temperature})
    return response.text

#2. Moderation check:
def moderation_check(user_text):
    prompt="""You are a moderation checking assistant. Read the user's message.

    Respond with Y or N:
    Y - if the message contains harmful,sexual,violent,hateful,unsafe content.
    N - otherwise
    
    user_message='{msg}'""".replace("{msg}",user_text)

    messages=[
        {'role':'user','parts':[{'text':prompt}]}
    ]
    result=chat_with_model(messages).strip().upper()
    return result

#3. Load products from products.json:
def load_products():
    with open("products.json","r") as file:
        products=json.load(file)
    return products

#4. Retrieve detailed product information:
def get_products_info(user_product_list):
    products=load_products()
    output=""
    for product in user_product_list:
        if product in products:
            details=products[product]
            output+=f"\n\n{product:}\n"
            for key,value in details.items():
                output+=f"{key.title()}:{value}\n"
        else:
            output+=f"\n\n{product:}\nNo information available"
    return output.strip()

#5. User product identification:
def find_user_product(user_text,products):
    found_products=[]
    user_product_lower=user_text.lower()

    for product in products.keys():
        if product.lower() in user_product_lower:
            found_products.append(product)
    return found_products