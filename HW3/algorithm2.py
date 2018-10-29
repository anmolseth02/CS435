import sys
import random
from random import randint
import string

ALPHABET = string.ascii_uppercase + string.ascii_lowercase


cmdargs = str(sys.argv)
output = open(sys.argv[3], 'w+')


# Read in the training data
file = open('rockyou-withcount.txt', )
data = []
for line in file:
    data.append(line[8:].rstrip())
data = data[:100]
#print(data)

# Read in the list of passwords
with open(sys.argv[2], 'r') as f:
    passwords = f.readlines()

# Number of honeywords to generate
n = int(sys.argv[1])

###### START OF HELPER FUNCTIONS #########

def generateRandSeq(n):
    seqlist = []
    start = randint(0, 9) % 5
    start
    seqlist.append(start)
    for i in range(n - 1):
        seqlist.append(start + 1)
        start += 1
    res = ""
    for ele in seqlist:
        res += str(ele)
    return res


# Shuffles digits in an input string
def shuffleDigits(input_str):
    digits = [int(x) for x in input_str]
    random.shuffle(digits)
    res = ""
    for ele in digits:
        res += str(ele)
    return res


# removes duplicates
def remove_duplicates(in_list, password):
    final_list = []
    for num in in_list:
        if num not in final_list and num != password and num != '':
            final_list.append(num)
    return final_list


# generates sweet "count" number of sweet words of "length" for a "password"
def generateSweetWords(count, length, password_type, password):
    sweetwords = []
    # generate count*10 sweet words (later sample out count number of sweet words as honeywords)
    while (len(sweetwords) < count * 10):
        # if password is a list of consecutive integers
        if (password_type == "digitSequence"):
            if (random.random() > 0.3):
                # for some cases generate random sequences of integers
                sweetwords.append(generateRandSeq(length))
            else:
                # for other cases generate random strings of numbers
                sweetwords.append(''.join([random.choice(string.digits) for n in range(length)]))
        # if password is a list of integers
        elif (password_type == "digits"):
            if (random.random() > 0.5):
                # half the time shullfe the digits
                sweetwords.append(shuffleDigits(password))
            else:
                # other cases generate random strings of integers
                sweetwords.append(''.join([random.choice(string.digits) for n in range(length)]))
        # if the password is a combination of chars, digits and special caras
        else:
            # divide the password into 3 lists - characters, digits and special
            characters = []
            digits = []
            special = []
            # poulate the lists
            for i in password.strip():
                if i in ALPHABET:
                    characters.append(i)
                elif i.isdigit():
                    digits.append(i)
                else:
                    special.append(i)

            # flip first letter case
            if characters and random.random() < 0.5:
                characters = [char.lower() for char in characters]
                characters[0] = characters[0].upper()

            # lowercase password
            if characters and random.random() < 0.2:
                charBlock = [char.lower() for char in characters]

                # remove "digits_to_remove" last digits
            digits_to_remove = randint(0, 2)
            if digits and random.random() < 0.3:
                digits = digits[:-digits_to_remove]

            # remove digits
            if digits and random.random() < 0.4:
                digits = ['']
            # add random digits
            elif not digits and random.random() < 0.10:
                digits = [random.choice(string.digits) for n in range(randint(0, 5))]
            # print("special before",special)
            if (special):
                special = random.sample(special, len(special))
            # print("special after",special)
            # shuffle characters, digits and special arrangement
            stringBlocks = [characters, digits, special]
            # print(characters, digits, special)
            if random.random() < 0.2:
                random.shuffle(stringBlocks)
            sweetwords.append(''.join(stringBlocks[0] + stringBlocks[1] + stringBlocks[2]))

        sweetwords = remove_duplicates(sweetwords, password)

    sweetwords = random.sample(sweetwords, count)
    return sweetwords


###### END OF HELPER FUNCTIONS #########

def honeywords_creation(n, password):

    honey_words = []
    honey_words.append(password)
    length= len(password)

    # If Password is in the data, return n random passwords from the data
    if password in data:
        while len(honey_words) != n:
            other_password = data[random.randint(0, len(data) - 1)]
            while other_password in honey_words:
                other_password = data[random.randint(0, len(data) - 1)]
            honey_words.append(other_password)
        return honey_words

    # Add n/4 words from the data with the same length as the password
    same_length_data = [d for d in data if len(d) == length]
    if len(same_length_data) >= n // 2 and same_length_data:
        while len(honey_words) != n // 2:
            other_password = same_length_data[random.randint(0, len(same_length_data) - 1)]
            while other_password in honey_words:
                other_password = data[random.randint(0, len(data) - 1)]
            honey_words.append(other_password)
    else:
        honey_words= honey_words+same_length_data

    # Add random n/4 words from the data

    if len(data) >= 3*n // 4:
        while len(honey_words) != 3*n / 4:
            other_password = data[random.randint(0, len(data) - 1)]
            while other_password in honey_words:
                other_password = data[random.randint(0, len(data) - 1)]
            honey_words.append(other_password)
    else:
        honey_words= honey_words+data

    # type of password
    if (password.isdigit()):
        if (int(password[-1]) - int(password[0]) == len(password) - 1):
            password_type = "digitSequence"
        else:
            password_type = "digits"
    else:
        password_type = "other"

    basic = generateSweetWords(n - len(honey_words), len(password), password_type, password)
    honey_words= honey_words+ basic
    return honey_words


for password in passwords:
    password = str(password)
    password = password.strip()

    #creating honeywords for each password
    honeyword_list = honeywords_creation(n, password)

    # Shuffling and writing honeywords to the file
    random.shuffle(honeyword_list)
    output.write(','.join(map(str, honeyword_list)) +'\n' )
