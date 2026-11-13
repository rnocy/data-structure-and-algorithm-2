import random

VALID_COLOURS = ["blue","green","red"] #create a variable that holds all the acceptable keywords

def get_user_list():
    print("Enter your list of words here, separated by commas.")
    print("Allowed words are:", VALID_COLOURS)

    while True:
        text = input("Your list:")
        words = text.replace(",", " ").lower().split() #convert the words in to string in a list
        if len(words) == 0:
            print("Please input words as above, the list is empty. Minimum input: 1 word")
            continue
        invalid = [w for w in words if w not in VALID_COLOURS]
        if invalid:
            print("Invalid! Please use only valid colours:", ", ".join(invalid))
            continue
        return words
        

def requirement(instructions: list[str]) -> list[int]: #define main requirements and convert list of str to int
    def get_index(i): #get the index based on the colour at position of current i
        if i >= len(instructions):
            return [] #return null for any index that is out of bounds

        colour = instructions[i] #get the colour at the current index

        if colour == "blue": #if i is at "blue", get the next "blue"
            next_blue = None # if no next "blue" is found, return the current index only
            for j in range(i + 1, len(instructions)): #set j as the next index after i and loop through the rest of the list
                if instructions[j] == "blue":
                    next_blue = j #set next_blue as "j"
                    break #break loop since we found the next "blue"

            if next_blue is None: #if there is no next blue, just go to the next index
                return [i]

            next_index = next_blue + 1 #if there is a next blue, set the next index to the index after it
        elif colour == "red": #if i is at "red", get the next index based on the formula 2 * i + 1
            next_index = 2 * i + 1
        else:  # green
            next_index = i + 1

        return [i] + get_index(next_index) #continue to the next one

    return get_index(0) #set the starting element

def main(): #define the main function for the algorithm
    print("Let's solve some example") #print this for user interface
    instructions =  get_user_list() #get user list as instruction input
    print("Your list:", instructions)
    print("Visited indices:", requirement(instructions))

if __name__ == "__main__": #run main
    main()
