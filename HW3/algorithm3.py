import sys
import random
import jellyfish
import string

cmdargs = str(sys.argv)
output = open(sys.argv[3], 'w+')

# Read in the training data
file = open('rockyou-withcount.txt', encoding='ISO-8859-1')
data = []
for line in file:
    data.append(line[8:].rstrip())

# Read in the list of passwords
with open(sys.argv[2], 'r') as f:
    passwords = f.readlines()

# Number of honeywords to generate
n = int(sys.argv[1])

# For each password, generate a list of honeywords
for password in passwords:
    honey_words = []
    # First, get a random password from the list from which to generate
    # half the honey words. If the original password is all letters or all digits,
    # so is this password. Otherwise, this password is made up of multiple types of characters.
    if password.rstrip().isalpha():
        other_password = data[random.randint(0, len(data) - 1)]
        while not other_password.isalpha():
            other_password = data[random.randint(0, len(data) - 1)]
    elif password.rstrip().isdigit():
        other_password = data[random.randint(0, len(data) - 1)]
        while not other_password.isdigit():
            other_password = data[random.randint(0, len(data) - 1)]
    else:
        other_password = data[random.randint(0, len(data) - 1)]
        while other_password.isalpha() or other_password.isdigit():
            other_password = data[random.randint(0, len(data) - 1)]
    for original in [password.rstrip(), other_password]:
        # If the password is made up of letters, find more passwords made up of
        # only letters in the training data
        if original.isalpha():
            if original == password.rstrip():
                limit = n/4
            else:
                limit = 3*n/4
            while len(honey_words) <= limit:
                index = random.randint(0, len(data) - 1)
                if data[index].isalpha() and data[index] != password and data[index] != other_password and data[index] not in honey_words:
                    honey_words.append(data[index])
        # If the password is made up of digits, find more passwords made up of
        # only digits in the training data
        elif original.isdigit():
            if original == password.rstrip():
                limit = n/4
            else:
                limit = 3*n/4
            while len(honey_words) <= limit:
                index = random.randint(0, len(data) - 1)
                if data[index].isdigit() and data[index] != password and data[index] != other_password and data[index] not in honey_words:
                    honey_words.append(data[index])
        # If the password is made up of multiple types of characters, change the case of the first character
        # and change any digits to random digits
        else:
            if original == password.rstrip():
                limit = n/4
            else:
                limit = 3*n/4
            # If the original password has trailing digits, one of the honey words
            # is the password with these digits removed and, with probability 0.5,
            # the capitalization of the first character changed
            if original.rstrip(string.digits) != original:
                if random.randint(0, 1) == 0:
                    if original[0] in string.ascii_uppercase:
                        new_word = original[0].lower()
                    else:
                        new_word = original[0].upper()
                else:
                    new_word = original[0]
                new_word = new_word + original[1:].rstrip(string.digits)
                honey_words.append(new_word)
            while len(honey_words) <= limit:
                # Change case of first character for every other honey word
                if len(honey_words) % 2 == 0:
                    if original[0] in string.ascii_uppercase:
                        new_word = original[0].lower()
                    else:
                        new_word = original[0].upper()
                else:
                    new_word = original[0]
                # Randomize the digits
                for char in original[1:]:
                    if char.isdigit():
                        new_word = new_word + str((random.randint(0, 9)))
                    else:
                        new_word = new_word + char
                # Add digits at random to the end if the password hasn't changed
                if new_word == original:
                    for i in range(random.randint(1, 5)):
                        new_word = new_word + str((random.randint(0,9)))
                if new_word not in honey_words:
                    honey_words.append(new_word)
        # The remaining honeywords are the nearest neighbors of original in the training data
        nearest_words = []
        if original == password.rstrip():
            limit = int(n/2) - len(honey_words)
        else:
            limit = n - len(honey_words) - 1
        i = 0
        while len(nearest_words) < limit:
            if data[i] not in honey_words:
                nearest_words.append((jellyfish.levenshtein_distance(data[i], original), data[i]))
            i += 1
        nearest_words.sort()
        for word in data[limit:200000]:
            distance = jellyfish.levenshtein_distance(word, original)
            for near in nearest_words:
                if distance < near[0] and word not in honey_words and word != password.rstrip() and word != other_password:
                    nearest_words.pop()
                    nearest_words.append((distance, word))
                    break
            nearest_words.sort()
        for word in nearest_words:
            honey_words.append(word[1])
    honey_words.append(other_password)
    # Randomize order of honeywords
    random.shuffle(honey_words)
    output.write(','.join(map(str, honey_words)) + '\n')

output.close()
