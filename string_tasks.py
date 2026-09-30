"""Python implementations for the 15 string practice tasks."""


TASKS = [
    {"id": 1, "title": "String indexing", "group": "Fundamentals", "fields": []},
    {"id": 2, "title": "String slicing", "group": "Fundamentals", "fields": [{"name": "text", "label": "Enter a string", "placeholder": "Python is easy", "multiline": True}]},
    {"id": 3, "title": "Uppercase & lowercase", "group": "Fundamentals", "fields": [{"name": "name", "label": "Your name", "placeholder": "Yash Kumar"}]},
    {"id": 4, "title": "Replace text", "group": "Fundamentals", "fields": [{"name": "sentence", "label": "Enter a sentence", "placeholder": "I am learning Python", "multiline": True}]},
    {"id": 5, "title": "Split a sentence", "group": "Fundamentals", "fields": [{"name": "sentence", "label": "Enter a sentence", "placeholder": "Python is very easy", "multiline": True}]},
    {"id": 6, "title": "Join words", "group": "Fundamentals", "fields": []},
    {"id": 7, "title": "Name formatting", "group": "Fundamentals", "fields": [{"name": "first_name", "label": "First name", "placeholder": "  yash  "}, {"name": "last_name", "label": "Last name", "placeholder": "  kumar  "}]},
    {"id": 8, "title": "F-string bill", "group": "Everyday strings", "fields": [{"name": "product", "label": "Product name", "placeholder": "Laptop"}, {"name": "price", "label": "Price (₹)", "type": "number", "step": "0.01", "placeholder": "50000"}, {"name": "quantity", "label": "Quantity", "type": "number", "step": "1", "placeholder": "2"}]},
    {"id": 9, "title": "Palindrome checker", "group": "Everyday strings", "fields": [{"name": "word", "label": "Enter a word", "placeholder": "Madam"}]},
    {"id": 10, "title": "Word counter", "group": "Everyday strings", "fields": [{"name": "sentence", "label": "Enter a sentence", "placeholder": "Python is easy to learn", "multiline": True}]},
    {"id": 11, "title": "Character counter", "group": "Count & inspect", "fields": [{"name": "text", "label": "Enter some text", "placeholder": "Python is easy", "multiline": True}]},
    {"id": 12, "title": "Vowel counter", "group": "Count & inspect", "fields": [{"name": "text", "label": "Enter some text", "placeholder": "education"}]},
    {"id": 13, "title": "Remove spaces", "group": "Count & inspect", "fields": [{"name": "sentence", "label": "Enter a sentence", "placeholder": "Python is easy", "multiline": True}]},
    {"id": 14, "title": "Reverse each word", "group": "Count & inspect", "fields": [{"name": "sentence", "label": "Enter a sentence", "placeholder": "Python is easy", "multiline": True}]},
    {"id": 15, "title": "String analyzer", "group": "Count & inspect", "fields": [{"name": "sentence", "label": "Enter a sentence", "placeholder": "Python is easy to learn", "multiline": True}]},
]


def run_task(task_id, data):
    """Run one task with submitted form values and return a display string."""
    if task_id == 1:
        text = "Python Programming"
        return (
            f"First character: {text[0]}\n"
            f"Last character: {text[-1]}\n"
            f"5th character: {text[4]}\n"
            f"Last 5 characters: {text[-5:]}"
        )

    if task_id == 2:
        text = _required(data, "text")
        return (
            f"First 5 characters: {text[:5]}\n"
            f"Last 5 characters: {text[-5:]}\n"
            f"Characters at index 2 to 7: {text[2:8]}\n"
            f"Reversed: {text[::-1]}"
        )

    if task_id == 3:
        name = _required(data, "name")
        return f"Original: {name}\nUppercase: {name.upper()}\nLowercase: {name.lower()}"

    if task_id == 4:
        sentence = _required(data, "sentence")
        return sentence.replace("Python", "Programming")

    if task_id == 5:
        words = _required(data, "sentence").split()
        return f"List: {words!r}\n\nWords, one per line:\n" + "\n".join(words)

    if task_id == 6:
        words = ["Python", "is", "very", "easy"]
        return (
            f"Spaces: {' '.join(words)}\n"
            f"Hyphens: {'-'.join(words)}\n"
            f"Commas: {','.join(words)}"
        )

    if task_id == 7:
        first_name = " ".join(_required(data, "first_name").split()).title()
        last_name = " ".join(_required(data, "last_name").split()).title()
        return f"Full Name: {' '.join(part for part in (first_name, last_name) if part)}"

    if task_id == 8:
        product = _required(data, "product").strip()
        try:
            price = float(_required(data, "price"))
            quantity = int(_required(data, "quantity"))
        except ValueError as error:
            raise ValueError("Enter a valid price and whole-number quantity.") from error
        total = price * quantity
        return (
            f"Product: {product}\n"
            f"Price: ₹{price:.2f}\n"
            f"Quantity: {quantity}\n"
            f"Total: ₹{total:.2f}"
        )

    if task_id == 9:
        word = _required(data, "word").strip()
        if word.casefold() == word[::-1].casefold():
            return "Palindrome"
        return "Not a palindrome"

    if task_id == 10:
        words = _required(data, "sentence").split()
        return f"Number of words: {len(words)}"

    if task_id == 11:
        text = _required(data, "text")
        vowels = sum(character.casefold() in "aeiou" for character in text)
        consonants = sum(character.isalpha() and character.casefold() not in "aeiou" for character in text)
        return (
            f"Total characters: {len(text)}\n"
            f"Spaces: {text.count(' ')}\n"
            f"Vowels: {vowels}\n"
            f"Consonants: {consonants}"
        )

    if task_id == 12:
        text = _required(data, "text").casefold()
        return "\n".join(f"{vowel} = {text.count(vowel)}" for vowel in "aeiou")

    if task_id == 13:
        return _required(data, "sentence").replace(" ", "")

    if task_id == 14:
        words = _required(data, "sentence").split()
        return " ".join(word[::-1] for word in words)

    if task_id == 15:
        sentence = _required(data, "sentence")
        vowels = sum(character.casefold() in "aeiou" for character in sentence)
        return (
            f"Original sentence: {sentence}\n"
            f"Uppercase: {sentence.upper()}\n"
            f"Lowercase: {sentence.lower()}\n"
            f"Number of words: {len(sentence.split())}\n"
            f"Number of characters: {len(sentence)}\n"
            f"Number of vowels: {vowels}\n"
            f"Reversed sentence: {sentence[::-1]}"
        )

    raise ValueError("That exercise does not exist.")


def _required(data, name):
    value = data.get(name)
    if value is None or not isinstance(value, str) or not value.strip():
        raise ValueError("Please fill in the required field.")
    return value