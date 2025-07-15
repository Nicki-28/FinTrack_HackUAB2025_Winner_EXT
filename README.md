# FinTrack_Winner_EXT 💸
*A financial assistant powered by AI – HackUAB 2025 Winner Edition*

---

This is an extension of that project, with improvements and a more complete backend implementation. It was born from my desire to consolidate what I learned in recent courses on Docker and Generative AI, which inspired me to revisit and enhance the original code.

## 🌟 Overview

**FinTrack** was born from the need to help individuals, especially those with limited financial literacy, understand and manage their money in a safe and informed way.

This project combines AI, automation, and financial education in a chatbot-powered tool that provides smart recommendations, tracks expenses, and verifies the safety of online shopping websites.

---

## What It Does

- 📊 **Tracks expenses and income** via a simple backend system  
- 🤖 **Analyzes user financial behavior** using Perplexity AI  
- 🌍 **Gives country-aware saving tips** based on user origin  
- 🛡️ **Evaluates website trustworthiness** via Trustpilot (Selenium)  
- 🧾 **Visualizes available payment methods** by region 
- 🧠 **Delivers a chatbot experience** to assist users with financial questions  

---

##  How It Works

The system is modular and divided into:

### Design  
- UX/UI mockups created with **Figma**  
- Friendly financial assistant mascot: **Fin**

###  AI Chatbot  
- Uses Sonar **(Perplexity API)** to generate real-time financial advice  
- Incorporates user origin data (e.g., country) for contextual responses  
- Structured prompts simulate a smart, helpful assistant

### Website Reputation Checker  
- Built with **Selenium + Trustpilot** to assess if a website is secure or risky for online purchases

---

## 🧠 New Features

### Persistent Memory with Docker Volumes

This chatbot now includes memory by saving user interactions (both questions and responses) in a `context.json` file.

- Memory is stored in a Docker **volume**, which allows the data to persist even if the container is stopped or rebuilt.
- The backend loads the last few interactions from memory and includes them in the prompt context before generating a new response.

#### How it works:

- A `context.json` file is created inside the `/app/memory` directory.
- When a new query arrives:
  - The chatbot **loads recent history** from the file.
  - Adds the new user input.
  - Sends all relevant messages to the AI model.
  - Appends the new response to the memory file.

> This enables a basic form of context retention across sessions.

---

### 🖼️ Image Support

You can also attach images along with your query through the web interface.

- Images are converted to **Base64** in the frontend and sent to the backend.
- If an image is present, it is included in the AI request using the `image_url` format supported by the API.
- This allows the assistant to interpret images of receipts, bills, or spending breakdowns.

> Example: You can take a photo of your expense list, and the assistant will consider it when analyzing your finances.

---

### 🐳 Docker Setup

The entire app runs inside a Docker container for easy portability and environment isolation.

- A Dockerfile defines the environment.
- A volume is mounted at `/app/memory` to persist conversation history.
- You can build and run the app with:

```bash
docker build -t finance-bot .
docker run -p 5000:5000 -v $(pwd)/chatbot_memory:/app/memory finance-bot

```
---
### Disclaimer
All backend, AI logic, API integration, were implemented by me as part of my individual learning journey and portfolio.

Some visual elements (such as mascot sketches or UI mockups) were initially created by the design team during the event. Minor visuals may still appear here for illustrative purposes.

The frontend components used during the hackathon are not included in this version. However, minimal UI code is present to support and visualize the new improvements.

If any original team member wishes to contribute or co-maintain this project, feel free to reach out.

--- 
### Clone de repository
```bash
git clone https://github.com/Nicki-28/FinTrack_Winner_EXT.git
cd FinTrack_Winner_EXT

