from functions.get_files_info import get_files_info


def main():
    # 1) Current directory under "calculator"
    print('get_files_info("calculator", "."):')
    result = get_files_info("calculator", ".")
    print("Result for current directory:")
    for line in result.splitlines():
        print(f"  {line}")

    print()  # blank line

    # 2) 'pkg' directory under "calculator"
    print('get_files_info("calculator", "pkg"):')
    result = get_files_info("calculator", "pkg")
    print("Result for 'pkg' directory:")
    for line in result.splitlines():
        print(f"  {line}")

    print()  # blank line

    # 3) absolute /bin (should be outside)
    print('get_files_info("calculator", "/bin"):')
    result = get_files_info("calculator", "/bin")
    print("Result for '/bin' directory:")
    print(f"    {result}")

    print()  # blank line

    # 4) parent directory ../ (should be outside)
    print('get_files_info("calculator", "../"):')
    result = get_files_info("calculator", "../")
    print("Result for '../' directory:")
    print(f"    {result}")


if __name__ == "__main__":
    main()
