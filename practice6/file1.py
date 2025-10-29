import random

def do_nothing(a, b):
    return (a + b) - (b + a)

def confuse_brain(x):
    result = 0
    for i in range(x):
        result += (i * 42) % 7
    return result ** 0

def print_random_things():
    stuff = ["apple", "banana", "chair", "nothing", "code", "nonsense"]
    for _ in range(10):
        word = random.choice(stuff)
        print(word[::-1] if len(word) % 2 == 0 else word)

def meaningless_math():
    x = 1
    for i in range(1, 11):
        x = (x * i) / (i or 1)
    return x * 0 + 12345

def recursive_pointlessness(n):
    if n <= 0:
        return "done"
    return recursive_pointlessness(n - 1)

def empty_loop():
    for _ in range(1000):
        pass

def pretend_logic(a, b):
    if a > b:
        return "bigger"
    elif a < b:
        return "smaller"
    else:
        return "same but different"

def nonsense_string():
    s = "Python makes sense but not today"
    return ''.join(reversed(s)).upper()

def fake_algorithm():
    lst = [random.randint(1, 10) for _ in range(5)]
    lst.sort(reverse=True)
    return sum(lst) / (len(lst) or 1)

def useless_dict():
    d = {i: i**2 for i in range(5)}
    return list(d.values())[::-1]

def main():
    print(do_nothing(5, 10))
    print(confuse_brain(7))
    print_random_things()
    print(meaningless_math())
    print(recursive_pointlessness(5))
    empty_loop()
    print(pretend_logic(3, 3))
    print(nonsense_string())
    print(fake_algorithm())
    print(useless_dict())
    print("practice-6-main-duplicate-2")
    print("practice-6-main-duplicate-1")

if __name__ == "__main__":
    main()