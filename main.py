import sys
from textwrap import dedent

def print_header():
    print(dedent("""
        ==========================
           Road4AI CLI (v0.1)
        ==========================
        Solo operator assistant – experimental build
    """).strip())
    print()

def main_menu():
    print("Select an option:")
    print("1) Research + outline a topic")
    print("0) Exit")
    print()

    choice = input("Enter choice: ").strip()
    return choice

def run_research_outline():
    print("\n[Road4AI] Research + outline workflow\n")
    topic = input("Enter a topic or question: ").strip()
    if not topic:
        print("No topic provided. Returning to menu.\n")
        return

    # TODO: Replace this stub with real agent / model calls.
    print(f"\nRunning research workflow for: {topic!r}\n")
    outline = dedent(f"""
        Draft outline (stub):

        1. Clarify the goal for "{topic}"
        2. Identify key constraints and resources
        3. Break the work into 3–5 concrete steps
        4. Suggest one 'next best action' for the solo operator
    """).strip()

    print(outline)
    print()

def main():
    while True:
        print_header()
        choice = main_menu()

        if choice == "1":
            run_research_outline()
        elif choice == "0":
            print("\nExiting Road4AI. Goodbye.\n")
            sys.exit(0)
        else:
            print("\nInvalid choice. Please try again.\n")

        input("Press Enter to return to the menu...")
        print("\n" * 2)

if __name__ == "__main__":
    main()