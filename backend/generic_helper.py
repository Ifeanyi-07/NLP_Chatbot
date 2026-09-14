import re


def extract_session_id(session_str: str):
    match = re.search(r"/sessions/(.*?)/contexts/", session_str)
    if match:
        extracted_string = match.group(1)
        return extracted_string

    return ""

def get_str_from_food_dict(food_dict: dict):
    result = ", ".join([f"{int(value)} {key}" for key, value in food_dict.items()])
    return result

# if __name__ == "__main__":
#     # print(extract_session_id("projects/oai-chatbot-yael/agent/sessions/9574848/contexts/ongoing-order"))
#     print(get_str_from_food_dict({"samosa": 2, "pizza": 8}))