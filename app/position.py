CHARACTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
LENGTH = len(CHARACTERS)


def get_char_index(character: str) -> int:
    return CHARACTERS.index(character)


def number_to_position(num: int) -> str:
    result = ""
    
    while num > 0:
        result += CHARACTERS[num % LENGTH]
        num //= LENGTH
    
    return "".join(reversed(result))


def position_to_number(pos: str) -> int:
    result = 0
    for index, char in enumerate(reversed(pos)):
        result += get_char_index(char) * (LENGTH ** index)
    return result
