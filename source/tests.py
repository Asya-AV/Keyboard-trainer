class Test:
    def __init__(self, word_count = 0, error_count = 0, speed = 0, test_time = 0):
        self.word_count = word_count
        self.error_count = error_count
        self.speed = speed
        self.test_time = test_time

    def __str__(self):
        return str(self.word_count) + " " + str(self.error_count) + " " + str(self.speed) + " " + str(self.test_time)

    def getList(self):
        return [self.word_count, self.error_count, self.speed]