class Position:
    CHARACTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    LENGTH = len(CHARACTERS)

    value: str
    
    # TODO there was: get_next_position_value (-> str)
    # TODO there was: get_char_index (-> int), get_char_by_index (-> str)
    # TODO there was: number_to_position (-> str), position_to_number (-> int)
    # TODO there was: none_position_value (-> str)
    def __init__(self, value: str):
        self.value = value
    
    @classmethod
    def get_index(cls, char: str) -> int:
        return cls.CHARACTERS.index(char)

