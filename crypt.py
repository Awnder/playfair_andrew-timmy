#crypt program created by Andrew and Timmy

import argparse

class Substitution:
    def __init__(self, password):
        self.alphabet = "abcdefghijklmnopqrstuvwxyz "
        self.key = self.generateKeyFromPassword(password)

    def encrypt(self, plaintext):
        ''' Encrypts the message using a substitution cipher. '''
        ciphertext = ""
        for ch in plaintext:
            idx = self.alphabet.find(ch)
            ciphertext += self.key[idx]
        return ciphertext
    
    def decrypt(self, ciphertext):
        ''' Decrypts the message using a substitution cipher. '''
        plaintext = ""
        for ch in ciphertext:
            idx = self.key.find(ch)
            plaintext += self.alphabet[idx]
        return plaintext
    
    def removeChar(self, string, idx):
        return string[:idx] + string[idx+1:]

    def removePasswordDupes(self, password):
        newPassword = ''
        for ch in password:
            if ch not in newPassword:
                newPassword = newPassword + ch
        return newPassword
    
    def removeAlphabetDupes(self, alphabet, password):
        newAlphabet = ''
        for ch in alphabet:
            if ch not in password:
                newAlphabet = newAlphabet + ch
        return newAlphabet
    
    def generateKeyFromPassword(self, password):
        password = password.lower()
        password = self.removePasswordDupes(password)
        splitChr = password[-1]
        splitIdx = self.alphabet.find(splitChr)
        afterStr = self.removeAlphabetDupes(self.alphabet[splitIdx+1:], password)
        beforeStr = self.removeAlphabetDupes(self.alphabet[:splitIdx], password)
        return password + afterStr + beforeStr 

class RailFence:
    #TODO - add number of rails as key - will make key required for railfence (?)
    def __init__(self) -> None:    
        self.even = []
        self.odd = []

    def encrypt(self, plaintext):
        ''' Encrypt text using the rail fence cipher. '''

        for i in range(len(plaintext)):
            if i % 2 == 0:
                self.even.append(plaintext[i])
            else:
                self.odd.append(plaintext[i])
        
        ciphertext = "".join(self.even) + "".join(self.odd)

        return ciphertext

