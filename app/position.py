CHARACTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
LENGTH = len(CHARACTERS)


def position_to_number(position: str) -> int:
    result: int = 0

    for index, char in enumerate(reversed(position)):
        result += get_char_number(char) * (LENGTH ** index)
    
    return result


def get_next_position(position: str) -> str:
    next_number = position_to_number(position) + 1
    next_position: str = number_to_position(next_number)
    return next_position


def get_none_position() -> str:
    return CHARACTERS[0]


def get_char_number(char: str) -> int:
    return CHARACTERS.index(char) + 1


def get_char_by_charnumber(charnumber: int) -> str:
    return CHARACTERS[charnumber - 1]


def get_next_char(char: str) -> str:
    if char[-1] == CHARACTERS[-1]:
        raise ValueError("Argument is final character")
    
    next_index = CHARACTERS.index(char) + 1
    return CHARACTERS[next_index]


def number_to_position(number_value: int) -> str:
    results: list[str] = []

    while number_value > 0:
        charnumber: int = number_value % LENGTH
        char = get_char_by_charnumber(charnumber)

        results.append(char)
        number_value //= LENGTH

        if charnumber == 0:
            number_value -= 1
    
    result: str = "".join(reversed(results))
    return result


def get_average_position(pos1: str, pos2: str) -> str:
    if pos1 == pos2:
        raise ValueError("Both positions are equal")
    
    pos1_number = position_to_number(pos1)
    pos2_number = position_to_number(pos2)

    average_number = (pos1_number + pos2_number) // 2
    average_position = number_to_position(average_number)
    
    if average_number == pos1_number or average_number == pos2_number:
        average_position += CHARACTERS[LENGTH // 2]

    return average_position
