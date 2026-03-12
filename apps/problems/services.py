from .models import Problem, TestCase, Topic


TOPIC_DATA = [
    ("Datatypes", "datatypes", "Master strings, integers, floats, booleans, and collections.", "#0d6efd"),
    ("Arrays", "arrays", "Practice indexed access, searching, and transformations.", "#198754"),
    ("For Loops", "for-loops", "Build confidence with iteration patterns and counting.", "#fd7e14"),
    ("While Loops", "while-loops", "Handle repetition with conditions and loop control.", "#dc3545"),
    ("Functions", "functions", "Write reusable Python functions with parameters and returns.", "#6f42c1"),
    ("Classes (OOP)", "classes-oop", "Model state and behavior using classes and objects.", "#20c997"),
    ("File Handling", "file-handling", "Read, write, and process file content safely.", "#6610f2"),
    ("Exception Handling", "exception-handling", "Use try, except, and validation for robust code.", "#d63384"),
]


PROBLEM_DATA = {
    "datatypes": [
        {
            "title": "Sum Two Integers",
            "slug": "sum-two-integers",
            "difficulty": "easy",
            "description": "Read two integers from standard input and print their sum.",
            "instructions": "Input arrives as two space-separated integers.",
            "starter_code": "a, b = map(int, input().split())\nprint(a + b)\n",
            "example_input": "3 7",
            "example_output": "10",
            "points": 10,
            "tests": [("3 7", "10"), ("-4 9", "5")],
        },
        {
            "title": "Type Counter",
            "slug": "type-counter",
            "difficulty": "medium",
            "description": "Given a comma-separated string, print the number of values.",
            "instructions": "Count non-empty values only.",
            "starter_code": "items = [item.strip() for item in input().split(',') if item.strip()]\nprint(len(items))\n",
            "example_input": "a, b, c",
            "example_output": "3",
            "points": 15,
            "tests": [("a, b, c", "3"), ("1,2,,4", "3")],
        },
    ],
    "arrays": [
        {
            "title": "Largest Number",
            "slug": "largest-number",
            "difficulty": "easy",
            "description": "Read a list of integers and print the largest number.",
            "instructions": "The first integer is the size, followed by the numbers.",
            "starter_code": "n = int(input())\nnums = list(map(int, input().split()))\nprint(max(nums))\n",
            "example_input": "5\n1 8 3 6 2",
            "example_output": "8",
            "points": 10,
            "tests": [("5\n1 8 3 6 2", "8"), ("4\n-1 -7 -3 -4", "-1")],
        },
        {
            "title": "Array Rotation",
            "slug": "array-rotation",
            "difficulty": "medium",
            "description": "Rotate an array to the left by k steps.",
            "instructions": "Print the rotated array separated by spaces.",
            "starter_code": "n, k = map(int, input().split())\nnums = list(map(int, input().split()))\nk %= n\nrotated = nums[k:] + nums[:k]\nprint(*rotated)\n",
            "example_input": "5 2\n1 2 3 4 5",
            "example_output": "3 4 5 1 2",
            "points": 15,
            "tests": [("5 2\n1 2 3 4 5", "3 4 5 1 2"), ("4 1\n9 8 7 6", "8 7 6 9")],
        },
    ],
    "for-loops": [
        {
            "title": "Even Counter",
            "slug": "even-counter",
            "difficulty": "easy",
            "description": "Count how many even numbers appear in the sequence.",
            "instructions": "The first line is n, the second line contains n integers.",
            "starter_code": "n = int(input())\nnums = list(map(int, input().split()))\nprint(sum(1 for value in nums if value % 2 == 0))\n",
            "example_input": "5\n1 2 3 4 6",
            "example_output": "3",
            "points": 10,
            "tests": [("5\n1 2 3 4 6", "3"), ("4\n1 3 5 7", "0")],
        }
    ],
    "while-loops": [
        {
            "title": "Countdown Sum",
            "slug": "countdown-sum",
            "difficulty": "easy",
            "description": "Given n, sum all integers from n down to 1 using a while loop.",
            "instructions": "Print the final sum.",
            "starter_code": "n = int(input())\ntotal = 0\nwhile n > 0:\n    total += n\n    n -= 1\nprint(total)\n",
            "example_input": "4",
            "example_output": "10",
            "points": 10,
            "tests": [("4", "10"), ("1", "1")],
        }
    ],
    "functions": [
        {
            "title": "Greeting Function",
            "slug": "greeting-function",
            "difficulty": "easy",
            "description": "Create a function that prints Hello, followed by the given name.",
            "instructions": "Input is a single name.",
            "starter_code": "def greet(name):\n    return f\"Hello, {name}\"\n\nname = input().strip()\nprint(greet(name))\n",
            "example_input": "Raj",
            "example_output": "Hello, Raj",
            "points": 10,
            "tests": [("Raj", "Hello, Raj"), ("Python", "Hello, Python")],
        }
    ],
    "classes-oop": [
        {
            "title": "Simple Counter Class",
            "slug": "simple-counter-class",
            "difficulty": "medium",
            "description": "Create a Counter class that increments a value n times and prints the final count.",
            "instructions": "Input is the number of increments.",
            "starter_code": "class Counter:\n    def __init__(self):\n        self.value = 0\n\n    def increment(self):\n        self.value += 1\n\ncounter = Counter()\nfor _ in range(int(input())):\n    counter.increment()\nprint(counter.value)\n",
            "example_input": "5",
            "example_output": "5",
            "points": 15,
            "tests": [("5", "5"), ("0", "0")],
        }
    ],
    "file-handling": [
        {
            "title": "Line Count Simulator",
            "slug": "line-count-simulator",
            "difficulty": "medium",
            "description": "Simulate file line counting by receiving text separated with | and printing the line count.",
            "instructions": "Treat each | character as a new line separator.",
            "starter_code": "content = input().strip()\nprint(len([line for line in content.split('|') if line != '']))\n",
            "example_input": "a|b|c",
            "example_output": "3",
            "points": 15,
            "tests": [("a|b|c", "3"), ("one|two", "2")],
        }
    ],
    "exception-handling": [
        {
            "title": "Safe Division",
            "slug": "safe-division",
            "difficulty": "medium",
            "description": "Read two integers and print the division result or 'Cannot divide'.",
            "instructions": "Use exception handling to catch division by zero.",
            "starter_code": "a, b = map(int, input().split())\ntry:\n    print(a // b)\nexcept ZeroDivisionError:\n    print('Cannot divide')\n",
            "example_input": "8 2",
            "example_output": "4",
            "points": 15,
            "tests": [("8 2", "4"), ("5 0", "Cannot divide")],
        }
    ],
}


