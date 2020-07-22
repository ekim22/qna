#!/usr/bin/env python3

import sys, shutil, subprocess
import re
import pprint as pp
from os import system, name
from termcolor import colored


class roman_numeral:
    def int_to_Roman(self, num):
        val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
        sym = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
        roman_num = ""
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
    return line.strip()[0] == "#"


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
    if name == "nt":
        _ = system("cls")
    # for mac and linux
    else:
        _ = subprocess.run(["clear"])
        _ = subprocess.run(["echo", "-en", "\e[3J"])


def print_topic(section, total_subsections=None):
    if total_subsections == None:
        term_columns = shutil.get_terminal_size()[0]
        print("=" * term_columns)
        # print("|" + (term_columns - 2) * " " + "|")
        print(
            "|"
            + (term_columns - len(section)) // 2 * " "
            + colored(section.upper(), attrs=["bold"])
            + (term_columns - 3 - len(section)) // 2 * " "
            + "|"
        )
        # print("|" + (term_columns - 2) * " " + "|")
        print("=" * term_columns)
    else:
        section += f" [{total_subsections}]"
        term_columns = shutil.get_terminal_size()[0]
        print("=" * term_columns)
        # print("|" + (term_columns - 2) * " " + "|")
        print(
            "|"
            + (term_columns - len(section)) // 2 * " "
            + colored(section.upper(), attrs=["bold"])
            + (term_columns - 3 - len(section)) // 2 * " "
            + "|"
        )
        # print("|" + (term_columns - 2) * " " + "|")
        print("=" * term_columns)


def print_subsection(subsection, total_questions=None):
    term_columns = shutil.get_terminal_size()[0]
    if total_questions == None:
        print()
        print(
            (term_columns - 1 - len(subsection)) // 2 * " "
            + colored(subsection, attrs=["bold",])
            + "\n"
        )
    else:
        print()
        print(
            (term_columns - 1 - len(subsection)) // 2 * " "
            + colored(subsection, attrs=["bold",])
            + colored(f" [{total_questions}]", attrs=["bold"])
            + "\n"
        )


def print_end_of_session(session_type):
    term_columns = shutil.get_terminal_size()[0]
    done_stmt = "END OF " + session_type.upper()
    print(
        (term_columns - len(done_stmt)) // 2 * "-"
        + colored(done_stmt, attrs=["blink", "bold"])
        + (term_columns - len(done_stmt)) // 2 * "-"
    )


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
        for subsection in topics[section]:
            for question in topics[section][subsection][0].keys():
                print(colored("Q: ", "cyan") + question[2:])


def list_answers():
    for section in topics:
        for subsection in topics[section]:
            for answer in topics[section][subsection][0].values():
                print(colored("A: ", "magenta") + answer[2:])


def list_questions_and_answers():
    my_printer = pp.PrettyPrinter(width=200)
    for section in topics:
        for subsection in topics[section]:
            for question, answer in topics[section][subsection][0].items():
                print(colored("Q: ", "cyan") + colored(question[2:]))
                print(colored("A: ", "magenta") + answer[2:])


def list_qna_for_each_section():
    my_printer = pp.PrettyPrinter(width=200)
    for section in topics:
        print_topic(section)
        numeral = 1
        for subsection in topics[section]:
            rn = roman_numeral()
            print_subsection(rn.int_to_Roman(numeral) + ". " + subsection)
            numeral += 1
            for q, a in topics[section][subsection][0].items():
                print(colored("Q: ", "cyan") + q[2:])
                print(colored("A: ", "magenta") + a[2:])
        print("\n")


def list_sections():
    for section in topics:
        print_topic(section)


def list_subsections():
    rn = roman_numeral()
    for section in topics:
        print_topic(section)
        for index, subsection in enumerate(topics[section]):
            print(
                colored(rn.int_to_Roman(index + 1) + ". " + subsection, attrs=["bold"])
            )


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
    print("Select mode: \n1. Default \n2. By Section")
    mode = input()
    if mode == "1":
        clear_screen()
        default()
    elif mode == "2":
        clear_screen()
        section = select_section()
        test_section(section)
    elif not mode:
        clear_screen()
        sys.exit(0)


def default():
    # my_printer = pp.PrettyPrinter(indent=2)
    my_answers = {}
    print(colored("STARTING TESTING SESSION...", "green", "on_red", attrs=["bold"]))
    for section in topics:
        print_topic(section)
        acknowledge = input("Attempt? (Yn) ")
        if acknowledge == "y":
            for subsection in topics[section]:
                print_subsection(subsection)
                for index, question in enumerate(topics[section][subsection][0].keys()):
                    q = (
                        colored("Question " + str(index + 1) + ": ", "cyan")
                        + question[2:]
                    )
                    print(f"{q}")
                    ans = input()
                    my_answers[question] = ans

    print(colored("STARTING REVIEW SESSION...", "red", "on_green", attrs=["bold"]))
    for section in topics:
        print_topic(section)
        acknowledge = input("View answers? (Yn) ")
        if acknowledge == "y":
            for subsection in topics[section]:
                print_subsection(subsection)
                for question, answer in topics[section][subsection][0].items():
                    try:
                        if my_answers[question]:
                            print(colored("Q: ", "cyan") + question[2:])
                            print(colored("A: ", "green") + answer[2:])
                            print(colored("R: ", "magenta") + my_answers[question])
                            input()
                    except KeyError:
                        my_answers[question] = ""
                        continue


def select_section():
    section_list = []
    for section in topics:
        section_list.append(section)
        print_topic(section)

    for index, section in enumerate(section_list):
        print(str(index + 1) + ". " + section)
    while True:
        try:
            selection = int(input("\nSelect section for testing: "))
            return section_list[selection - 1]
        except ValueError:
            print("Invalid input.")
        except IndexError:
            print("Out of range.")
        else:
            break


def test_section(section):
    clear_screen()
    my_answers = {}
    print(colored("STARTING TESTING SESSION...", "green", "on_red", attrs=["bold"]))
    print_topic(section, len(topics[section]))
    acknowledge = input("Attempt? (Yn) ")
    if acknowledge.lower() == "y":
        for subsection in topics[section]:
            print_subsection(subsection, len(topics[section][subsection][0]))
            for index, question in enumerate(topics[section][subsection][0].keys()):
                q = colored("Question " + str(index + 1) + ": ", "cyan") + question[2:]
                print(f"{q}")
                ans = input()
                my_answers[question] = ans
    print_end_of_session("testing")
    input()
    clear_screen()
    print(colored("STARTING REVIEW SESSION...", "red", "on_green", attrs=["bold"]))
    print_topic(section, len(topics[section]))
    if acknowledge.lower() == "y":
        acknowledge = input("View answers? (Yn) ")
        if acknowledge.lower() == "y":
            for subsection in topics[section]:
                print_subsection(subsection, len(topics[section][subsection][0]))
                for question, answer in topics[section][subsection][0].items():
                    try:
                        if my_answers[question]:
                            print(colored("Q: ", "cyan") + question[2:])
                            print(colored("A: ", "green") + answer[2:])
                            print(colored("R: ", "magenta") + my_answers[question])
                            input()
                    except KeyError:
                        my_answers[question] = ""
                        continue
    print_end_of_session("review")
    input()


def random_questions():
    # Can randomize sections
    # Can randomize subsections
    # Can randomize questions
    pass


def multiple_choice():
    pass


def fill_in_the_blank():
    pass


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

clear_screen()
while False:
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
    clear_screen()
    pose_questions()
