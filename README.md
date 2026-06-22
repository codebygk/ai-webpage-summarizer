# Webpage Summarizer

A full-featured AI webpage analysis tool that fetches a webpage, extracts visible content, removes clutter, and generates a concise markdown summary using OpenAI.


## Features
- Fetches a webpage by URL.
- Removes navigation and irrelevant HTML content.
- Summarizes the page with OpenAI Chat Completions.
- Streams the summary output in real time.

## Requirements
- Python 3.9+
- uv package manager (https://docs.astral.sh/uv/getting-started/installation/) (Install and configure using documentation. Verify installation using `uv --version`)
- OpenAI-compatible API key
- Internet access to fetch webpages and call the OpenAI-compatible API

## Setup
Repository: [https://github.com/codebygk/ai-webpage-summarizer](https://github.com/codebygk/ai-webpage-summarizer)
1. Clone the repository and open the project folder.
2. Create a .env file in the project root.
3. Add the following variables to .env:

```shell
BASE_URL=your_openai_compatible_base_url
API_KEY=your_openai_compatible_api_key
MODEL=gpt-4o-mini
```

4. (Optional) Set BASE_URL if you need a custom OpenAI-compatible endpoint. By default it uses `https://api.openai.com/v1`.

5. Install project dependencies with uv:

```shell
uv install
```

## Usage
Run the script from the project directory:

```shell
uv run main.py
```

Then follow the prompts:
- Enter the URL of the page to summarize.
- Wait while the tool fetches the page and generates the summary.
- Confirm if you want to summarize another page.

## Need something better?
Checkout [Nanoread](https://nanoread.vercel.app) - A clean and fast web app that summarizes any webpage using AI. Paste a URL and get the summary in seconds.