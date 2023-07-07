import openai

from story.base import Story


def init_openai_key():
    # read openAI key from txt file, if file is not found, prompt for key
    try:
        with open('openai_key.txt', 'r') as f:
            openai_key = f.read()
    except FileNotFoundError:
        openai_key = input("Please enter your openAI key: ")
        with open('openai_key.txt', 'w') as f:
            f.write(openai_key)

    # set openAI key
    openai.api_key = openai_key


def read_story_from_file() -> str:
    # get all txt files in 'data' folder
    import os
    data_files = os.listdir('data')
    data_files = [file for file in data_files if file.endswith('.txt')]

    choice = input(f"Which story seed do you want (1 to {len(data_files)})? type 'r' to random: ")
    # if choice is neither 'q' nor an integer, prompt for choice again
    while choice != 'q' and not choice.isdigit():
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
    init_openai_key()

    # read story from file
    print("Reading story from file...")
    story_txt = read_story_from_file()

    # initialize story
    print("Initializing story...")
    story = Story(story_txt)
    story.init_understand()
    story.play()

    # get choice from user
    choice = input("Please type the index of the choice you want to make, type 'q' to quit: ")
    while choice != 'q':
        story.generate_scene_from_choice(int(choice))
        story.play()
        choice = input("Please type the index of the choice you want to make, type 'q' to quit: ")

        # if choice is neither 'q' nor an integer, prompt for choice again
        while choice != 'q' and not choice.isdigit():
            choice = input("Your input should be an integer from 1 to 3, or 'q', please try again: ")


if __name__ == '__main__':
    main()
