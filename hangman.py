# Problem Set 2, hangman.py
# Name: Sarthak Agrawal
# Collaborators: -
# Time spent: 5 hours

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''

    #Method 1 (Does not work)
    """
    secret=set(secret_word)
    freq={}
    
    for i in secret:
        freq[i]=1
    
    for i in letters_guessed:
        if i in freq:
            del[i]

    if len(freq)==0:
        return True
    return False
    """
    #Method 2
    freq=Counter(secret_word)
    a=0 # a counter
    for i in letters_guessed:
        if i in freq:
            a+=freq[i]
    
    return a==len(secret_word)




def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''

    ch="_ " #for when a character is not present
    my_str=""

    for i in secret_word:
        if i in letters_guessed:
            my_str+=i
        else:
            my_str+=ch
    return my_str



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    all=string.ascii_lowercase

    my_str=''

    for i in all:
        if i not in letters_guessed:
            my_str+=i
    return my_str
    
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''

    guesses_remaining=6
    warnings_remaining=3
    vowels=('a', 'e', 'i', 'o', 'u')
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is", len(secret_word), "letters long.")
    print("You have 3 warnings left.")
    print("-------------")
    letters_guessed=''
    flag=True #flag for correct guess

    while guesses_remaining>0 and flag:
        print("You have", guesses_remaining, "guesses left.")
        print("Available letters:", get_available_letters(letters_guessed))
        ch=str(input("Please guess a letter: "))

        if ch not in string.ascii_letters:
            if warnings_remaining==0:
                guesses_remaining-=1
                print("Oops! That is not a valid letter. You have no warnings left so you lose one guess:", end = ' ')
            else:
                warnings_remaining-=1
                print("Oops! That is not a valid letter. You have", warnings_remaining, "warnings left:", end = ' ')
        else:
            print("")
            ch=ch.lower()
            if ch in letters_guessed:
                if warnings_remaining==0:
                    guesses_remaining-=1
                    print("Oops! You've already guessed that letter. You have no warnings left so you lose one guess:", end =' ')
                else:
                    warnings_remaining-=1
                    print("Oops! You've already guessed that letter. You have", warnings_remaining, "warnings left:", end = ' ')
            else:
                letters_guessed+=ch
                if ch in secret_word:
                    print("Good guess:", end = ' ')
                else:
                    if ch in vowels:
                        guesses_remaining-=2
                    else:
                        guesses_remaining-=1
                    print("Oops! That letter is not in my word:", end = '  ')
        
        print( get_guessed_word(secret_word, letters_guessed) )
        print("-------------")

        if is_word_guessed(secret_word, letters_guessed):
            flag=False
            print("Congratulations, you won!\nYour total score for this game is:", int(guesses_remaining*len(set(secret_word))))

    if flag:
        print("Sorry, you ran out of guesses. The word was", secret_word)        



# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''

    #other_word.strip(' ') #not required as input was also stripped
    my_word=my_word.replace(' ', '') #takes care of strip and of '_ ' being of length 2

    if len(my_word)!=len(other_word):
        return False
    
    # Method 1 not used since not as pythonic
    """
    for i in range(len(my_word)):
        if my_word[i].isalpha():
            if my_word[i]!=other_word[i]:
                return False
    """
    
    # Method 2
    for i, j in zip(my_word, other_word):
        if i.isalpha() and i!=j:
            return False

    return True



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    a=True

    for i in wordlist:
        i=i.strip(' ')
        if match_with_gaps(my_word, i):
            if a:
                a=False
            print(i, end=' ')
    if a:
        print("No matches found", end='')
    print()



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''

    guesses_remaining=6
    warnings_remaining=3
    vowels=('a', 'e', 'i', 'o', 'u')
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is", len(secret_word), "letters long.")
    print("You have 3 warnings left.")
    print("-------------")
    letters_guessed=''
    flag=True #flag for correct guess

    while guesses_remaining>0 and flag:
        print("You have", guesses_remaining, "guesses left.")
        print("Available letters:", get_available_letters(letters_guessed))
        ch=str(input("Please guess a letter: "))

        if ch=='*':
            print("Possible word matches are:")
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
        elif ch not in string.ascii_letters:
            if warnings_remaining==0:
                guesses_remaining-=1
                print("Oops! That is not a valid letter. You have no warnings left so you lose one guess:", end = ' ')
            else:
                warnings_remaining-=1
                print("Oops! That is not a valid letter. You have", warnings_remaining, "warnings left:", end = ' ')
        
        else:
            print("")
            ch=ch.lower()
            if ch in letters_guessed:
                if warnings_remaining==0:
                    guesses_remaining-=1
                    print("Oops! You've already guessed that letter. You have no warnings left so you lose one guess:", end =' ')
                else:
                    warnings_remaining-=1
                    print("Oops! You've already guessed that letter. You have", warnings_remaining, "warnings left:", end = ' ')
            else:
                letters_guessed+=ch
                if ch in secret_word:
                    print("Good guess:", end = ' ')
                else:
                    if ch in vowels:
                        guesses_remaining-=2
                    else:
                        guesses_remaining-=1
                    print("Oops! That letter is not in my word:", end = '  ')
        
        print( get_guessed_word(secret_word, letters_guessed) )
        print("-------------")

        if is_word_guessed(secret_word, letters_guessed):
            flag=False
            print("Congratulations, you won!\nYour total score for this game is:", int(guesses_remaining*len(set(secret_word))))

    if flag:
        print("Sorry, you ran out of guesses. The word was", secret_word)        

    
# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    
    #secret_word = choose_word(wordlist)
    #hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    #secret_word="else"

    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
    
