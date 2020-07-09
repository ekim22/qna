# import sys
# open file
# read lines
# if line doesnt start with whitespace its title
# add to title dict
# until next title or EOF
    # create new dict
    # if line starts with '-' add line as key
    # elif line starts with '+' or number add line as value


import sys
import json
import pprint as pp

def check_for_len(line):
    return len(line.strip())


def check_for_dash(line):
    return line.strip()[0] == '-'


def check_for_star(line):
    return line.strip()[0] == '*'


def check_for_header(line):
    return line.strip()[0].isalpha()


lines = []

with open(sys.argv[1]) as f:
    for line in f:
        if check_for_len(line) and check_for_header(line):
            print("H: " + line)
        elif check_for_len(line) and check_for_dash(line):
            print("Q: " + line)
        elif check_for_len(line) and check_for_star(line):
            print("A: " + line)
            answers = []
            answers.append(line.strip())
            line = next(f)
            if check_for_len(line) and check_for_dash(line):
                print("Q: " + line)
            while len(line.strip()) != 0 and line.strip()[0] != '-' and '*':
                answers.append(line.strip())
                print(line)
                line = next(f)
                if check_for_len(line) and check_for_dash(line):
                    print("Q: " + line)
            answers = " ".join(answers)
            lines.append(answers)
        


pp.PrettyPrinter(indent=4)
#pp.pprint(lines)
#print(len(lines))
#for line in lines:
#    print("LN: " + line)
#        
