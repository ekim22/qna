#!/usr/bin/env python

import sys, shutil
import re
import pprint as pp
from os import system, name
from termcolor import colored

class roman_numeral:
    def int_to_Roman(self, num):
        val = [
            1000, 900, 500, 400,
            100, 90, 50, 40,
            10, 9, 5, 4,
            1
        ]
        sym = [
            "M", "CM", "D", "CD",
            "C", "XC", "L", "XL",
            "X", "IX", "V", "IV",
            "I"
        ]
        roman_num = ''
        i = 0
        while num > 0:
            for _ in range(num // val[i]):
                roman_num += sym[i]
                num -= val[i]
            i += 1
        return roman_num


def check_for_len(line):
    return len(line.strip())


def check_for_dash(line):
    return line.strip()[0] == "-"


def check_for_star(line):
    return line.strip()[0] == "*"


def check_for_topic(line):
    return line.strip()[0] == '#'


def check_for_numeric(line):
    return line.strip()[0].isnumeric()


def check_header_lvl(line):
    p_header_lvl = re.compile("^([#]+)")
    m_header_lvl = p_header_lvl.search(line)
    if len(m_header_lvl.group(1)) == 1:
        return 1
    else:
        return 2


def add_section(section):
    global topics, line
    topics[section] = {}


def add_subsection(subsection):
    global topics, line, section
    topics[section][subsection] = []
    topics[section][subsection].append({})


def clear_screen():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux
    else:
        _ = system('clear')


def print_topic(section):
    term_columns = shutil.get_terminal_size()[0]
    print("=" * term_columns)
    # print("|" + (term_columns - 2) * " " + "|")
    print("|" + (term_columns - len(section))//2 * " " +
          colored(section.upper(), attrs=['bold']) +
          (term_columns - 3 - len(section))//2 * " " + "|")
    # print("|" + (term_columns - 2) * " " + "|")
    print("=" * term_columns)


def print_subsection(subsection):
    term_columns = shutil.get_terminal_size()[0]
    print()
    print((term_columns - len(subsection))//2 * " " + colored(subsection,
                                                             attrs=['bold',
                                                                    'underline'])
         + "\n")


def list_all():
    my_printer = pp.PrettyPrinter(depth=2, width=200)
    print("\n")
    for section in topics:
        print(section)
        for subsection in topics[section]:
            print("   " + subsection)
            my_printer.pprint(topics[section][subsection])
            print("\n")


def list_questions():
    for section in topics:
        for question, answer in topics[section][0].items():
            print("Q: " + question)


def list_answers():
    for section in topics:
        for question, answer in topics[section][0].items():
            print("A:" + answer)


def list_questions_and_answers():
    my_printer = pp.PrettyPrinter(width=200)
    for section in topics:
        for subsection in topics[section]:
            for question, answer in topics[section][subsection][0].items():
                print(colored("Q: ", 'yellow') + colored(question[2:], attrs=['bold']))
                print(colored("A: ", 'red') + answer[2:])


def list_qna_for_each_section():
    my_printer = pp.PrettyPrinter(width=200)
    for section in topics:
        print_topic(section)
        numeral = 1
        for subsection in topics[section]:
            rn = roman_numeral()
            print_subsection(rn.int_to_Roman(numeral) + ". " + subsection)
            numeral+=1
            for q, a in topics[section][subsection][0].items():
                print(colored("Q: ", 'yellow') + q[2:])
                print(colored("A: ", 'red') + a[2:])
        print("\n")


def list_sections():
    for section in topics:
        print_topic(section)


def list_subsections():
    for section in topics:
        print_topic(section)
        for index, subsection in enumerate(topics[section]):
            print(str(index + 1) + ". " + subsection)


def add_answers():
    global end_of_file, line, question
    answers = []
    try:
        while check_for_len(line) and not check_for_dash(line):
            answers.append(line.strip())
            line = next(f)
    except StopIteration:
        answers = " ".join(answers)
        topics[section][subsection][0][question] = answers
        end_of_file = True
    if not end_of_file:
        answers = " ".join(answers)
        topics[section][subsection][0][question] = answers


def pose_questions():
    # Default behavior should be list first section and its set of questions,
    # allow inputting an answer, present next question and so on until all sets
    # are done. 
    # TODO: adding store_text.py's fill in the blank as a mode.
    # TODO: adding a multiple choice mode.
    # TODO: adding a matching a to q or q to a mode.
    print("Select mode: \n1. Default")
    mode = input()
    if mode == "1":
        default()
    elif not mode:
        clear_screen()
        sys.exit(0)


def default():
    my_printer = pp.PrettyPrinter(indent=2)
    my_answers = {}
    for section in topics:
        print_topic(section)
        acknowledge = input("Skip section? (y/n) ")
        if acknowledge == "n" or not acknowledge:
            for index, question in enumerate(topics[section][0].keys()):
                q = colored("Question " + str(index + 1) + ": " + question,
                            'yellow')
                print(f"{q}")
                ans = input()
                my_answers[question] = ans
    for section in topics:
        print_topic(section)
        acknowledge = input("Review answers? (y/n) ")
        if acknowledge == 'y' or not acknowledge:
            for question, answer in topics[section][0].items():
                try:
                    if my_answers[question]:
                        print(colored(question, 'yellow'))
                        print(colored("ANS: ", 'green') + answer[2:])
                        print(colored("RES: ", 'magenta') + my_answers[question])
                except KeyError:
                    my_answers[question] = ""
                    continue
       

topics = {}  # A data class should be made for a file and this should be an attr.

# All this stuff should go in a function and be decomposed where similar, if
# possible
with open(sys.argv[1]) as f:
    for line in f:
        end_of_file = False
        if check_for_len(line) and check_for_topic(line):
            header_lvl = check_header_lvl(line)
            if header_lvl == 1:
                section = line.strip()[2:]
                add_section(section)
                line = next(f)
                subsection = ""
                # let section = header[2:]
                # let subsection = ''
                # This way, if adding Q and subsection = '', subsection =
                # section, else continue.
            elif header_lvl == 2:
                subsection = line.strip()[3:]
                add_subsection(subsection)
                line = next(f)
                # subsection = header[3:]
            while check_for_len(line) and not end_of_file:
                if check_for_len(line) and check_for_dash(line):
                    questions = []
                    while (
                        check_for_len(line)
                        and not check_for_star(line)
                        and not check_for_numeric(line)
                    ):
                        questions.append(line.strip())
                        line = next(f)
                    question = " ".join(questions)
                    if subsection == "":
                        subsection = "Introduction"
                        add_subsection(subsection)
                        topics[section][subsection][0][question] = ""
                    else:
                        topics[section][subsection][0][question] = ""
                if check_for_len(line) and check_for_star(line):
                    add_answers()
                elif check_for_len(line) and check_for_numeric(line):
                    add_answers()
                # TODO: Handling code sections that start with ```.


while True:
    print(
        "\nMain Menu \n1. All \n2. Questions \n3. Answers \n4. Q&A's \n5."
        " Q&A per Subsection \n6. Sections \n7. Subsections \n"
    )
    choice = input("Selection: ")
    if choice == "1":
        clear_screen()
        list_all()
    elif choice == "2":
        clear_screen()
        list_questions()
    elif choice == "3":
        clear_screen()
        list_answers()
    elif choice == "4":
        clear_screen()
        list_questions_and_answers()
    elif choice == "5":
        clear_screen()
        list_qna_for_each_section()
    elif choice == "6":
        clear_screen()
        list_sections()
    elif choice == "7":
        clear_screen()
        list_subsections()
    else:
        break

while True:
    pose_questions()


