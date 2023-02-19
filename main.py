import json
import random
# Define a dictionary of questions, where the keys are the question ids and the values are the questions
with open('questions.json', 'r') as f:
    questions = json.load(f)
questions_dict = {}
for q in questions:
    q_id = q['id']
    questions_dict[q_id] = q
# Define the initial difficulty level and score
difficulty = 1
total_score = 0
possible_score = 0
num_asked_total = 0
num_asked_difficulty = 0
asked_questions = set()
# Loop through the questions
while num_asked_total < 4:
    # Select a question with the current difficulty level that hasn't been asked before
    possible_questions = [questions_dict[q_id] for q_id in questions_dict.keys() if questions_dict[q_id]['difficulty'] == difficulty and q_id not in asked_questions]
    if not possible_questions and difficulty == 1:
        print("No more questions at difficulty 1. Ending test.")
        break
    if not possible_questions:
        continue
    current_question = random.choice(possible_questions)
    # Ask and get the user's answer
    print(f"\nQuestion {num_asked_total + 1}: {current_question['question']}")
    print(f"\tdiff: {difficulty}")
    for j, option in enumerate(current_question["options"]):
        print(f"{j + 1}. {option}")
    question_len = len(current_question['options'])
    answer = int(input(f"Enter your answer 1-{question_len}: "))
    # Check the answer and update the score and difficulty level
    if answer == current_question["options"].index(current_question["answer"]) + 1:
        total_score += current_question["point_value"]*current_question["weight"]
        possible_score += current_question["point_value"]*current_question["weight"]
        num_asked_difficulty += 1
        num_asked_total += 1
        difficulty = min(difficulty + 1, 3)
    else:
        possible_score += current_question["point_value"]*current_question["weight"]
        num_asked_difficulty += 1
        num_asked_total += 1
        difficulty = max(difficulty - 1, 1)
    if difficulty < 1:
        difficulty = 1
    elif difficulty > 3:
        difficulty = 3
    asked_questions.add(current_question['id'])
# Calculate and print the final score
if possible_score > 0:
    score = total_score / possible_score * 100
else:
    score = 0
print(f"\nFinal score: {total_score:.2f}")
