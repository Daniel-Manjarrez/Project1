import os

KEY = os.environ.get('OPENAI_KEY')

print(KEY)


def Program():

    print("Welcome to Python Pokedex!")

    while True:
        choice = input("What can I help you with today?: ")


Program()
