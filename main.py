from utility.skaner import Skaner


def main():
    print("Wprowadź wyrażenie matematyczne")
    expression = input()

    skaner = Skaner(expression)
    skaner.loop()

    print(skaner)


if __name__ == "__main__":
    main()
