from functions.write_file import write_file


def main():
    # 1) Write to lorem.txt in calculator/
    print('write_file("calculator", "lorem.txt", "wait, this isn\'t lorem ipsum"):')
    result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(result)

    print()  # blank line

    # 2) Write to pkg/morelorem.txt in calculator/
    print('write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"):')
    result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(result)

    print()  # blank line

    # 3) Try to write to /tmp/temp.txt (outside working dir)
    print('write_file("calculator", "/tmp/temp.txt", "this should not be allowed"):')
    result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(result)


if __name__ == "__main__":
    main()
