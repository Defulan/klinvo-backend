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
    def get_char_number(cls, char: str) -> int:
        return cls.CHARACTERS.index(char) + 1
    

    @classmethod
    def get_char_by_charnumber(cls, charnumber: int) -> str:
        return cls.CHARACTERS[charnumber - 1]
    

    @classmethod
    def get_next_char(cls, char: str) -> str:
        if char[-1] == cls.CHARACTERS[-1]:
            raise ValueError("Argument is final character")
        
        next_index = cls.CHARACTERS.index(char) + 1
        return cls.CHARACTERS[next_index]
    

    def to_number(self) -> int:
        result: int = 0

        for index, char in enumerate(reversed(self.value)):
            result += self.get_char_number(char) * (self.LENGTH ** index)
        
        return result
    

    @classmethod
    def number_to_position(cls, number_value: int) -> str:
        results: list[str] = []

        while number_value > 0:
            charnumber: int = number_value % cls.LENGTH
            char = cls.get_char_by_charnumber(charnumber)

            results.append(char)
            number_value //= cls.LENGTH
        
        result: str = "".join(reversed(results))
        return result
    

    def get_next_position(self) -> str:
        next_number = self.to_number() + 1
        next_position: str = self.get_char_by_charnumber(next_number)
        return next_position
    

    @classmethod
    def get_none_position(cls) -> str:
        return cls.CHARACTERS[0]
