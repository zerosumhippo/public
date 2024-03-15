import pandas as pd


class MorseConverter:
    """Converts text inputs to morse code. Punctuation not supported."""

    def __init__(self):
        self.morse_data = pd.read_csv("morse.csv", names=["Text", "Morse"])
        self.power_on = True

    def converter(self):
        print("Welcome to the text to Morse Code converter.\n"
              "Please provide the English language text string you would like to convert, without punctuation, using "
              "letters and numbers.\nType 'end' to quit.\n")
        while self.power_on:
            text_input = input("Text to Convert: ").upper()
            if text_input == "END":
                self.power_on = False
            else:
                morse_output = ""
                for letter in text_input:
                    for n in self.morse_data.index:
                        if self.morse_data.Text[n] == letter:
                            morse_output += f"{str(self.morse_data.Morse[n])} "
                print(morse_output)
                