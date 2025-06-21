import os
import requests
import random
from dotenv import load_dotenv


load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

API_URL = "https://api.together.xyz/v1/chat/completions"
MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"  # You can use llama3 too


def ask_together(prompt):
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 50,
        "stop": ["\n"]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            return f"API Error {response.status_code}:\n{response.text}"
    except Exception as e:
        return f"Request failed: {e}"


# Prompt templates
PROMPT_TEMPLATES = {
    "1": [
        "Answer in one word only: {q}",
        "Give a one-line factual answer only, no explanation: {q}",
        "Reply with only the fact, nothing more: {q}"
    ],
    "2": [
        "Please summarize this text: {text}",
        "Summarize the main points in this passage: {text}",
        "TL;DR of the following: {text}"
    ],
    "3": [
        "Write a short story about: {topic}",
        "Create a poem or story based on: {topic}",
        "Imagine and write a creative piece on: {topic}"
    ],
    "4": [
        "Give me some practical tips on: {advice}",
        "What advice can you provide about: {advice}",
        "List helpful suggestions related to: {advice}"
    ]
}


def main():
    print("\n🤖 Welcome to SmartPrompt AI Assistant\n")
    print("Functions:")
    print("1. Answer factual question")
    print("2. Summarize a text")
    print("3. Generate creative content")
    print("4. Get advice")

    choice = input("Choose a function (1–4): ")

    if choice == "1":
        q = input("Enter your question: ")
        prompt = random.choice(PROMPT_TEMPLATES["1"]).format(q=q)

    elif choice == "2":
        text = input("Paste the text to summarize:\n")
        prompt = random.choice(PROMPT_TEMPLATES["2"]).format(text=text)

    elif choice == "3":
        topic = input("Topic for the creative content: ")
        prompt = random.choice(PROMPT_TEMPLATES["3"]).format(topic=topic)

    elif choice == "4":
        advice = input("What topic do you need advice on? ")
        prompt = random.choice(PROMPT_TEMPLATES["4"]).format(advice=advice)

    else:
        print("Invalid choice. Please try again.")
        return

    print("\n⏳ Generating response...\n")
    result = ask_together(prompt)
    print("💬 Response:\n")
    print(result)

    feedback = input("\nWas this helpful? (yes/no): ")
    with open("feedback_together.txt", "a") as f:
        f.write(f"\n[Function: {choice}]\nPrompt: {prompt}\nFeedback: {feedback}\n{'-' * 40}\n")


if __name__ == "__main__":
    main()
