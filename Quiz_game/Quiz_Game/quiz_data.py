import requests
import html
import random

def fetch_quiz_data(amount=10, category=None, difficulty=None):
    """
    Fetches quiz questions dynamically from the Open Trivia DB API.
    Each question includes text, 4 options, and the correct answer.
    """
    url = f"https://opentdb.com/api.php?amount={amount}&type=multiple"

    if category:
        url += f"&category={category}"
    if difficulty:
        url += f"&difficulty={difficulty}"

    response = requests.get(url)
    data = response.json()

    questions = []
    for item in data["results"]:
        question = html.unescape(item["question"])
        correct = html.unescape(item["correct_answer"])
        options = [html.unescape(opt) for opt in item["incorrect_answers"]]
        options.append(correct)
        random.shuffle(options)
        questions.append({
            "question": question,
            "options": options,
            "answer": correct
        })

    return questions

# For testing this file alone
if __name__ == "__main__":
    q_data = fetch_quiz_data(amount=5, difficulty="easy")
    for q in q_data:
        print(q["question"], "→", q["answer"])

