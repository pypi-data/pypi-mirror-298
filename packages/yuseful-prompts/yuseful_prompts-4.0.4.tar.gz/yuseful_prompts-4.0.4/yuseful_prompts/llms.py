from langchain_community.chat_models import ChatOllama

DEFAULT_MODEL = "llama3.1" 
# tests performance (2024-09-28) => 12/12 in 15.36s (categories) | 41/43 in 22.72s (headlines)

def get_json_local_model(model_name: str = DEFAULT_MODEL):
    return ChatOllama(model=model_name, format="json", temperature=0)


def get_text_local_model(model_name: str = DEFAULT_MODEL):
    return ChatOllama(model=model_name, temperature=0)
