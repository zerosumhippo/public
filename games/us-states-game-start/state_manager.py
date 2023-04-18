from turtle import Turtle
import pandas

ALIGNMENT = "left"
FONT = ('Arial', 8, 'normal')


class StateManager(Turtle):

    def __init__(self):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.states_data = pandas.read_csv("50_states.csv")
        self.states_data_dict = self.states_data.to_dict()
        # self.learn_list = []
        # self.learn_dict = {}

    def states_to_list(self):
        state_list = self.states_data.state.to_list()
        return state_list

    def guess_to_map(self, answer_state):
        for state_key in self.states_data_dict["state"]:
            if answer_state == self.states_data_dict["state"][state_key]:
                state_location = (self.states_data_dict["x"][state_key], self.states_data_dict["y"][state_key])
                self.goto(state_location)
                self.write(answer_state, align=ALIGNMENT, font=FONT)

    def write_learning_file(self, user_answers):
        all_correct_answers = self.states_to_list()
        learn_list = [state for state in all_correct_answers if state not in user_answers]
        pandas.DataFrame(learn_list).to_csv("states_to_learn.csv")
        # for state in all_correct_answers:
        #     if state not in user_answers:
        #         self.learn_list.append(state)
        #         self.learn_dict = {
        #             "States to Learn": self.learn_list
        #         }
        # pandas.DataFrame(self.learn_dict).to_csv("states_to_learn.csv")
