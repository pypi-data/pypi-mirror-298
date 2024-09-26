import random
from colorama import Fore, Back, Style
print(f"{Fore.BLACK}{Back.WHITE}{Style.BRIGHT}ROCK, PAPER, SCISSORS")
name = input('What is your name? ')

print('Winning rules of the game ROCK PAPER SCISSORS are :\n'
      + "Rock vs Paper -> Paper wins \n"
      + "Rock vs Scissors -> Rock wins \n"
      + "Paper vs Scissors -> Scissor wins \n")
while True:

    print("So", name, "enter your choice \n 1 - Rock \n 2 - Paper \n 3 - Scissors \n")
    # user input
    choice = int(input("Enter your choice :"))
    while choice > 3 or choice < 1:
        choice = int(input('Enter a valid choice please ☺'))
        # initialize value of choice_name variable
    # corresponding to the choice value
    if choice == 1:
        choice_name = 'Rock'
    elif choice == 2:
        choice_name = 'Paper'
    else:
        choice_name = 'Scissors'
        # print user choice
    print('User choice is \n', choice_name)
    print('Now its Computers Turn....')
    # Computer chooses random number
    comp_choice = random.randint(1, 3)
    while comp_choice == choice:
        comp_choice = random.randint(1, 3)
    if comp_choice == 1:
        comp_choice_name = 'RocK'
    elif comp_choice == 2:
        comp_choice_name = 'Paper'
    else:
        comp_choice_name = 'Scissors'
    print("Computer choice is \n", comp_choice_name)
    print(choice_name, 'Vs', comp_choice_name)
    if choice == comp_choice:
        print('Its a Draw', end="")
        result = "DRAW"
    # wins
    if (choice == 1 and comp_choice == 2):
        print('paper wins =>', end="")
        result = 'Paper'
    elif (choice == 2 and comp_choice == 1):
        print('paper wins =>', end="")
        result = 'Paper'
    if (choice == 1 and comp_choice == 3):
        print('Rock wins =>\n', end="")
        result = 'Rock'
    elif (choice == 3 and comp_choice == 1):
        print('Rock wins =>\n', end="")
        result = 'RocK'
    if (choice == 2 and comp_choice == 3):
        print('Scissors wins =>', end="")
        result = 'Scissors'
    elif (choice == 3 and comp_choice == 2):
        print('Scissors wins =>', end="")
        result = 'Rock'
     # draws
    if result == 'DRAW':
        print("<== Its a tie ==>")
    if result == choice_name:
        print("<== YOU WIN ==>")
    else:
        #lose
        print("<== YOU LOSE ==>")
    print("Do you want to play again? (Y/N)")
    # replay option
    ans = input().lower()
    if ans == 'n':
        #reward
        print(f"{Fore.WHITE}{Back.RED}{Style.BRIGHT}Thanks for playing")
        print(f"{Style.RESET_ALL}")
        break