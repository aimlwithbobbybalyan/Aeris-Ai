from AppOpener import close, open as appopen  # Import functions to open and close apps.
from webbrowser import open as webopen  # Import and browser functionality.
from pywhatkit import search, playonyt  # Import functions for Google search and YouTube playback.
from dotenv import dotenv_values  # Import dotenv to manage environment variables.
from bs4 import BeautifulSoup  # Import BeautifulSoup for parsing HTML content.
from rich import print  # Import rich for styled console outputs.
from groq import Groq  # Import Groq for AI chat functionalities.
import webbrowser  # Import subprocess for opening URLs.
import subprocess  # Import subprocess for interacting with the system.
import requests  # Import requests for making HTTP requests.
import keyboard  # Import keyboard for keyboard-related actions.
import asyncio  # Import asyncio for asynchronous programming.
import os  # Import os for operating system functionalities.

fallback_urls = {
    "facebook": "https://www.facebook.com",
    "instagram": "https://www.instagram.com",
    "twitter": "https://twitter.com",
    "linkedin": "https://www.linkedin.com",
    "youtube": "https://www.youtube.com",
    "gmail": "https://mail.google.com"
}



# Load environment variables from the .env file.
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")  # Retrieve the Groq API key.

# Define CSS classes for parsing specific elements in HTML content.
classes = ["zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta",
           "IZ6rdc", "O5uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table_webanswers-table", "dDoNo ikb4Bb gsrt", "sXLaOe", "LWKfke", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

# Define a user-agent for making web requests.
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

client = Groq(api_key=GroqAPIKey)  # Initialize the Groq client with the API key.

professional_responses = [
    "Your satisfaction is my priority; feel free to reach out if there's anything else i can help you with.",
    "I'm at your service for any dditional questions or support you may need-don't hesitate to ask.",
]

messages = []

SystemChatbot =[ {"role": "system", "content": f"Hello, I am {os.environ['Username'] }, You're a content writer . You have to write content like letter "},]

def GoogleSearch(Topic):
    search(Topic)
    return True



def Content(Topic):

    def OpenNotepad(File):
        default_text_editor = 'notepad.exe'  # Default text editor
        subprocess.Popen([default_text_editor, File])

    #Nested function to handle the content using Ai chatbot
    def ContentWriterAi(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})

        completion =client.chat.completions.create(
            model = "llama3-70b-8192",
            messages =SystemChatbot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream = True,
            stop = None
        )

        Answer = ""

        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})
        return Answer
    
    Topic: str = Topic.replace("Content ", "")
    ContentByAI = ContentWriterAi(Topic)

    with open(rf"Data\{Topic.lower().replace(' ', '')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI)
        file.close()

        OpenNotepad(rf"Data\{Topic.lower().replace(' ', '')}.txt")
        return True
    
def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True



def PlayYouTube(query):
    playonyt(query)
    return True



def openApp(app, sess=requests.session()):
    try:
        # Attempt to open app
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True

    except Exception as e:
        print(f"[red]Error opening '{app}': {e}[/red]")

        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a', href=True)
            clean_links = []

            for link in links:
                href = link['href']
                if href.startswith("/url?q="):
                    actual_url = href.split("/url?q=")[1].split("&")[0]
                    if actual_url.startswith("http"):
                        clean_links.append(actual_url)
            return clean_links

        def search_google(query):
            url = f"https://www.google.com/search?q={query}"
            headers = {"User-Agent": useragent}
            response = sess.get(url, headers=headers)
            return response.text if response.status_code == 200 else None

        html = search_google(query=f"{app} official site")
        links = extract_links(html)

        if links:
            print(f"[yellow]App '{app}' not found. Opening in browser instead.[/yellow]")
            webbrowser.open(links[0])
        elif app.lower() in fallback_urls:
            print(f"[yellow]Using fallback URL for '{app}'[/yellow]")
            webbrowser.open(fallback_urls[app.lower()])
        else:
            print(f"[red]No suitable web link found for '{app}'.[/red]")

        return False




def CloseApp(app):
    if "chrome" in app:
        pass
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)
            return True
        except:
            return False
        
def System(command):

    def mute():
        keyboard.press_and_release('volume_mute')

    def unmute():
        keyboard.press_and_release('volume_unmute')

    def volume_up():
        keyboard.press_and_release('volume_up')

    def volume_down():
        keyboard.press_and_release('volume_down')

    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()

    return True


async def TranslateAndExecute(commands: list[str]):

    funcs = []

    for command in commands:

        if command.startswith("open"):

            if "open it" in command:
                pass
            if "open file" == command:
                pass

            else:
                fun = asyncio.to_thread(openApp, command.removeprefix("open "))
                funcs.append(fun)

        elif command.startswith("general "):
            pass

        elif command.startswith("realtime "):
            pass

        elif command.startswith("close "):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
            funcs.append(fun)

        elif command.startswith("play "):
            fun = asyncio.to_thread(PlayYouTube, command.removeprefix("play "))
            funcs.append(fun)

        elif command.startswith("content "): 
            fun = asyncio.to_thread(Content, command.removeprefix("content "))
            funcs.append(fun)

        elif command.startswith("google search "):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))
            funcs.append(fun)

        elif command.startswith("youtube search "):
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search "))
            funcs.append(fun)

        elif command.startswith("system "):
            fun = asyncio.to_thread(System, command.removeprefix("system "))
            funcs.append(fun)
        
        else:
            print(f"No Function Found. For {command}")

    results = await asyncio.gather(*funcs)

    for result in results:
        if isinstance(result, str):
            yield result
        else:
            yield result 


async def Automation(commands: list[str]):
    
    async for result in  TranslateAndExecute(commands):
        pass

    return True

