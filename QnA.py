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

pp.PrettyPrinter(indent=4)
lines = []
headers = {}

with open(sys.argv[1]) as f:
    for line in f:
        if check_for_len(line) and check_for_header(line):
            print("H: " + line)
            header = line.strip()
            headers[header] = []
            while check_for_len(line):
                line = next(f)
                if check_for_len(line) and check_for_dash(line):
                    print("Q: " + line)
                    Q = line.strip()
                    headers[header].append({Q: ""})
                elif check_for_len(line) and check_for_star(line):
                    answers = []
                    while check_for_len(line) and not check_for_dash(line):
                        answers.append(line.strip())
                        print("A: " + line)
                        line = next(f)
                    answers = " ".join(answers)
                    headers[header][0][Q] = answers
                    if check_for_len(line) and check_for_dash(line):
                        print("Q2: " + line)
                        Q = line.strip()
                        #headers[header].append({Q: ""})
                

       # elif check_for_len(line) and check_for_dash(line):
       #     print("Q: " + line)
       # elif check_for_len(line) and check_for_star(line):
       #     answers = []
       #     while len(line.strip()) != 0 and not check_for_dash(line):
       #         answers.append(line.strip())
       #         print("A: " + line)
       #         line = next(f)
       #     if check_for_len(line) and check_for_dash(line):
       #         print("Q2: " + line)
       #     answers = " ".join(answers)
       #     lines.append(answers)
       # 

for header in headers:
    print("\n" + header)
    for question, answer in headers[header][0].items():
        print(question)
        print("    " + answer)
#pp.pprint(lines)
#print(len(lines))
#for line in lines:
#    print("LN: " + line)
#        
