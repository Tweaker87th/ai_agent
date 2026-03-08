from functions.get_file_content import get_file_content


def main():
    # 1) Test lorem.txt truncation
    print('get_file_content("calculator", "lorem.txt"):')
    lorem_content = get_file_content("calculator", "lorem.txt")
    print(f"Length: {len(lorem_content)} chars")
    if "[...File \"lorem.txt\" truncated at 10000 characters]" in lorem_content:
        print("✓ Truncation message present")
    else:
        print("✗ No truncation message")
    print()

    # 2) main.py
    print('get_file_content("calculator", "main.py"):')
    print(get_file_content("calculator", "main.py"))
    print()

    # 3) pkg/calculator.py
    print('get_file_content("calculator", "pkg/calculator.py"):')
    print(get_file_content("calculator", "pkg/calculator.py"))
    print()

    # 4) /bin/cat (outside)
    print('get_file_content("calculator", "/bin/cat"):')
    print(get_file_content("calculator", "/bin/cat"))
    print()

    # 5) Non-existent file
    print('get_file_content("calculator", "pkg/does_not_exist.py"):')
    print(get_file_content("calculator", "pkg/does_not_exist.py"))


if __name__ == "__main__":
    main()
