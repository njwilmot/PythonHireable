import json
import random
import time


class AVLTreeNode:
    def __init__(self, data, height=1):
        self.data = data
        self.height = height
        self.left = None
        self.right = None


class AVLTree:
    def __init__(self):

        with open('questions.json', 'r') as f:
            self.questions = json.load(f)

        self.start_time = time.time()  # start timer
        # create a dictionary to store questions by ID
        self.questions_by_id = {}
        for q in self.questions:
            self.questions_by_id[q['id']] = AVLTreeNode(q)

        # build the AVL tree
        self.root = self._build_balanced_question_tree()

        self.asked_questions = set()  # initialize an empty set of asked questions
        self.current_question = None  # initialize current question to None
        self.difficulty = 2  # initialize difficulty to 1
        self.score = 0  # initialize score to 0

    def _height(self, node):
        if node is None:
            return 0
        return node.height

    def _rotate_left(self, node):
        right_child = node.right
        node.right = right_child.left
        right_child.left = node

        node.height = 1 + max(self._height(node.left), self._height(node.right))
        right_child.height = 1 + max(self._height(right_child.left), self._height(right_child.right))

        return right_child

    def _rotate_right(self, node):
        left_child = node.left
        node.left = left_child.right
        left_child.right = node

        node.height = 1 + max(self._height(node.left), self._height(node.right))
        left_child.height = 1 + max(self._height(left_child.left), self._height(left_child.right))

        return left_child

    def _balance_factor(self, node):
        if node is None:
            return 0
        return self._height(node.left) - self._height(node.right)

    def _balance(self, node):
        if node is None:
            return node

        balance = self._balance_factor(node)

        if balance > 1:
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        elif balance < -1:
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        node.height = 1 + max(self._height(node.left), self._height(node.right))
        return node

    def _insert(self, node, data):
        if node is None:
            return AVLTreeNode(data)

        if data['id'] < node.data['id']:
            node.left = self._insert(node.left, data)
        else:
            node.right = self._insert(node.right, data)

        node = self._balance(node)
        return node

    def _build_balanced_question_tree(self):
        questions_by_difficulty = self._sort_questions_by_difficulty()
        root = None
        for difficulty in range(1, 4):
            questions = questions_by_difficulty[difficulty]
            random.shuffle(questions)
            for question in questions:
                root = self._insert(root, question)
        return root

    def _sort_questions_by_difficulty(self):
        questions_by_difficulty = [[], [], [], []]
        for q in self.questions:
            questions_by_difficulty[q['difficulty']].append(q)

        return questions_by_difficulty

    def _get_question(self, node):
        if node is None:
            return None

        if time.time() - self.start_time >= 60:  # check if 1 minute has passed
            return None

        # check if the question has already been asked
        if node.data['id'] in self.asked_questions:
            return self._get_question(node.right)

        # check if the difficulty is appropriate
        if node.data['difficulty'] == self.difficulty:
            self.current_question = node
            return node

        # check if there are no questions of the specific difficulty that haven't been asked yet
        questions = [q for q in self.questions_by_id.values() if q.data['difficulty'] == self.difficulty]
        unanswered_questions = set(q.data['id'] for q in questions) - self.asked_questions
        if not unanswered_questions:
            return None
        # select a random unanswered question of the appropriate difficulty
        question_id = random.choice(list(unanswered_questions))
        self.current_question = self.questions_by_id[question_id]
        return self.current_question

    def get_question(self):
        elapsed_time = int(time.time() - self.start_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        print(f"Time Elapsed: {minutes:02d}:{seconds:02d}")

        if time.time() - self.start_time >= 60:  # check if 1 minute has passed
            return None

        question = self._get_question(self.root)
        while question is not None:
            self.asked_questions.add(question.data['id'])
            return question.data

        # Check if all questions have been asked
        if len(self.asked_questions) == len(self.questions_by_id):
            return None

        # Check if there are no more unanswered questions in the current difficulty
        questions = [q for q in self.questions_by_id.values() if q.data['difficulty'] == self.difficulty]
        unanswered_questions = set(q.data['id'] for q in questions) - self.asked_questions
        if not unanswered_questions:
            # If all questions in the current difficulty have been asked, end quiz
            return None

        return None

    def answer_question(self, question_id, answer_index):
        if self.current_question is None or question_id != self.current_question.data['id']:
            return False

        # check if the answer is correct
        if answer_index == self.current_question.data['index_answer']:
            self.score += self.current_question.data['weight'] * self.current_question.data['points']
            self.difficulty = min(self.difficulty + 1, 3)  # increase difficulty level if answer is correct
            return True
        else:
            self.difficulty = max(self.difficulty - 1, 1)  # decrease difficulty level if answer is incorrect
            return False

    def get_score(self):
        return self.score

    def get_elapsed_time(self):
        return int(time.time() - self.start_time)

    def get_score_category(self):
        total_score = self.get_score()
        if total_score < 20:
            return "entry"
        elif total_score < 30:
            return "junior"
        elif total_score < 40:
            return "senior"
        else:
            return "executive"


def main():
    quiz = AVLTree()

    while True:
        question = quiz.get_question()
        if question is None:
            print("No more questions available!")
            break

        # Display the question
        print(f"Question: {question['question']}")

        # Display the choices
        for i, choice in enumerate(question['options']):
            print(f"{i + 1}. {choice}")

        # Display the difficulty level
        print(f"Difficulty level: {question['difficulty']}")

        # Get the user's answer
        answer = input(f"Your answer (1-{len(question['options'])}): ")

        # Check if the answer is valid
        if not answer.isdigit() or int(answer) < 1 or int(answer) > len(question['options']):
            print("Invalid answer. Please enter a number between 1 and", len(question['options']))
            continue

        # Answer the question
        if quiz.answer_question(question['id'], int(answer)):
            print("Correct!")
        else:
            print("Incorrect!")

    # Display the final score and score category
    print(f"Final score: {quiz.get_score()}")
    print(f"Score category: {quiz.get_score_category()}")


if __name__ == '__main__':
    main()
