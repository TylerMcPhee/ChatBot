import json  
from difflib import get_close_matches  # Function that finds similar matches in a list of strings

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)  # Load the JSON data into a Python dictionary
    return data

def save_knowledge_base(file_path: str, data: dict):
    # Save the updated knowledge base back to the JSON file.
    with open(file_path, 'w') as file: 
        json.dump(data, file, indent=2)  # Write the data as JSON

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=.6)  # Get the closest match
    return matches[0] if matches else None 

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:  # Loop through each question in the knowledge base
        if q["question"] == question:  
            return q["answer"]  # Return the answer to question

def chat_bot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    while True: 
        user_input: str = input('You: ') 

        if user_input.lower() == 'quit':  
            break  

        # Find the best matching question for the user's input
        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base['questions']])

        if best_match:  
            answer: str = get_answer_for_question(best_match, knowledge_base)  
            print(f'Bot: {answer}')  # Respond with the answer obtained from knowledge_base
        else:  
            print('Bot: I don\'t know the answer. Can you teach me?')  
            new_answer: str = input('Type the answer or "skip" to skip: ')  # Ask for a new answer to unknown question

            if new_answer.lower() != 'skip':  
                # Add the new question-answer pair to the knowledge base
                knowledge_base['questions'].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)  
                print('Bot: Thank you! I learned a new response') 

if __name__ == '__main__':
    chat_bot() 
