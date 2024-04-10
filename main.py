# -*- coding: utf-8 -*-
import curses
import json
import matplotlib.pyplot as plt
import random
import sys
import time

end_of_input = ["\n", "\t"]

class Test():
    def __init__(self, word_count = 0, error_count = 0, speed = 0, test_time = 0):
        self.word_count = word_count
        self.error_count = error_count
        self.speed = speed
        self.test_time = test_time

    def __str__(self):
        return str(self.word_count) + " " + str(self.error_count) + " " + str(self.speed) + " " + str(self.test_time)

    def getList(self):
        return [self.word_count, self.error_count, self.speed]

current_tests = []

class FileUtils():
    @staticmethod
    def get_all_data(name_of_file):
        with open(name_of_file, "r", encoding="utf-8") as file:
            all_data = json.load(file)
        return all_data

    @staticmethod
    def set_all_data(name_of_file, all_data):
        with open(name_of_file, "w", encoding="utf-8") as file:
            json.dump(all_data, file, indent=2)

    @staticmethod
    def uplouad_count_of_test():
        all_data = FileUtils.get_all_data("source/data.json")
        count_of_test = all_data["count of elements"]
        return count_of_test

    @staticmethod
    def load_all_test():
        all_data = FileUtils.get_all_data("source/data.json")
        all_test = all_data["data of tests"]
        return all_test

    @staticmethod
    def upload_test():
        count_of_test = FileUtils.uplouad_count_of_test()
        all_test = FileUtils.load_all_test()

        global current_tests

        all_test += current_tests
        count_of_test += len(current_tests)

        all_data = FileUtils.get_all_data("source/data.json")

        all_data["data of tests"] = all_test
        all_data["count of elements"] = count_of_test

        FileUtils.set_all_data("source/data.json" , all_data)
        current_tests = []

    @staticmethod
    def save_name(name):
        all_config = FileUtils.get_all_data("source/config.json")

        all_config["name"] = name

        FileUtils.set_all_data("source/config.json", all_config)

    @staticmethod
    def get_name():
        all_config = FileUtils.get_all_data("source/config.json")
        name = all_config["name"]
        return name

    @staticmethod
    def get_all_sentenses():
        all_sentenses = []
        with open("source/sentenses.txt", encoding="utf-8") as file:
            for line in file:
                line = line[:-1]
                all_sentenses.append(line)
        return all_sentenses

class Console():
    def __init__(self):
        self.stdsrc = curses.initscr()

        self.str_count = 0
        self.index_in_str = 0
        self.stdsrc.clear()

    def transport_to_next_line(self):
        self.str_count += 1
        self.index_in_str = 0

    def send_message(self, message, color, without_move=False):
        self.stdsrc.addstr(self.str_count, self.index_in_str, message, color)
        if not without_move:
            temp = self.index_in_str + len(message)
            self.index_in_str = temp % curses.COLS
            self.str_count += temp // curses.COLS
            self.stdsrc.refresh()
            if len(message) >= 1 and message[-1] == "\n":
                self.transport_to_next_line()

    def get_char(self):
        return self.stdsrc.getkey()

    def get_message(self, is_blind=True):
        start_srt = self.str_count
        start_index_in_srt = self.index_in_str
        message = ""
        while True:
            key = self.get_char()

            if key == "KEY_BACKSPACE":
                if self.index_in_str != start_index_in_srt or self.str_count != start_srt:
                    if self.index_in_str == 0:
                        self.str_count -= 1
                        self.index_in_str = curses.COLS - 1;
                    else:
                        self.index_in_str -= 1
                    self.stdsrc.addstr(self.str_count, self.index_in_str, " ")
                    message = message[:-1]
                continue
            else:
                if not is_blind:
                    self.send_message(key, curses.color_pair(2))
                message += key
            if key in end_of_input:
                break
        return message

    def clear(self):
        self.stdsrc.clear()
        self.stdsrc.refresh()
        self.str_count = 0
        self.index_in_str = 0

all_sentenses = []
console = Console()

def initialize():
    console.send_message("enter your name: ", curses.color_pair(1))
    return console.get_message(is_blind=False)

def start(stdsrc):
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

    name = initialize()
    FileUtils.save_name(name)
    console.send_message("hello " + name, curses.color_pair(1))
    global all_sentenses
    all_sentenses = FileUtils.get_all_sentenses()

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

    current_tests.append(str(Test(word_count=word_count,
                              error_count=error_count,
                              speed=speed,
                              test_time=test_time)))

def work(stdsrc):
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
    FileUtils.upload_test()
    all_test = FileUtils.load_all_test()
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
   FileUtils.upload_test()

def main():
    curses.wrapper(start)
    curses.wrapper(work)
    curses.wrapper(end)

if __name__ == "__main__":
    main()

