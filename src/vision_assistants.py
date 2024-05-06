
from openai import OpenAI
from system_prompts import system_prompts
import base64
import requests
import os
from PIL import Image

# todo: several image comparisionn

client = OpenAI()

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.environ.get("OPENAI_API_KEY")}"
}


def encode_image(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        return f"data:image/jpeg;base64,{base64_image}"


def analyze_image(assistant, img_url, query):
    payload = {
        "model": "gpt-4-turbo",
        "messages": [
            {
            "role": "system",
            "content": system_prompts[assistant]
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": query
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": img_url
                }
                }
            ]
            }
        ],
        "max_tokens": 3000
        }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    #print(response.json)
    return response


def main():
    print("---- GPT-4 Vision ----")
    while True:
        a = ''
        while a not in system_prompts:
            a = input("Choose an assistant " + ", ".join(system_prompts.keys()) + ": ")
        img_set = False
        while not img_set:
            try:
                i = input("Image url or image name: ")
                if "http" not in i:
                    path = "src/img/" + i
                    i = encode_image(path)
                    img = Image.open(path)
                    img.show()
                img_set = True
            except:
                print("No such image.")
        q = input("Query: ")
        
        response = analyze_image(a, i, q)
        try:
            json = response.json()
        except Error as e:
            print(f"Error: {e.args[0]}")
            print(response)
        print("\n", json["choices"][0]["message"]["content"])
        
    
    
if __name__=='__main__':
    main()