class Playfair:
    '''
    Algorithm that uses encryption/decryption playfair method. The grid is 5 lists of lists containing a 5 character string and
    encrypt is a bool used to determine encryption or decryption
    '''
    def __init__(self, keyword, encrypt):
        self.grid = self.create_playfair_grid(keyword)
        self.encrypt = encrypt
    
    def create_playfair_grid(self, keyword):
        '''
        Creates the grid by removing j, repeating characters in keyword, and adding the rest of the alphabet to a
        5x5 list of list of characters [ [a,b,c,d,e],[f,g,h,i,k] . . . ]
        '''
        alphabet = "abcdfeghiklmnopqrstuvwxyz"
        playfair_grid = []
        keyword = self.removeKeywordDupes(keyword.lower().replace('j','i').replace(' ',''))
        keyword = self.removeKeywordDupes(keyword+alphabet)
        for i in range(0, len(alphabet), 5):
            playfair_grid.append([keyword[i:i+5]])
        return playfair_grid

    def removeKeywordDupes(self, keyword):
        '''Removes duplicate characters in a keyword'''
        newKey = ''
        for c in keyword:
            if c not in newKey:
                newKey += c
        return newKey

    def print_playfair_grid(self):
        '''Prints rows in playfair grid'''
        for row in self.grid:
            print(row)

    def decode_playfair_digrams(self, ciphertext):
        '''Breaks ciphertext into a plaintext string, removing q's, returns a string'''
        plaintext = []
        for index in range(len(ciphertext)-1, -1, -1):
            if index == 0 or index == len(ciphertext) - 1:
                plaintext.append(ciphertext[index])
                continue
            if ciphertext[index] == 'q' and ciphertext[index-1] == ciphertext[index+1]:
                continue
            plaintext.append(ciphertext[index])
        
        # removes last q of string if exists (index 0 b/c reversed)
        if plaintext[0] == 'q':
            plaintext.pop(0)

        return ''.join(reversed(plaintext))

    def encode_playfair_digrams(self, plaintext):
        '''
        Breaks plaintext into a string of digrams, adding q's when letter repeats or at end if odd number of characters, 
        returns a string
        '''
        digrams = list(plaintext.replace(' ', ''))
        for i, digram in enumerate(digrams):
            if i % 2 == 1:
                if digram == digrams[i-1]:
                    digrams.insert(i,'q')

        if len(digrams) % 2 == 1: # if last digram does not have pair
            digrams.append('q')

        return ''.join(digrams)
    
    def get_letter(self, row, col):
        ''''''
        return self.grid[row][0][col] # because the grid is a list of lists of a string, [0] needs to be present to access string
    
    def get_pos(self, letter):
        '''Returns a tuple of indecies (row, col) of an inputted letter in a given grid. Returns None otherwise'''
        for row_index, row in enumerate(self.grid):
            for col_index, col in enumerate(row):
                if letter in row[col_index]:
                    return (row_index,row[col_index].index(letter))
        return None

    def get_rectangle_shift(self, pos1, pos2):
        '''
        When two letters are not in same column or row, switch them along a rectangle, where pos1 and pos2 are two 
        letters' indecies as (row, col) tuples. Bool encrypt isn't needed as function will flip letter location 
        the same way regardless of encrypting or decrypting
        '''
        new_letter1_col = -1
        new_letter2_col = -1
        letter1_row = pos1[0]
        letter1_col = pos1[1]
        letter2_row = pos2[0]
        letter2_col = pos2[1]

        col_difference = abs(letter1_col - letter2_col)

        if letter1_col < letter2_col:
            new_letter1_col = letter1_col + col_difference
            new_letter2_col = letter2_col - col_difference
        else:
            new_letter1_col = letter1_col - col_difference
            new_letter2_col = letter2_col + col_difference
            
        return [(letter1_row, new_letter1_col), (letter2_row, new_letter2_col)]
    
    def get_column_shift(self, pos1, pos2, encrypt):
        '''
        When two letters are in the same col, pos1 and pos2 are the letters' indecies as (row, col) tuples and bool
        encrypt changes the direction of shift +1 (down) or -1 (up)
        '''
        shift = 1 if encrypt else -1
        newpos1 = (pos1[0], (pos1[1] + shift) % 5)
        newpos2 = (pos2[0], (pos2[1] + shift) % 5)
        
        return [newpos1, newpos2]
    
    def get_row_shift(self, pos1, pos2, encrypt):
        '''
        When two letters are in the same row, pos1 and pos2 are the letters' indecies as (row, col) tuples and bool
        encrypt changes the direction of shift +1 (right) or -1 (left)
        '''
        shift = 1 if encrypt else -1
        newpos1 = ((pos1[0] + shift) % 5, pos1[1])
        newpos2 = ((pos2[0] + shift) % 5, pos2[1])
        
        return [newpos1, newpos2]
    
    def crypt(self, text):
        crypted_digrams = []

        # Turn text into digrams
        input_digrams = self.encode_playfair_digrams(text)

        # Crypt digrams with the key, producing a list of index tuples for each digram like this: [(1,3), (2,2)]
        index = 1
        while index < len(input_digrams):
            posits = [self.get_pos(input_digrams[index-1]),self.get_pos(input_digrams[index])]
            if posits[0][0] == posits[1][0]:
                crypted_digrams.append(self.get_column_shift(posits[0], posits[1], self.encrypt))
            elif posits[0][1] == posits[1][1]:
                crypted_digrams.append(self.get_row_shift(posits[0], posits[1], self.encrypt))
            else:
                crypted_digrams.append(self.get_rectangle_shift(posits[0], posits[1]))
            index += 2

        # Takes the list of indecies and produces a digram string 
        new_text = ''
        for digram in crypted_digrams:
            new_text += self.get_letter(digram[0][0], digram[0][1])
            new_text += self.get_letter(digram[1][0], digram[1][1])

        # Decode the digram string
        crypted = self.decode_playfair_digrams(new_text)

        # Return the result
        return crypted

def main():
    parser = argparse.ArgumentParser(description='Translates between ciphertext and plaintext using chosen algorithms')
    parser.add_argument('-a', '--algorithm', choices=['railfence', 'substitution', 'playfair'], help='algorithm type', required=True)
    mode = parser.add_mutually_exclusive_group(required=False)
    mode.add_argument('-e', '--encrypt', action='store_true', help='message to encrypt')
    mode.add_argument('-d', '--decrypt', action='store_true', help='message to decrypt')
    parser.add_argument('-k', '--key', type=str, help='the key/password to use for playfair/substitution')
    parser.add_argument('-t', '--text', type=str, help='the text to encrypt or decrypt')
    args = parser.parse_args()
    
    if ((args.algorithm == 'substitution' or args.algorithm == 'playfair') and not (args.encrypt or args.decrypt)):
        print(f"Please provide a mode (encrypt/decrypt) for {args.algorithm}")
        return
    
    encrypted_message = "Encrypted Message: "
    decrypted_message = "Decrypted Message: "

    if args.algorithm == 'railfence':
        print(encrypted_message + RailFence().encrypt(args.text))
    elif args.encrypt:
        if args.algorithm == 'substitution':
            print(encrypted_message + Substitution(args.key).encrypt(args.text.lower()))
        elif args.algorithm == 'playfair':
            print(encrypted_message + Playfair(args.key, True).crypt(args.text.lower()))
    elif args.decrypt:
        if args.algorithm == 'substitution':
            print(decrypted_message + Substitution(args.key).decrypt(args.text.lower()))
        elif args.algorithm == 'playfair':
            print(decrypted_message + Playfair(args.key, False).crypt(args.text.lower()))
    else:
        print('Flag or message error')
    return

if __name__ == '__main__':
    main()