def seed_initial_content():
    topic_lookup = {}
    for index, (title, slug, description, color) in enumerate(TOPIC_DATA, start=1):
        topic, _ = Topic.objects.get_or_create(
            slug=slug,
            defaults={
                "title": title,
                "description": description,
                "order": index,
                "accent_color": color,
            },
        )
        topic_lookup[slug] = topic

    for slug, problems in PROBLEM_DATA.items():
        topic = topic_lookup[slug]
        for order, payload in enumerate(problems, start=1):
            problem, _ = Problem.objects.get_or_create(
                slug=payload["slug"],
                defaults={
                    "topic": topic,
                    "title": payload["title"],
                    "difficulty": payload["difficulty"],
                    "description": payload["description"],
                    "instructions": payload["instructions"],
                    "starter_code": payload["starter_code"],
                    "example_input": payload["example_input"],
                    "example_output": payload["example_output"],
                    "order": order,
                    "is_daily_challenge": payload["slug"] == "array-rotation",
                    "points": payload["points"],
                },
            )
            if not problem.test_cases.exists():
                for case_order, (case_input, expected_output) in enumerate(payload["tests"], start=1):
                    TestCase.objects.create(
                        problem=problem,
                        input_data=case_input,
                        expected_output=expected_output,
                        is_sample=(case_order == 1),
                        order=case_order,
                    )
