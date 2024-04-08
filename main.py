from game import Game

def main():
    print("\n=================================\n")

    while True:
        user_input = ""

        while user_input not in ['X', 'O']:
            user_input = input("Enter 'X' or 'O' ('q' to quit): ")

            if user_input == 'q':
                return

        print("\n=================================\n")

        winner = Game(user_input).play()

        if winner:
            print(f"{winner} wins!\n")
        else:
            print("Draw.\n")

if __name__ == "__main__":
    main()