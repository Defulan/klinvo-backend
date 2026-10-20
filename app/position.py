class Position:
    CHARACTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    LENGTH = len(CHARACTERS)

    value: str
    
    def __init__(self, value: str):
        self.value = value

    def get_next_position(self):
        if self.value[-1] == self.CHARACTERS[-1]:
            return self.value + self.CHARACTERS[0]
        
        next_char_index = self.get_char_index(self.value[-1])
        return self.value[:-1] + self.CHARACTERS[next_char_index]
    

    def get_char_index(self, char: str) -> int:
        return self.CHARACTERS.index(char)
    

    def number_to_position(self, num: int) -> str:
        result = ""
        
        while num > 0:
            result += self.CHARACTERS[num % self.LENGTH]
            num //= self.LENGTH
        
        return "".join(reversed(result))
    

    def position_to_number(self, pos: str) -> int:
        result = 0
        for index, char in enumerate(reversed(pos)):
            result += self.get_char_index(char) * (self.LENGTH ** index)
        return result
