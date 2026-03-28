#🚀 Jak uruchomić projekt
Możesz uruchomić skaner na dwa sposoby:

1. Tryb analizy pliku (Zalecany)
Jeśli masz już plik z kodem (np. test.py), przekaż jego nazwę jako argument wiersza poleceń:

Bash
python main.py test.py
Program natychmiast wczyta plik, wyświetli listę tokenów w konsoli i wygeneruje obok plik pokolorowany_kod.html.

2. Tryb interaktywny (Konsola)
Jeśli uruchomisz skrypt bez żadnych argumentów:

Bash
python main.py
Program poprosi Cię o wpisanie lub wklejenie kodu bezpośrednio do konsoli. Ponieważ kod może mieć wiele linijek, po zakończeniu wpisywania należy wysłać sygnał końca pliku (EOF):

Na systemie Windows: Wciśnij Ctrl + Z, a następnie Enter.

Na systemie Linux / macOS: Wciśnij Ctrl + D.

#⚙️ Generowanie HTML (Syntax Highlighting)
Po każdym pomyślnym przeskanowaniu kodu, program automatycznie wygeneruje plik pokolorowany_kod.html w katalogu głównym. Otwórz ten plik w dowolnej przeglądarce internetowej, aby zobaczyć kod z nałożonym profesjonalnym motywem kolorystycznym.

# Język implementacji

Python

📚 Zbiór tokenów i architekturaSkaner opiera się na ręcznie zdefiniowanych automatach. Do obsługi stałych fragmentów (np. operatory, słowa kluczowe) używana jest dynamiczna funkcja _create_exact.Typ TokenuAutomatRegex (Odpowiednik)Opis wzorcaFLOATNUMBERfloat_automat(?:\d+(?:_\d+)*)?\.\d+(?:_\d+)*(?:[eE][+-]?\d+(?:_\d+)*)?|\d+(?:_\d+)*[eE][+-]?\d+(?:_\d+)*Liczba zmiennoprzecinkowa (z notacją naukową)NUMBERfloat_automat\d+(?:_\d+)*Zwykła liczba całkowita (dziesiętna)BINNUMBERbin_automat0[bB](?:_?[01])+Liczba binarnaOCTNUMBERoct_automat0[oO](?:_?[0-7])+Liczba ósemkowaHEXNUMBERhex_automat0[xX](?:_?[0-9a-fA-F])+Liczba szesnastkowaIDid_automat[a-zA-Z_][a-zA-Z0-9_]*Litery i cyfry, zaczynające się od litery lub _SPECIAL_create_exact\b(?:if|else|for|while|def|class|return|True|False|None)\bSłowa kluczowe języka PythonFSTRINGfstring_automat(Wymaga stosu)F-stringi z obsługą zagnieżdżeń (PDA)STRINGstring_automat""".*?"""|'''.*?'''|".*?"|'.*?'Ciągi znaków (napisy)PLUS_create_exact\+Znak plusaMINUS_create_exact-Znak minusaMUL_create_exact\*MnożenieDIV_create_exact/DzielenieDOUBLESLASH_create_exact//Dzielenie całkowiteDOUBLESTAR_create_exact\*\*PotęgowaniePERCENT_create_exact%Modulo, reszta z dzieleniaLPAREN_create_exact\(Nawias otwierający okrągłyRPAREN_create_exact\)Nawias zamykający okrągłyLSQB_create_exact\[Nawias otwierający kwadratowyRSQB_create_exact\]Nawias zamykający kwadratowyLBRACE_create_exact\{Klamra otwierającaRBRACE_create_exact\}Klamra zamykającaEQUAL_create_exact=PrzypisaniePLUSEQUAL_create_exact\+=Przypisanie z dodaniemMINUSEQUAL_create_exact-=Przypisanie z odejmowaniemMULEQUAL_create_exact\*=Przypisanie z mnożeniemDIVEQUAL_create_exact/=Przypisanie z dzieleniemDOUBLESLASHEQUAL_create_exact//=Przypisanie z dzieleniem całkowitymCOMPARISON_create_exact==Porównanie wartościNOTEQUAL_create_exact!=NierówneLESS_create_exact<MniejszeLESSEQUAL_create_exact<=Mniejsze lub równeGREATER_create_exact>WiększeGREATEREQUAL_create_exact>=Większe lub równeCOLON_create_exact:DwukropekCOMMA_create_exact,PrzecinekDOT_create_exact\.KropkaBITAND_create_exact&Bitowe ANDBITOR_create_exact|Bitowe ORNEWLINEnewline_automat\n|\r\nEnter (Logiczny koniec linii)INDENTindent_automat\tTabulatorSPACEspace_automat[ \f\v]+SpacjaCOMMENTcomment_automat#.*Komentarz jednowierszowyERROR(Fallback).Błąd leksykalny (Nierozpoznany znak)
