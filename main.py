# -*- coding: utf-8 -*-
import curses
import json
import matplotlib.pyplot as plt
import random
import sys
import time
import source.consoles
import source.fileutils
import source.tests

end_of_input = ["\n", "\t"]

current_tests = []
all_sentenses = []
console = source.consoles.Console()

def initialize():
    console.send_message("enter your name: ", curses.color_pair(1))
    return console.get_message(is_blind=False)

def start(stdsrc):
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

    name = initialize()
    source.fileutils.FileUtils.save_name(name)
    console.send_message("hello " + name, curses.color_pair(1))
    global all_sentenses
    all_sentenses = source.fileutils.FileUtils.get_all_sentenses()

def print_help():
    console.send_message("""    commands:
    start
    graph
    exit""", curses. color_pair(1))
    for i in range(4):
        console.transport_to_next_line()

def generate_text():
    count_of_sentenses = random.randint(1, 2)
    ans = ""
    for i in range(count_of_sentenses):
        diaposon = len(all_sentenses)
        num = random.randint(0, diaposon)
        ans += all_sentenses[num]
        if i != (count_of_sentenses - 1):
            ans += " "
    return ans

def test():
    text = generate_text()
    num_in_text = 0
    error_count = 0
    speed = 0
    console.send_message(text, color=curses.color_pair(2), without_move=True)

    is_start = False
    while num_in_text < len(text):
        char = console.get_char()

        if not is_start:
            start = time.time()
            is_start = True

        if char != text[num_in_text]:
            error_count += 1
        else:
            console.send_message(char,color=curses.color_pair(3))
            num_in_text += 1

    end = time.time()
    test_time = end - start
    console.transport_to_next_line()
    word_count = len(text.split())
    speed = int(word_count / test_time * 60)

    console.send_message(f"your spped: {speed}", curses.color_pair(2))
    console.transport_to_next_line()
    console.send_message(f"your error {error_count}", curses.color_pair(2))
    console.transport_to_next_line()

    current_tests.append(str(tests.Test(word_count=word_count,
                              error_count=error_count,
                              speed=speed,
                              test_time=test_time)))

def game(stdsrc):
    while True:
        print_help()
        message = console.get_message(is_blind=False)
        message = message.strip()
        console.transport_to_next_line()
        console.send_message(message, curses.color_pair(1))
        console.clear()
        if message == "start":
            test()
        if message == "graph":
            build_graph()
        if message == "exit":
            break
        else:
            console.send_message("not command " + message, curses.color_pair(1))
            console.transport_to_next_line()

def build_graph():
    source.fileutils.FileUtils.upload_test(current_tests)
    current_tests = []
    all_test = source.fileutils.FileUtils.load_all_test()
    x = []
    y_speed = []
    y_error = []
    counter = 1
    for test in all_test:
        x.append(counter)
        y_speed.append(int(test.split()[2]))
        y_error.append(int(test.split()[1]))
        counter += 1
    plt.plot(x, y_speed, label="speed", color="blue")
    plt.plot(x, y_error, label="error", color="red", linestyle="dashed")
    plt.xlabel("attempt")
    plt.ylabel("speed")
    plt.title("WPM grafic")
    plt.show()

def end(stdsrc):
   global current_tests
   source.fileutils.FileUtils.upload_test(current_tests)
   current_tests = []

def main():
    curses.wrapper(start)
    curses.wrapper(game)
    curses.wrapper(end)

if __name__ == "__main__":
    main()
