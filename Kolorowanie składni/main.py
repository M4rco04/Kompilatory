from utility.skaner import Skaner
from utility.html_generator import HtmlGenerator
import sys


def main():
    expression = ""

    if len(sys.argv) > 1:
        filename = sys.argv[1]
        try:
            with open(filename, "r", encoding="utf-8") as file:
                expression = file.read()
            print(f"--- Wczytano plik: {filename} ---")
        except FileNotFoundError:
            print(f"Błąd: Nie znaleziono pliku '{filename}'.")
            return
        except Exception as e:
            print(f"Błąd podczas odczytu pliku: {e}")
            return
    else:
        print("Wprowadź kod do przeskanowania.")
        print(
            "(Aby zakończyć wprowadzanie, wciśnij Ctrl+Z i Enter na Windowsie lub Ctrl+D na Mac/Linux):\n"
        )
        try:
            expression = sys.stdin.read()
            print("\n--- Rozpoczynam skanowanie ---")
        except KeyboardInterrupt:
            print("\nPrzerwano przez użytkownika.")
            return
    if not expression.strip():
        print("Nie podano żadnego tekstu do analizy.")
        return

    skaner = Skaner(expression)

    try:
        skaner.loop()
        generator = HtmlGenerator(skaner.tokens)
        generator.generate("pokolorowany_kod.html")
    except Exception as e:
        print(f"Błąd podczas skanowania: {e}")


if __name__ == "__main__":
    main()
