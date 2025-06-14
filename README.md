<div id="top">

<!-- HEADER STYLE: CLASSIC -->
<div align="center">


# SEARCH_BE

<em>Transform Insights into Action with AI-Powered Clarity</em>

<!-- BADGES -->
<img src="https://img.shields.io/github/last-commit/leegitae00/Search_BE?style=flat&logo=git&logoColor=white&color=0080ff" alt="last-commit">
<img src="https://img.shields.io/github/languages/top/leegitae00/Search_BE?style=flat&color=0080ff" alt="repo-top-language">
<img src="https://img.shields.io/github/languages/count/leegitae00/Search_BE?style=flat&color=0080ff" alt="repo-language-count">

<em>Built with the tools and technologies:</em>

<img src="https://img.shields.io/badge/Flask-000000.svg?style=flat&logo=Flask&logoColor=white" alt="Flask">
<img src="https://img.shields.io/badge/Markdown-000000.svg?style=flat&logo=Markdown&logoColor=white" alt="Markdown">
<img src="https://img.shields.io/badge/tqdm-FFC107.svg?style=flat&logo=tqdm&logoColor=black" alt="tqdm">
<img src="https://img.shields.io/badge/Gunicorn-499848.svg?style=flat&logo=Gunicorn&logoColor=white" alt="Gunicorn">
<img src="https://img.shields.io/badge/NumPy-013243.svg?style=flat&logo=NumPy&logoColor=white" alt="NumPy">
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/pandas-150458.svg?style=flat&logo=pandas&logoColor=white" alt="pandas">
<img src="https://img.shields.io/badge/OpenAI-412991.svg?style=flat&logo=OpenAI&logoColor=white" alt="OpenAI">

</div>
<br>

---

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Usage](#usage)
    - [Testing](#testing)
- [Features](#features)
- [Project Structure](#project-structure)

---

## Overview

Search_BE is an open-source developer tool that combines news retrieval, sentiment analysis, and AI-powered summaries into a streamlined Flask web application. It enables developers to build real-time news insights and content analysis systems with ease. The core features include:

- 🧩 **🔍 News Crawler:** Fetches and cleans recent news articles from Naver's API for targeted monitoring.
- 🚀 **🤖 AI Summarization:** Uses GPT-3.5-turbo to generate concise summaries and classify sentiment.
- 🖥️ **Main Interface:** Provides a user-friendly Flask app to interact with news data and AI insights locally.
- 🔧 **Dependency Management:** Ensures a consistent environment for scalable deployment.
- 🌐 **API Integration:** Connects news retrieval, analysis, and client responses seamlessly.

---

## Features

|      | Component       | Details                                                                                     |
| :--- | :-------------- | :------------------------------------------------------------------------------------------ |
| ⚙️  | **Architecture**  | <ul><li>RESTful API built with Flask</li><li>Separation of concerns between API endpoints and utility modules</li><li>Uses environment variables for configuration</li></ul> |
| 🔩 | **Code Quality**  | <ul><li>Consistent code style adhering to PEP8</li><li>Modular structure with dedicated directories for routes, utils, and configs</li><li>Includes docstrings for functions and classes</li></ul> |
| 📄 | **Documentation** | <ul><li>Basic README with project overview</li><li>In-code comments for key functions</li><li>Uses markdown for formatting</li></ul> |
| 🔌 | **Integrations**  | <ul><li>OpenAI API for search or NLP functionalities</li><li>BeautifulSoup4 for web scraping</li><li>Requests for HTTP calls</li><li>Flask-Cors for cross-origin support</li></ul> |
| 🧩 | **Modularity**    | <ul><li>Separate modules for API routes, utilities, and configuration</li><li>Reusable functions for API interactions and data processing</li></ul> |
| 🧪 | **Testing**       | <ul><li>Minimal or no explicit test suite identified</li><li>Potential for unit tests in `tests/` directory (not confirmed)</li></ul> |
| ⚡️  | **Performance**   | <ul><li>Uses `gunicorn` for production WSGI server</li><li>Potential bottlenecks in web scraping or API calls not optimized</li></ul> |
| 🛡️ | **Security**      | <ul><li>Uses `python-dotenv` for environment variables, possibly for API keys</li><li>Limited security measures observed; no explicit input validation or sanitization</li></ul> |
| 📦 | **Dependencies**  | <ul><li>Relies on `requirements.txt` for dependency management</li><li>Key dependencies include Flask, openai, beautifulsoup4, requests, pandas, numpy, tqdm, Flask-Cors, python-dotenv</li></ul> |

---

## Project Structure

```sh
└── Search_BE/
    ├── README.md
    ├── app.py
    ├── crawler.py
    ├── gpt_sentiment_summary.py
    └── requirements.txt
```

---

## Getting Started

### Prerequisites

This project requires the following dependencies:

- **Programming Language:** Python
- **Package Manager:** Pip

### Installation

Build Search_BE from the source and install dependencies:

1. **Clone the repository:**

    ```sh
    ❯ git clone https://github.com/leegitae00/Search_BE
    ```

2. **Navigate to the project directory:**

    ```sh
    ❯ cd Search_BE
    ```

3. **Install the dependencies:**

**Using [pip](https://pypi.org/project/pip/):**

```sh
❯ pip install -r requirements.txt
```

### Usage

Run the project with:

**Using [pip](https://pypi.org/project/pip/):**

```sh
python {entrypoint}
```

### Testing

Search_be uses the {__test_framework__} test framework. Run the test suite with:

**Using [pip](https://pypi.org/project/pip/):**

```sh
pytest
```

---

<div align="left"><a href="#top">⬆ Return</a></div>

---
