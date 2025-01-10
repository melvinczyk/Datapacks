def encrypt(input):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    encriptAlphabet = 'acegikmoqsuvywbdfghjlnprtxz'
    encryption = ''
    for letter in input:
        if letter != ' ':
            if letter == letter.lower():
                alphabetIndex = alphabet.index(letter)
                encryption += encriptAlphabet[alphabetIndex]
            else:
                alphabetIndex = alphabet.index(letter.lower())
                encryption += encriptAlphabet[alphabetIndex].upper()
        else:
            encryption += ' '
    return encryption
    
def decrypt(encrypted):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    substituteAlphabet = 'acegikmoqsuvywbdfghjlnprtxz'
    decryption = ''
    for letter in encrypted:
        if letter != ' ':
            if letter == letter.lower():
                substituteIndex = substituteAlphabet.index(letter)
                decryption += alphabet[substituteIndex]
            else:
                substituteIndex = substituteAlphabet.index(letter.lower())
                decryption += alphabet[substituteIndex].upper()
        else:
            decryption += ' '
    return decryption
def main():
    message = input('Enter a message: ')
    encrypted = encrypt(message)
    print("Encrypted: " + encrypted)
    print("Decrypted: " + decrypt(encrypted))
main()
