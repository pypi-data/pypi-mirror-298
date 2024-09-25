line1 = "         * "
line2 = "        /|\\"
line3 = "       /*|O\\"
line4 = "      /*/|*\\"
line5 = "     /X/O|*\\X\\"
line6 = "    /*/X/|\\X\\*\\"
line7 = "   /O/*/X|*\\O\\X\\"
line8 = "  /*/O/X/|\\X\\O\\*\\"
line9 = " /X/O/*/X|O\\X\\*\\O\\"
line10 = "/O/X/*/O/|\\X\\*\\O\\X\\"
line11 = "        |X|      "
line12 = "        |X|      "

def tree():
    lines = [line1, line2, line3, line4, line5, line6, line7, line8, line9, line10, line11, line12]
    for line in lines:
        print(line)

# Roep de functie aan om de boom weer te geven
tree()
