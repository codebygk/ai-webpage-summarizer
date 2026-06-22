import os
import time

from openai import OpenAI
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://api.openai.com/v1")
API_KEY = os.getenv("API_KEY")
MODEL = os.getenv("MODEL")

class WebpageSummarizer:
    def __init__(self, url: str):
        self.url = url
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")
        self.title = soup.title if soup.title else "Title not found"
        irrelevant_tags = ["script", "style", "img", "input"]
        for tag in soup.body(irrelevant_tags):
            tag.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)

    def get_summarize_messages(self):
        system_prompt = ("You are an assistant that analyzes the contents of a website and provides a short summary, "
                         "ignoring text that might be navigation related. Respond in markdown.")
        user_prompt = (f"You are looking at a website titled {self.title}."
                       f"The contents of this website is as follows; "
                       f"Please provide a short summary of this website in markdown. "
                       f"If it includes news or announcements, then summarize these too. {self.text}")
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        return messages

    def summarize(self):
        client = OpenAI(base_url=BASE_URL, api_key=API_KEY)
        messages = self.get_summarize_messages()
        response = client.chat.completions.create(model=MODEL, messages=messages, stream=True)
        print()  # Initial newline before streaming starts
        for chunk in response:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
        print()  # final newline after streaming finishes


def is_url_valid(url: str) -> bool:
    parsed = urlparse(url)
    return all([parsed.scheme, parsed.netloc])

def is_url_reachable(url: str) -> bool:
    try:
        response = requests.head(url, timeout=3)
        return response.status_code < 400
    except requests.RequestException:
        return False

def prompt_for_url():
    while True:
        url = input("Enter the URL of the page to summarize: ").strip().lower()
        if not is_url_valid(url):
            print("❌ Invalid URL. Please enter a valid URL (e.g. https://example.com)")
            continue
        if not is_url_reachable(url):
            print("❌ Webpage in the given URL is not reachable. Retry with a different URL.")
            continue
        print(f"✅ Selected URL: {url}")
        return url

def confirm_input(prompt, default='y'):
    while True:
        choice = input(prompt).strip().lower()
        if choice == '':
            return default == 'y'
        if choice in ('y', 'yes'):
            return True
        if choice in ('n', 'no'):
            return False
        print("Invalid input — please enter 'y' or 'n'.")

def main():
    while True:
        try:
            url = prompt_for_url()
            webpage_summarizer = WebpageSummarizer(url)
            print("Initializing Summarizer...")
            print(f"Please wait while {MODEL} summarizes the webpage. This might take a while...")
            start = time.time()
            webpage_summarizer.summarize()
            end = time.time()
            # Calculate elapsed time in seconds
            elapsed_seconds = end - start
            print(f"\n{MODEL} summarized the webpage in {elapsed_seconds:.4f} seconds.")
            if confirm_input("Do you want to summarize another page? (Y/n): "):
                print("Restarting Summarizer...")
                continue
            else:
                print("Restarting canceled by user.")
                break
        except Exception as e:
            print(f"❌ Failed to summarize the webpage. Exception: {e}")
            if confirm_input("Do you want to retry? (Y/n): "):
                print("Retrying Summarizer...")
                continue
            else:
                print("Retry canceled by user.")
                break
    print("Exiting Summarizer. Goodbye.")


if __name__ == '__main__':
    main()
