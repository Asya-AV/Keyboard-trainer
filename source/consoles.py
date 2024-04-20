import curses

end_of_input = ["\n", "\t"]

class Console:
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
