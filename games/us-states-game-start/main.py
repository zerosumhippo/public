import turtle
from state_manager import StateManager

PROMPT = "Enter a State Name"

screen = turtle.Screen()
screen.title("U.S. States Game")
image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)
state_manager = StateManager()
answer_list = []
state_list = state_manager.states_to_list()


while len(answer_list) < 50:
    correct_answer_count = len(answer_list)
    answer_state = screen.textinput(title=f"{correct_answer_count}/50 States Correct", prompt=PROMPT).title()
    if answer_state in state_list:
        state_manager.guess_to_map(answer_state)
        answer_list.append(answer_state)
    if answer_state == "Exit" or len(answer_list) >= 50:
        state_manager.write_learning_file(user_answers=answer_list)
        break
