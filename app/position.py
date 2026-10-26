CHARACTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
LENGTH = len(CHARACTERS)


def position_to_number(position: str) -> int:
    """Convert position to number as if position was 52-based number
    
    Number (int) form of position needs only for easier calculations in other functions"""

    result: int = 0

    for index, char in enumerate(reversed(position)):
        result += get_charnumber(char) * (LENGTH ** index)
    
    return result


def generate_new_bottom_position(position: str) -> str:
    """Generate new last position based on current last position
    
    Needs to generate a position than should be at the end"""
    
    if position[-1] == CHARACTERS[1]:
        prev_position = position[:-1] + CHARACTERS[0] + CHARACTERS[-1]
        return prev_position
    
    prev_number = position_to_number(position) - 1
    prev_position: str = number_to_position(prev_number)
    return prev_position


def generate_new_top_position(position: str) -> str:
    """Generate new first position based on current first position
    
    Needs to generate a position than should be at the beginning"""

    if position[-1] == CHARACTERS[-1]:
        next_position = position + CHARACTERS[0]
        return next_position
    
    next_number = position_to_number(position) + 1
    next_position: str = number_to_position(next_number)
    return next_position


def get_none_position() -> str:
    """Get a default position value for empty list
    
    Needs to generate a position for element that is the only element in it's list"""

    return CHARACTERS[0]


def get_charnumber(char: str) -> int:
    """Get charnumber of char in CHARACTERS (from all possible characters in position string)
    
    Needs only for easier calculations in other functions"""

    return CHARACTERS.index(char) + 1


def get_char_by_charnumber(charnumber: int) -> str:
    """Get char by it's charnumber (reverse function of get_charnumber)"""

    return CHARACTERS[charnumber - 1]


def get_next_char(char: str) -> str:
    """Get next char in list of all possible characters for position string"""

    if char == CHARACTERS[-1]:
        raise ValueError("Argument is final character")
    
    next_index = CHARACTERS.index(char) + 1
    return CHARACTERS[next_index]


def get_previous_char(char: str) -> str:
    """Get previous char in list of all possible characters for position string"""

    if char == CHARACTERS[0]:
        raise ValueError("Argument is first character")
    
    next_index = CHARACTERS.index(char) - 1
    return CHARACTERS[next_index]


def number_to_position(number_value: int) -> str:
    """Get position string from number (reverse function of position_to_number)"""

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
    """Get average position between two entered positions"""

    if pos1 == pos2:
        raise ValueError("Both positions are equal")
    
    pos1_number = position_to_number(pos1)
    pos2_number = position_to_number(pos2)

    average_number = (pos1_number + pos2_number) // 2
    average_position = number_to_position(average_number)
    
    if average_number == pos1_number or average_number == pos2_number:
        average_position += CHARACTERS[LENGTH // 2]

    return average_position
