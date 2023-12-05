import re
from os.path import join


folder_name = 'day_2'
digit_pattern = re.compile('\d+')
color_pattern = re.compile('(?=(red|green|blue))')
number_color_pattern = re.compile('(\d+\s(?=(red|blue|green)))')
max_values = {'red': 12, 'blue': 14, 'green': 13}


class CachedProperty():
    def __init__(self, func, name=None):
        self.func = func
        self.name = name if name is not None else func.__name__
        self.__doc__ = func.__doc__

    def __get__(self, instance, class_):
        if instance is None:
            return self
        res = self.func(instance)
        setattr(instance, self.name, res)
        return res


class CubeSet():
    def __init__(self, red: int = 0, blue: int = 0, green: int = 0):
        self.__red = red
        self.__blue = blue
        self.__green = green
    
    def __repr__(self):
        return f'Cube Set(red: {self.red}, green: {self.green}, blue: {self.blue})'

    @classmethod
    def parse_cubeset(cls, string):
        matches = number_color_pattern.findall(string)
        dic = {c: int(n) for n, c in matches}
        return cls(**dic)

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

    @CachedProperty
    def power(self) -> int:
        return self.red * self.blue * self.green

    @CachedProperty
    def possible(self) -> bool:
        if self.red > max_values['red']:
            return False
        if self.green > max_values['green']:
            return False
        if self.blue > max_values['blue']:
            return False
        return True

    

class Game():
    def __init__(self, game_number : int = 0, extractions: list[CubeSet] = []):
        self.__game_number = game_number
        self.__extractions = extractions
    
    @classmethod
    def parse_game(cls, game_string: str):
        game_number, extractions = game_string.split(':')
        game_number = int(digit_pattern.findall(game_number)[0])
        extractions = [CubeSet.parse_cubeset(e) for e in extractions.split(';')]
        return cls(game_number=game_number, extractions=extractions)
    
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
    
    @CachedProperty
    def minimal_cube_set(self) -> CubeSet:
        minimal = CubeSet()
        for e in self.__extractions:
            if e.red > minimal.red:
                minimal.red = e.red
            if e.green > minimal.green:
                minimal.green = e.green
            if e.blue > minimal.blue:
                minimal.blue = e.blue
        return minimal

    @CachedProperty
    def minimal_power(self) -> int:
        minimal = self.minimal_cube_set
        return minimal.power

    @CachedProperty
    def possible(self):
        for e in self.__extractions:
            if not e.possible:
                return False
        return True



def parse_file(file_name: str, verbose:str=False):
    games = []
    with open(join(folder_name, file_name)) as f:
        for line in f:
            line = line.strip('\n')
            g = Game.parse_game(line)
            games.append(g)
            if verbose:
                print(f'{g}\nMinimal {g.minimal_cube_set} -> Power: {g.minimal_power}\n')
    return games


def find_possible_games(games: list[Game], verbose=False):
    possible_games = []
    for g in games:
        possible = g.possible
        if possible:
            possible_games.append(g.game_number)
        if verbose:
            print("Game {} is {}".format(g.game_number, 'possible' if possible else 'not possible'))
    return possible_games


if __name__ == '__main__':
    games = parse_file('input_1.txt', verbose=False)
    possible_games = find_possible_games(games, verbose=False)
    print("Part 1: {}".format(sum(possible_games)))
    print("Part 2: {}".format(sum([g.minimal_power for g in games])))
