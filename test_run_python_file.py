from functions.run_python_file import run_python_file


def main():
    # 1) main.py usage
    print('run_python_file("calculator", "main.py"):')
    print(run_python_file("calculator", "main.py"))
    print()

    # 2) main.py with args
    print('run_python_file("calculator", "main.py", ["3 + 5"]):')
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print()

    # 3) tests.py
    print('run_python_file("calculator", "tests.py"):')
    print(run_python_file("calculator", "tests.py"))
    print()

    # 4) ../main.py (outside)
    print('run_python_file("calculator", "../main.py"):')
    print(run_python_file("calculator", "../main.py"))
    print()

    # 5) Nonexistent
    print('run_python_file("calculator", "nonexistent.py"):')
    print(run_python_file("calculator", "nonexistent.py"))
    print()

    # 6) lorem.txt (not .py)
    print('run_python_file("calculator", "lorem.txt"):')
    print(run_python_file("calculator", "lorem.txt"))


if __name__ == "__main__":
    main()
