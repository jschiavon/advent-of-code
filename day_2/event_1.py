import re
from os.path import join


folder_name = 'day_2'
digit_pattern = re.compile('\d+')
color_pattern = re.compile('(?=(red|green|blue))')
number_color_pattern = re.compile('(\d+\s(?=(red|blue|green)))')
max_values = {'red': 12, 'blue': 14, 'green': 13}


class Extraction():

    def __init__(self, red: int = 0, blue: int = 0, green: int = 0):
        self.__red = red
        self.__blue = blue
        self.__green = green
    
    def __repr__(self):
        return f'Extraction(red: {self.red}, green: {self.green}, blue: {self.blue})'

    @property
    def red(self):
        return self.__red
    
    @red.setter
    def red(self, value: int):
        if value >= 0:
            self.__red = value
        else:
            raise ValueError("Red balls should be >= 0")

    @property
    def green(self):
        return self.__green
    
    @green.setter
    def green(self, value: int):
        if value >= 0:
            self.__green = value
        else:
            raise ValueError("Green balls should be >= 0")
    
    @property
    def blue(self):
        return self.__blue
    
    @blue.setter
    def blue(self, value: int):
        if value >= 0:
            self.__blue = value
        else:
            raise ValueError("Blue balls should be >= 0")

    def get(self, color: str):
        if color == 'red':
            return self.red
        if color == 'green':
            return self.green
        if color == 'blue':
            return self.blue
        raise KeyError("`color` should be one of [red, green, blue]")

    @property
    def possible(self):
        if self.red > max_values['red']:
            return False
        if self.green > max_values['green']:
            return False
        if self.blue > max_values['blue']:
            return False
        return True

    @classmethod
    def parse_cubeset(cls, string):
        matches = number_color_pattern.findall(string)
        dic = {c: int(n) for n, c in matches}
        return cls(**dic)


class Game():
    def __init__(self, game_number : int = 0, extractions: list[Extraction] = []):
        self.__game_number = game_number
        self.__extractions = extractions
    
    def __repr__(self):
        extractions = '\n'.join([f' -> {repr(e)}' for e in self.__extractions])
        return f'Game {self.__game_number}:\n' + extractions
        
    @property
    def game_number(self):
        return self.__game_number
    
    @game_number.setter
    def game_number(self, value):
        if value >= 0:
            self.__game_number = value
        else:
            raise ValueError("game number should be >= 0")
    
    @classmethod
    def extract_game(cls, game_string: str):
        game_number, extractions = game_string.split(':')
        game_number = int(digit_pattern.findall(game_number)[0])
        extractions = [Extraction.parse_cubeset(e) for e in extractions.split(';')]
        return cls(game_number=game_number, extractions=extractions)
    
    def check_game(self):
        for e in self.__extractions:
            if not e.possible:
                return False
        return True


def parse_file(file_name: str, verbose:str=False) -> list[Game]:
    games = []
    with open(join(folder_name, file_name)) as f:
        for line in f:
            line = line.strip('\n')
            g = Game.extract_game(line)
            games.append(g)
            if verbose:
                print(g)
    return games


def find_possible_games(games: list[Game], verbose=False) -> list[int]:
    possible_games = []
    for g in games:
        possible = g.check_game()
        if possible:
            possible_games.append(g.game_number)
        if verbose:
            print("Game {} is {}".format(g.game_number, 'possible' if possible else 'not possible'))
    return possible_games



if __name__ == '__main__':
    games = parse_file('input_1_example.txt', verbose=True)
    possible_games = find_possible_games(games, verbose=True)
    print(sum(possible_games))
