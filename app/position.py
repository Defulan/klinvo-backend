class Position:
    CHARACTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    LENGTH = len(CHARACTERS)

    value: str
    
    def __init__(self, value: str):
        self.value = value

    def get_next_position_value(self) -> str:
        if self.value[-1] == self.CHARACTERS[-1]:
            return self.value + self.CHARACTERS[0]
        
        next_char_index = self.get_char_index(self.value[-1])
        return self.value[:-1] + self.CHARACTERS[next_char_index]
    

    def get_char_index(self, char: str) -> int:
        return self.CHARACTERS.index(char)


    def get_char_by_index(self, index: int) -> str:
        return self.CHARACTERS[index]
    
    
    @classmethod
    def number_to_position(cls, num: int) -> str:
        result = ""
        
        while num > 0:
            result += cls.CHARACTERS[num % cls.LENGTH]
            num //= cls.LENGTH
        
        return "".join(reversed(result))
    

    @classmethod
    def position_to_number(cls, pos: str) -> int:
        result = 0
        for index, char in enumerate(reversed(pos)):
            result += cls.get_char_index(cls, char) * (cls.LENGTH ** index)
        return result
    
    
    @classmethod
    def none_position_value(cls) -> str:
        return cls.CHARACTERS[0]
