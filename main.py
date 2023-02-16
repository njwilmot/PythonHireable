import random
import json

# Load questions from a JSON file
with open('questions.json', 'r') as f:
    questions = json.load(f)

# Define the initial difficulty level and score
difficulty = 1
score = 0

# Keep track of which questions have been asked
asked_questions = set()

# Loop through the questions
for i in range(len(questions)):


    # Select a question with the current difficulty level that hasn't been asked before
    possible_questions = [q for q in questions if q["difficulty"] == difficulty and q["question"] not in asked_questions]
    if len(possible_questions) == 0:
        # If there are no more questions at this difficulty level, move to the next level
        difficulty += 1
        possible_questions = [q for q in questions if q["difficulty"] == difficulty and q["question"] not in asked_questions]
    if len(possible_questions) == 0:
        # If there are no more questions at any difficulty level, end the game
        break
    current_question = random.choice(possible_questions)

    # Ask and get the user's answer
    print(f"Question {i + 1}: {current_question['question']}")
    for j, option in enumerate(current_question["options"]):
        print(f"{j + 1}. {option}")

    question_len = len(current_question['options'])
    answer = int(input(f"Enter your answer 1-{question_len}: "))

    # Check the answer and update the score and difficulty level
    if answer == current_question["options"].index(current_question["answer"]) + 1:
        print("Correct!")
        score += current_question.get("points", 1)
        difficulty += 1
    else:
        print("Incorrect!")
        difficulty -= 1

    # Make sure the difficulty level stays within the appropriate range
    if difficulty < 1:
        difficulty = 1
    elif difficulty > 4:
        difficulty = 4

    # Add the question to the set of asked questions
    asked_questions.add(current_question['question'])

# Print the final score
print(f"Final score: {score}/{len(questions)}")
