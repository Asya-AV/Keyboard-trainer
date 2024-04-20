import json

class FileUtils:
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
    def upload_test(current_tests):
        count_of_test = FileUtils.uplouad_count_of_test()
        all_test = FileUtils.load_all_test()

        all_test += current_tests
        count_of_test += len(current_tests)

        all_data = FileUtils.get_all_data("source/data.json")

        all_data["data of tests"] = all_test
        all_data["count of elements"] = count_of_test

        FileUtils.set_all_data("source/data.json" , all_data)

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
