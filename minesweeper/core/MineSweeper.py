from random import randint

class MineSweeper:

    def __init__(self, width=8, height=8, percent_of_tiles_as_bombs=0.16 ):
        if width <= 0:
            raise ValueError('Width must be grater then 0')

        if height <= 0:
            raise ValueError('Height must be grater then 0')
        
        if percent_of_tiles_as_bombs <= 0 or percent_of_tiles_as_bombs >= 1:
            raise ValueError('Percent of bombs must be grater then 0 and less then 1')

        self.percent_of_tiles_as_bombs = percent_of_tiles_as_bombs

        self.__tiles = width * height
        self.__bombs_quantity = int(self.__tiles * percent_of_tiles_as_bombs)
        self.__tiles_countdown = self.__tiles - self.__bombs_quantity

        self.__width = width
        self.__height = height

        self.__bombs_positions = set()

        self.__dead = False
        self.__flags = set()

        self.__board = []
        self.__build_board()

    def __build_board(self):
        self.__board = [[None for j in range(0, self.__width)] for i in range(0, self.__height)]
        
        while len(self.__bombs_positions) < self.__bombs_quantity:
            self.__bombs_positions.add((randint(0, self.__height - 1), randint(0, self.__width - 1)))

    def get_dimensions(self):
        return (self.__width, self.__height)

    def get_bombs_quantity(self):
        return self.__bombs_quantity

    def get_bombs(self):
        if self.is_over():
            return list(self.__bombs_positions)
        
        return []

    def get_flags(self):
        return list(self.__flags)
    
    def is_dead(self):
        return self.__dead
    
    def is_over(self):
        return self.is_dead() or self.__tiles_countdown is self.get_bombs_quantity()

    def step(self, x, y):
        if self.is_dead():
            raise Exception('The game is over: the player is dead')

        if self.is_over():
            raise Exception('The game is over: found all bombs')

        point = (y,x)
        
        if point in self.__bombs_positions and point not in self.__flags:
            self.__dead = True

        self.__reveal(x, y)
        
    def flag(self, x, y):
        if self.__board[y][x] is None:
            if (y, x) in self.__flags:
                self.__flags.discard((y, x))
            else:
                self.__flags.add((y, x))
        

    def __neighborhood(self, x, y):
        neighbors = set()
        x0 = x - 1
        y0 = y - 1

        for i in range(3):
            yy = i + y0
            if yy >= 0 and yy < self.__height:
                for j in range(3):
                    xx = j + x0

                    if xx >= 0 and xx < self.__width:
                        if xx is not x or yy is not y:
                            neighbors.add((yy, xx))
            
        return neighbors
                
    def __reveal(self, x, y):
        cell = self.__board[y][x]

        if cell is None:
            neighbors = self.__neighborhood(x, y)
            bombs = 0

            for neighbor in neighbors:
                if neighbor in self.__bombs_positions:
                    bombs += 1

            self.__tiles_countdown -= 1
            self.__board[y][x] = bombs

            if bombs == 0:
                for neighbor in neighbors:
                    self.__reveal(neighbor[1], neighbor[0])

    def __str__(self):
        padding = 5
        result = ""
        header = " ".join(["" for i in range(padding + 1)])
        header += "".join([("{x:^" + str(padding) + "}").format(x=x) for x in range(self.__width)])

        header.format(set(range(self.__width)))

        for y in range(self.__height):
            line = ("{y:^" + str(padding) + "}").format(y=str(y))

            for x in range(self.__width):
                character = 'x'

                if (y,x) in self.__flags:
                        character = "f"
                elif isinstance(self.__board[y][x], int):
                    character = str(self.__board[y][x])
                
                if self.is_over():
                    if (y,x) in self.__bombs_positions:
                        if character == "f":
                            character = "c"
                        else:
                            character = "b"
                
                line += ("{c:^" + str(padding) + "}").format(c=character)

            result += "\n" + line
        
        return header + "\n" + result
        