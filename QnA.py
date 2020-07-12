import sys
import pprint as pp

def check_for_len(line):
    return len(line.strip())


def check_for_dash(line):
    return line.strip()[0] == '-'


def check_for_star(line):
    return line.strip()[0] == '*'


def check_for_header(line):
    return line.strip()[0].isalpha()


def list_all():
    for header in headers:
        for i in range(len(headers[header])):
            pp.pprint(headers[header][i])


def list_headers():
    for header in headers:
        print(header)


def list_questions_and_answers():
    for header in headers:
        for question, answer in headers[header][0].items():
            print("\n")
            print(header)
            print("Q: " + question)
            print("A: " + answer)


def list_qna_for_header():
    my_printer = pp.PrettyPrinter(indent=4)
    for topic in headers:
        print(topic)
        for question, answer in headers[topic][0].items():
            print("Q: " + question[2:])
            my_printer.pprint("A: " + answer[2:])
        print("\n")


def list_questions():
    for header in headers:
        for question, answer in headers[header][0].items():
            print("Q: " + question)


def list_answers():
    for header in headers:
        for question, answer in headers[header][0].items():
            print("A:" + answer)


def pose_questions():
    # Default behavior should be list first header and its set of questions,
    # allow inputting an answer, present next question and so on until all sets
    # are done.
    print("Select mode \n1. Default")
    mode = input()
    if mode == '1':
        default()
    elif not mode:
        sys.exit(0)
    

def default():
    my_printer = pp.PrettyPrinter(indent=2)
    my_answers = {}
    for header in headers:
        print("= " * len(header) + header.upper() + " =" * len(header))
        acknowledge = input("Skip? (y/n) ")
        if acknowledge == 'n' or not acknowledge:
            for index, question in enumerate(headers[header][0].keys()):
                print(f"Question {index + 1}: {question}")
                ans = input()
                my_answers[question] = ans
    my_printer.pprint(my_answers)
    pose_questions()
                



headers = {} # A class should be made for a file and this should be an attr.

# All this stuff should go in a function and be decomposed where similar, if
# possible
with open(sys.argv[1]) as f:
    for line in f:
        if check_for_len(line) and check_for_header(line):
            header = line.strip()
            headers[header] = []
            headers[header].append({})
            line = next(f)
            while check_for_len(line):
                if check_for_len(line) and check_for_dash(line):
                    questions = []
                    while check_for_len(line) and not check_for_star(line):
                        questions.append(line.strip())
                        line = next(f)
                    question = " ".join(questions)
                    headers[header][0][question] = ''
                if check_for_len(line) and check_for_star(line):
                    answers = []
                    try:
                        while check_for_len(line) and not check_for_dash(line):
                            answers.append(line.strip())
                            line = next(f)
                    except StopIteration:
                        answers = " ".join(answers)
                        headers[header][0][question] = answers
                        break
                    answers = " ".join(answers)
                    headers[header][0][question] = answers



while False:
    print("Main Menu \n1. All \n2. Questions \n3. Answers \n4. Q&A's \n5."
            "Headers \n6. Q&A per Header\n")
    choice = input("Selection: ")
    if choice == '1':
        list_all()
    elif choice == '2':
        list_questions()
    elif choice == '3':
        list_answers()
    elif choice == '4':
        list_questions_and_answers()
    elif choice == '5':
        list_headers()
    elif choice == '6':
        list_qna_for_header()
    else:
        break

while True:
    pose_questions()

# list_questions_and_answers()

