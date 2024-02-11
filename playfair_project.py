class Playfair:
    def __init__(self):
        pass
    
    def create_playfair_grid(self, keyword):
        alphabet = "abcdfeghiklmnopqrstuvwxyz"
        playfair_grid = []
        keyword = self.removeKeywordDupes(keyword.lower().replace('j','').replace(' ',''))
        keyword = self.removeKeywordDupes(keyword+alphabet)
        for i in range(0, len(alphabet), 5):
            playfair_grid.append(keyword[i:i+5])
        return playfair_grid

    def removeKeywordDupes(keyword):
        newKey = ''
        for c in keyword:
            if c not in newKey:
                newKey += c
        return newKey

    def print_playfair_grid(playfair_grid):
        for row in playfair_grid:
            print(row)

    def decode_playfair_digrams(ciphertext):
        plaintext = []
        for index in range(len(ciphertext)-1, -1, -1):
            if index == 0 or index == len(ciphertext) - 1:
                plaintext.append(ciphertext[index])
                continue
            if ciphertext[index] != ciphertext[index-1] and ciphertext[index] != ciphertext[index+1]:
                plaintext.append(ciphertext[index])
        return ''.join(reversed(plaintext))

    def encode_playfair_digrams(plaintext):
        digrams = list(plaintext.lower().replace(' ', ''))
        
        for i, digram in enumerate(digrams):
            if i % 2 == 1:
                if digram == digrams[i-1]:
                    digrams.insert(i,'q')

        if len(digrams) % 2 == 1: # if last digram does not have pair
            digrams.append('q')
        
        return ''.join(digrams)
    
    def get_indecies_of_letter(grid, letter):
        '''Returns a tuple of indecies (row, col) of an inputted letter in a given grid. Returns None otherwise'''
        for row in range(len(grid)):
            if letter in grid[row]:
                return (row, grid[row].index(letter))
        return None

    def get_rectangle_shift(pos1, pos2, encrypt):
        # ANDREW
        '''
        When two letters are not in the same column or row, this function switches them along a rectangle, where 
        pos1 and pos2 are two letters' indecies as (row, col) tuples. encrypt is bool determining sign (encrypt/decrypt)
        '''
        new_letter1_col = -1
        new_letter2_col = -1
        letter1_row = pos1[0]
        letter1_col = pos1[1]
        letter2_row = pos2[0]
        letter2_col = pos2[1]

        col_difference = abs(letter1_col - letter2_col)
        
        if letter1_row > letter2_row:
            if encrypt:
                new_letter1_col = letter1_col + col_difference
                new_letter2_col = letter2_col - col_difference
            else:
                new_letter1_col = letter1_col - col_difference
                new_letter2_col = letter2_col + col_difference
        else:
            if encrypt:
                new_letter1_col = letter1_col - col_difference
                new_letter2_col = letter2_col + col_difference
            else:
                new_letter1_col = letter1_col + col_difference
                new_letter2_col = letter2_col - col_difference
        return
    
    def get_column_shift(pos1, pos2, encrypt):
        # TIMMY
        # encrypt is a bool - determines sign of addition
        return
    
    def get_row_shift(pos1, pos2, encrypt):
        # TIMMY
        return
    
    def crypt(text, key, encrypt=True):
        #TODO
        return

if __name__ == '__main__':
    pass
