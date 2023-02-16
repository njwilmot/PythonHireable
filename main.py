import json
import random

# Define a list of questions, where each question is a dictionary with the question, the possible answers,
# and the correct answer
with open('questions.json','r') as f:
    questions = json.load(f)

# Define the initial difficulty level and score
difficulty = 1
score = 0

num_asked_total = 0
num_asked_difficulty = 0
asked_questions = []

# Loop through the questions
while num_asked_total < 5:
    # Select a question with the current difficulty level
    possible_questions = [q for q in questions if q["difficulty"] == difficulty and q not in asked_questions]
    if not possible_questions:
        print(f"No more questions at difficulty {difficulty}. Ending test.")
        break
    current_question = random.choice(possible_questions)

    # Ask and get the user's answer
    print(f"Question {num_asked_total + 1}: {current_question['question']}")
    for j, option in enumerate(current_question["options"]):
        print(f"{j + 1}. {option}")

    question_len = len(current_question['options'])
    answer = int(input(f"Enter your answer 1-{question_len}: "))

    # Check the answer and update the score and difficulty level
    if answer == current_question["options"].index(current_question["answer"]) + 1:
        print("Correct!")
        score += 1
        num_asked_difficulty += 1
        num_asked_total += 1
        difficulty = min(difficulty + 1, 4)
    else:
        print("Incorrect!")
        num_asked_difficulty += 1
        num_asked_total += 1
        difficulty = max(difficulty - 1, 1)

    asked_questions.append(current_question)

# Print the final score
print(f"Final score: {score}/{num_asked_total}")
