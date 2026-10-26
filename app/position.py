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
    
    Needs to generate a position than should be at the end
    
    If last character between C and z, function will just move back by one character
    
    If last character is B:
    if all previous is A - function will move B to A and add z to the end of position string
    if any of previous characters is not A:
        if it is between C and z: function will move that not-A character by one further and throw away everything after it
        if it is B - function will move B to A and add z to the end of position string"""
    
    if position[-1] not in (CHARACTERS[0], CHARACTERS[1]):
        return position[:-1] + get_previous_char(position[-1])
    
    for index, char in enumerate(position):
        if char == CHARACTERS[0]:
            continue

        if char == CHARACTERS[1]:
            slice_position = position[:index]
            return slice_position + CHARACTERS[0] + CHARACTERS[-1]
        
        slice_position = position[:index]
        return slice_position + get_previous_char(char)
    
    raise ValueError("Position with only A characters is impossible")


def generate_new_top_position(position: str) -> str:
    """Generate new first position based on current first position
    
    Needs to generate a position than should be at the beginning
    
    If last character between A and y, function will just move next by one character.
    
    If last character is z:
    if all previous characters is z, function will add A to the end of position string
    if one of characters on the way is not z - function will move that not-z character by one and throw away everything after it"""

    for index, char in enumerate(reversed(position)):
        if char != CHARACTERS[-1]:
            slice_position = position[:-1]
            if index != 0:
                slice_position = slice_position[:-index]
            next_position = slice_position + get_next_char(char)
            return next_position
    
    return position + CHARACTERS[0]


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
