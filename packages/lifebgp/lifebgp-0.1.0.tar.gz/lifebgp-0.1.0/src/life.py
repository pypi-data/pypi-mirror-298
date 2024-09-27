from bitarray import bitarray

class Life:
    """A python implementation of Game of Life
    
    part of BGP
    """
    def __init__(self, filename:str):
        """Create a game of life object
    
        Args:
            filename: Input file name.
    
        Raises:
            Exceptions: If input data is invalid.
        """
        self.filename = filename  
        self.extgrid = []
        with open(filename) as f:
            
            self.w,self.h = map(int, f.readline().split(' ', 1))
            
            for y in range(self.h + 2):
                self.extgrid.append(bitarray(self.w + 2)) # save memory, bitarray is also avaliable
                
            for no, line in enumerate(f):
                try:
                    y , x = map(int, line.split(' ', 1))
                    
                    if y < 0 or x < 0:
                        raise ValueError
    
                except ValueError:
                    raise Exception(f"Invaild cell on line {no+2}.")
     
                self.extgrid[y + 1][x + 1] = 1

        self.grid = [row[1:-1] for row in self.extgrid[1:-1]]

    
    def tick_grid(self,n:int=1):
        """Applies the rules of Game of Life for specified number of generations.
    
        Args:
        n: Number of generations      
        """
        for i in range(n):
            for y,row in enumerate(self.extgrid[1:-1]):
                y1,y2 = y+1,y+2   
                curr = bitarray (self.w+2)
                for x,cell in enumerate(row[1:-1]):
                    count = self.extgrid[y][x] + self.extgrid[y][x+1] + self.extgrid[y][x+2] + self.extgrid[y1][x] + self.extgrid[y1][x+2]  + self.extgrid[y2][x] + self.extgrid[y2][x+1] + self.extgrid[y2][x+2]
                    curr[x+1] = 1 if count == 3 or (cell and count ==2) else 0
        
                if y > 0:
                    self.extgrid [y] = prev
                prev = curr
            self.extgrid [y+1] = curr

        self.grid = [row[1:-1] for row in self.extgrid[1:-1]]

    def write_grid(self,filename:str="grid.txt"):
        """Write grid to a given text file

        Args:
        filename: Given output file name
        """
        with open(filename,"w") as file:
            for row in self.grid:
                file.write(" ".join(map(str, row)) + "\n")
