import sys, shutil
import pprint as pp


def check_for_len(line):
    return len(line.strip())


def check_for_dash(line):
    return line.strip()[0] == "-"


def check_for_star(line):
    return line.strip()[0] == "*"


def check_for_topic(line):
    return line.strip()[0].isalpha()


def check_for_numeric(line):
    return line.strip()[0].isnumeric()

def print_topic(topic):
    term_columns = shutil.get_terminal_size()[0]
    print("=" * term_columns)
    print("|" + (term_columns - 2) * " " + "|")
    print("|" + (term_columns - len(topic))//2 * " " + topic.upper() +
          (term_columns - 3 - len(topic))//2 * " " + "|")
    print("|" + (term_columns - 2) * " " + "|")
    print("=" * term_columns)


def list_all():
    for topic in topics:
        for i in range(len(topics[topic])):
            pp.pprint(topics[topic][i])


def list_topics():
    for topic in topics:
        print_topic(topic)


def list_questions_and_answers():
    for topic in topics:
        print_topic(topic)
        for question, answer in topics[topic][0].items():
            print(question)
            print("   " + answer)
            print("\n")


def list_qna_for_topic():
    my_printer = pp.PrettyPrinter(indent=4)
    for topic in topics:
        print(topic)
        for question, answer in topics[topic][0].items():
            print("Q: " + question[2:])
            my_printer.pprint("A: " + answer[2:])
        print("\n")


def list_questions():
    for topic in topics:
        for question, answer in topics[topic][0].items():
            print("Q: " + question)


def list_answers():
    for topic in topics:
        for question, answer in topics[topic][0].items():
            print("A:" + answer)


def add_answers():
    global end_of_file, line, question
    answers = []
    try:
        while check_for_len(line) and not check_for_dash(line):
            answers.append(line.strip())
            line = next(f)
    except StopIteration:
        answers = " ".join(answers)
        topics[topic][0][question] = answers
        end_of_file = True
    if not end_of_file:
        answers = " ".join(answers)
        topics[topic][0][question] = answers


def pose_questions():
    # Default behavior should be list first topic and its set of questions,
    # allow inputting an answer, present next question and so on until all sets
    # are done.
    print("Select mode \n1. Default")
    mode = input()
    if mode == "1":
        default()
    elif not mode:
        sys.exit(0)


def default():
    my_printer = pp.PrettyPrinter(indent=2)
    my_answers = {}
    for topic in topics:
        print("=" * len(topic) + topic.upper() + "=" * len(topic))
        acknowledge = input("Skip? (y/n) ")
        if acknowledge == "n" or not acknowledge:
            for index, question in enumerate(topics[topic][0].keys()):
                print(f"Question {index + 1}: {question}")
                ans = input()
                my_answers[question] = ans
    my_printer.pprint(my_answers)


topics = {}  # A class should be made for a file and this should be an attr.

# All this stuff should go in a function and be decomposed where similar, if
# possible
with open(sys.argv[1]) as f:
    for line in f:
        end_of_file = False
        if check_for_len(line) and check_for_topic(line):
            topic = line.strip()
            topics[topic] = []
            topics[topic].append({})
            line = next(f)
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
                    topics[topic][0][question] = ""
                if check_for_len(line) and check_for_star(line):
                    add_answers()
                elif check_for_len(line) and check_for_numeric(line):
                    add_answers()


while True:
    print(
        "Main Menu \n1. All \n2. Questions \n3. Answers \n4. Q&A's \n5."
        " topics \n6. Q&A per topic\n"
    )
    choice = input("Selection: ")
    if choice == "1":
        list_all()
    elif choice == "2":
        list_questions()
    elif choice == "3":
        list_answers()
    elif choice == "4":
        list_questions_and_answers()
    elif choice == "5":
        list_topics()
    elif choice == "6":
        list_qna_for_topic()
    else:
        break

while True:
    pose_questions()
