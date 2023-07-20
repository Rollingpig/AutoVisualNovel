from llm.initKeys import init_keys
from story.base import Story


def read_story_from_file() -> str:
    # get all txt files in 'data' folder
    import os
    data_files = os.listdir('data')
    data_files = [file for file in data_files if file.endswith('.txt')]

    choice = input(f"Which story seed do you want (1 to {len(data_files)})? type 'r' to random: ")
    # if choice is neither 'q' nor an integer, prompt for choice again
    while choice != 'q' and choice != 'r' and not choice.isdigit():
        choice = input(f"Your input should be an integer from 1 to {len(data_files)}, or 'r', please try again: ")

    if choice == 'r':
        # randomly choose a file
        import random
        story_file = random.choice(data_files)
    else:
        story_file = f'story{choice}.txt'

    # read story from file
    with open(f'data/{story_file}', 'r') as f:
        story_txt = f.read()

    return story_txt


def main():
    init_keys()

    # read story from file
    print("Reading story from file...")
    story_txt = read_story_from_file()

    # initialize story
    print("Initializing story...It takes about 1-2 minutes.")
    story = Story(story_txt)
    story.init_understand()

    choice = input("Now the story begin. Press Enter to continue.\n"
                   "Or type the index of the choice you want to make, type 'q' to quit: ")
    if choice == 'q':
        return

    print("-" * 20)

    story.play()
    response = True
    while response:
        choice = input("")
        response = story.receive_input(choice)


if __name__ == '__main__':
    main()
