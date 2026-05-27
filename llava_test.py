from ollama import chat, ChatResponse

image_path = "computer_image.jpg"

history = []

def add_history():
    


def llava(message: str, image: str = None, model: str = "LLaVA") -> ChatResponse:
    if image == None:
        response = chat(model=model, messages=[
            {
                'role': 'user',
                'content': message
            }
        ])
    else:
        response = chat(model=model, messages=[
            {
                'role': 'user',
                'content': message,
                'images': [image]
            }
        ])

    return response


while True:
    query = input("> ")
    image = image_path

    if query == "":
        break
    if query[-1] == "0":
        print("NO IMAGE")
        image = None

    if query[-2] == "0":
        print("MOONDREAM")
        response = llava(query, image, model="moondream")
    else:
        response = llava(query, image)
    
    print(":", response.message.content)
    print()




    if response.message.images != None:
        print(response.message.images)
