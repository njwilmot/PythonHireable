import json
import heapq
import random

# Define a dictionary of questions, where the keys are the question ids and the values are the questions
with open('questions.json', 'r') as f:
    questions = json.load(f)
random.shuffle(questions)
questions_dict = {q['id']: q for q in questions}

# Create a priority queue for each difficulty level, where the priority is based on the weight of each question
question_queues = {
    1: [],
    2: [],
    3: []
}
for q in questions:
    question_queues[q['difficulty']].append((q['weight'], q['id']))

# Define the initial difficulty level and score
difficulty = 1
total_score = 0
possible_score = 0
num_asked_total = 0
num_asked_difficulty = 0
num_questions_difficulty = {1: len(question_queues[1]),
                            2: len(question_queues[2]),
                            3: len(question_queues[3])}
asked_questions = {1: {}, 2: {}, 3: {}}

# Loop through the questions
while num_asked_total < len(questions_dict):
    # Select the next question from the highest-priority queue that has unasked questions
    while True:
        if not question_queues[difficulty]:
            # If all questions at the current difficulty level have been asked, move to the next difficulty level
            num_questions_difficulty[difficulty] = 0
            difficulty += 1
            if difficulty > 3:
                break
        else:
            current_question_weight, current_question_id = heapq.heappop(question_queues[difficulty])
            if not asked_questions[difficulty].get(current_question_id):
                current_question = questions_dict[current_question_id]
                break

    # If all questions have been asked, break out of the loop
    if difficulty > 3:
        break

    # Shuffle the list of options
    options = current_question['options']
    random.shuffle(options)

    # Ask and get the user's answer
    print(f"\ndifficulty: {current_question['difficulty']}")
    print(f"\nQuestion {num_asked_total + 1}: {current_question['question']}")
    for j, option in enumerate(options):
        print(f"{j + 1}. {option}")
    question_len = len(options)
    while True:
        answer = input(f"Enter your answer 1-{question_len}: ")
        try:
            answer = int(answer)
            if answer < 1 or answer > question_len:
                print(f"Invalid answer, please enter a number between 1 and {question_len}")
            else:
                break
        except ValueError:
            print(f"Invalid answer, please enter a number between 1 and {question_len}")

    if answer == current_question["options"].index(current_question["answer"]) + 1:
        total_score += current_question["point_value"] * current_question["weight"]
        possible_score += current_question["point_value"] * current_question["weight"]
        num_asked_difficulty += 1
        num_asked_total += 1
        num_questions_difficulty[difficulty] -= 1
        asked_questions[difficulty][current_question_id] = True
        if difficulty < 3:
            difficulty += 1
    else:
        possible_score += current_question["point_value"] * current_question["weight"]
        num_asked_difficulty += 1
        num_asked_total += 1
        num_questions_difficulty[difficulty] -= 1
        asked_questions[difficulty][current_question_id] = True
        if difficulty > 1:
            difficulty -= 1

        # Add the question back to the priority queue with a higher weight
        current_question['weight'] += 1
        heapq.heappush(question_queues[difficulty], (current_question['weight'], current_question_id))

# Print the results
print(f"\nTotal score: {total_score} out of {possible_score}")
print("Thanks for playing!")
