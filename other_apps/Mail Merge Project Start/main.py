#TODO: Create a letter using starting_letter.txt 
#for each name in invited_names.txt
#Replace the [name] placeholder with the actual name.
#Save the letters in the folder "ReadyToSend".
    
#Hint1: This method will help you: https://www.w3schools.com/python/ref_file_readlines.asp
    #Hint2: This method will also help you: https://www.w3schools.com/python/ref_string_replace.asp
        #Hint3: THis method will help you: https://www.w3schools.com/python/ref_string_strip.asp
        #Hint4: Saving a file to a new file path: https://stackoverflow.com/questions/8024248/telling-python-to-save-a-txt-file-to-a-certain-directory-on-windows-and-mac
# C:\Users\breim\Documents\Mail Merge Project Start


with open("../Mail Merge Project Start/Input/Names/invited_names.txt") as file:
    name_list = file.readlines()
    for name in name_list:
        name_list[name_list.index(name)] = name.replace("\n", "")
    #     Could also do this instead: name_list[name_list.index(name)] = name.strip()
    print(name_list)

with open("../Mail Merge Project Start/Input/Letters/starting_letter.txt") as file:
    contents = file.read()
    for x in range(len(name_list)):
        individual_name = name_list[x]
        personalized_contents = contents.replace("[name]", name_list[x])
        file_name_path = f"./Output/ReadyToSend/letter_for_{individual_name}.txt"
        personalized_file = open(file_name_path, "w")
        personalized_file.write(personalized_contents)
        personalized_file.close()
