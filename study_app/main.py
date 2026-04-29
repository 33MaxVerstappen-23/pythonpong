from questions import get_question

def main():
    print("Welcome to Competitive Exam Study App")
    print("Subjects: math, physics, chemistry")
    subject = input("Select subject: ").lower().strip()
    if subject not in ['math', 'physics', 'chemistry']:
        print("Invalid subject")
        return

    print("Levels: 1-5")
    try:
        level = int(input("Select level (1-5): "))
        if level not in range(1, 6):
            print("Invalid level")
            return
    except ValueError:
        print("Invalid input")
        return

    questions = [get_question(subject, level, i) for i in range(20)]
    score = 0

    for i, q in enumerate(questions):
        print(f"\nQuestion {i+1}/20: {q['question']}")
        for j, opt in enumerate(q['options']):
            print(f"{j+1}. {opt}")
        try:
            ans = int(input("Your answer (1-4): ")) - 1
            if ans == q['correct']:
                score += 1
                print("Correct!")
            else:
                print(f"Wrong! Correct is: {q['options'][q['correct']]}")
        except (ValueError, IndexError):
            print("Invalid answer, skipping")

    percentage = (score / 20) * 100
    print(f"\nQuiz Complete! Score: {score}/20 ({percentage:.2f}%)")

if __name__ == "__main__":
    main()