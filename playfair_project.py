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

    def removeKeywordDupes(self, keyword):
        newKey = ''
        for c in keyword:
            if c not in newKey:
                newKey += c
        return newKey

    def print_playfair_grid(self, playfair_grid):
        for row in playfair_grid:
            print(row)

    def decode_playfair_digrams(self, ciphertext):
        plaintext = []
        for index in range(len(ciphertext)-1, -1, -1):
            if index == 0 or index == len(ciphertext) - 1:
                plaintext.append(ciphertext[index])
                continue
            if ciphertext[index] != ciphertext[index-1] and ciphertext[index] != ciphertext[index+1]:
                plaintext.append(ciphertext[index])
        return ''.join(reversed(plaintext))

    def encode_playfair_digrams(self, plaintext):
        digrams = list(plaintext.lower().replace(' ', ''))
        
        for i, digram in enumerate(digrams):
            if i % 2 == 1:
                if digram == digrams[i-1]:
                    digrams.insert(i,'q')

        if len(digrams) % 2 == 1: # if last digram does not have pair
            digrams.append('q')
        
        return ''.join(digrams)
    
    def get_rectangle_shift(pos1, pos2):
        return
    
    def get_column_shift(pos1, pos2, encrypt):
        # encrypt is a bool - determines sign of addition
        return
    
    def get_row_shift(pos1, pos2, encrypt):
        return
    
    def crypt(text, key, encrypt=True):
        #TODO
        return

    def test(self):
        pass

    def test2(self):
        pass

if __name__ == '__main__':
    pass