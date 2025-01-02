import os
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
from openai import OpenAI
from IPython.display import Markdown, display

load_dotenv()

openai = OpenAI()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("No API key found")
elif not api_key.startswith("sk-proj-"):
    print("API is found. But, it is not start with sk-proj-. Please check the API key")
elif api_key.strip() != api_key:
    print(
        "An API key was found, but it looks like it might have space or tab characters at the start or end - please remove them"
    )
else:
    print("API key found and looks good so far!")


headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

class Website:
    def __init__(self, url):
        self.url = url
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No title Found"
        for irrelevent in soup.body(['script', 'style', 'imng', 'input']):
            irrelevent.decompose()

        self.text = soup.body.get_text(separator="\n", strip=True)


system_prompt = "You are an assistant that analyzes the contents of a website \
and provides a short summary, ignoring text that might be navigation related. \
Respond in markdown."


def user_prompt_for(website):
    user_prompt = f"You are looking at a website titled {website.title}"
    user_prompt += "\nThe contents of this website is as follows; \
please provide a short summary of this website in markdown. \
If it includes news or announcements, then summarize these too.\n\n"
    user_prompt += website.text
    return user_prompt


def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(website)}
    ]

def summarize(url):
    website = Website(url)
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages_for(website)
        ) 
    return response.choices[0].message.content

# def display_summary(url):
#     summary = summarize(url)
#     display(Markdown(summary))

print(summarize('https://www.blinkpayroll.com'))
