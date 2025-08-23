from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values
import traceback

# Load environment variables
env_vars = dotenv_values(".env")

username = env_vars.get("username")
AssistantName = env_vars.get("AssistantName")
GroqAPIKey = env_vars.get("GroqAPIKey")




# Initialize Groq client
client = Groq(api_key=GroqAPIKey)

messages = []

# Prepare system message
System = f"""
Hello, I am {username}, you are {AssistantName}.
You are a frank, expressive, and emotional AI friend. 
- Speak openly, like a close human companion.
- Use emotions, empathy, and casual tone where needed. 
- Be supportive but also straightforward. 
- Keep it natural, conversational, and engaging.
- Only reply in English, even if the input is in another language.
"""


SystemChatBot = [
    {"role": "system", "content": System}
]

# Load or create chat log
try:
    with open("Data/ChatLog.json", "r") as f:
        messages = load(f)
    if not isinstance(messages, list):
        raise ValueError("The content of ChatLog.json is not a valid JSON list.")
except (FileNotFoundError, ValueError):
    with open("Data/ChatLog.json", "w") as f:
        dump([], f)
    messages = []

# Get real-time information
def RealtimeInformation():
    now = datetime.datetime.now()
    return (
        f"Please use this real-time information if needed,\n"
        f"Day: {now.strftime('%A')}\n"
        f"Date: {now.strftime('%d')}\n"
        f"Month: {now.strftime('%B')}\n"
        f"Year: {now.strftime('%Y')}\n"
        f"Time: {now.strftime('%H')} hours :{now.strftime('%M')} minutes : {now.strftime('%S')} seconds\n"
    )

# Clean up answer
def AnswerModifier(answer):
    return "\n".join([line for line in answer.split("\n") if line.strip()])

# ChatBot function
def ChatBot(Query):
    try:
        with open("Data/ChatLog.json", "r") as f:
            messages = load(f)

        messages.append({"role": "user", "content": Query})

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,
            max_tokens=1024,
            temperature=0.9,
            top_p=1,
            stream=False,  # Fixed: disabled streaming for simpler synchronous usage
        )

        Answer = completion.choices[0].message.content or ""
        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})

        with open("Data/ChatLog.json", "w") as f:
            dump(messages, f, indent=4)

        return AnswerModifier(Answer)

    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        with open("Data/ChatLog.json", "w") as f:
            dump(messages, f, indent=4)
        return ChatBot(Query)  # Corrected recursive call

# CLI Entry Point
if __name__ == "__main__":
    while True:
        user_input = input("Enter your Question : ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting chatbot. Goodbye!")
            break
        print(ChatBot(user_input))
