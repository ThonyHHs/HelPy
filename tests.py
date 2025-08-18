from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def get_files_info_test():
    tests = [
        ["calculator", "."],
        ["calculator", "pkg"],
        ["calculator", "/bin"],
        ["calculator", "../"],
    ]

    for test in tests:
        print(f"Result for '{test[1]}' directory")
        print(get_files_info(test[0], test[1]))
        print()

def get_file_content_test():
    tests = [
        ["calculator", "main.py"],
        ["calculator", "pkg/calculator.py"],
        ["calculator", "/bin/cat"],
        ["calculator", "pkg/does_not_exist.py"],
        ["calculator", "lorem.txt"],
    ]

    for test in tests:
        print(f"Result for '{test[1]}' directory")
        print(get_file_content(test[0], test[1]))
        print()

def write_file_test():
    tests = [
        ["calculator", "lorem.txt", "wait, this isn't lorem ipsum"],
        ["calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"],
        ["calculator", "/tmp/temp.txt", "this should not be allowed"],
    ]

    for test in tests:
        print(f"Result for '{test[1]}' directory")
        print(write_file(test[0], test[1], test[2]))
        print()

def run_python_file_test():
    tests = [
        ["calculator", "main.py"],
        ["calculator", "main.py", ["3 + 5"]],
        ["calculator", "tests.py"],
        ["calculator", "../main.py"],
        ["calculator", "nonexistent.py"],
    ]

    for test in tests:
        print(f"Result for '{test[1]}' directory")
        if len(test) == 3:
            print(run_python_file(test[0], test[1], test[2]))
        else:
            print(run_python_file(test[0], test[1]))

        print()
        

if __name__ == "__main__":
    # get_files_info_test()
    # get_file_content_test()
    # write_file_test()
    run_python_file_test()