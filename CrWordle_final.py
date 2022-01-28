# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 09:22:15 2022

@author: Lesept

Howto:
    First go to the Wordle website: https://www.powerlanguage.co.uk/wordle/
    Enter your first guess: I use 'above' but there are other suggestions
    (https://www.polygon.com/gaming/22884031/wordle-game-tips-best-first-guess-5-letter-words)
    Wordle answers with colored letters: enter this answer using the following code
        use - for grey (letter not in the word)
        use = for yellow (letter misplaced)
        use + for green (correct place)
    For example : -+==-
    I suggest a word : play it in Wordle
    Enter Wordle's answer until you find the correct word
"""

def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

# Compute the score of a word
def score(word, Wordle):
    score = "-----"

    for i in range(len(word)):
        if Wordle[i] == word[i]:
            Wordle = Wordle[:i]+'0'+Wordle[i+1:]
            score  = score[:i]+'+'+score[i+1:]

    for j in range(len(word)):
        if score[j]=='+': continue
        comp = [i for i in range(len(Wordle)) if Wordle.startswith(word[j], i)]
        if comp == []:
            score  = score[:j]+'-'+score[j+1:]
        else:
            score  = score[:j]+'='+score[j+1:]
    return score

# Search words matching a given score
def search(filename, target, guess, wordList):
    Nwords = len(wordList)
    count = 0
    lst = []
    for i in range(Nwords):
        test = wordList[i]
        if score(guess, test) == target:
            count += 1
            lst.append(test)
    return count, lst
# 
# Main code
# 

if __name__ == '__main__':
    filename = "Dict-5757.txt"
    found = False

# Create the initial list of words    
    wordList = []
    with open(filename) as file:
        Lines = file.readlines()
        for line in Lines:
            line = line[:-1]
            wordList.append(line)
        
    word = input ("Enter your initial guess: ")
# Main loop : search for words fitting the scores, and reduce the search scope
    while not found:
        s = input ("Enter your score: ")
        if s == '+++++':
            print('Congratulations !!!')
            found = True
        elif s == '-----':
            print("That wasn't a good guess. Try playing a word with several vowels such as: adieu, about, above...")
        else:
            count, lst = search(filename, s, word, wordList)
            if count == 0:
                import sys
                sys.exit('no matching word: please try again from the beginning')
            else:
                print(f'Found {count} matching words --> my suggestion: {lst[0]}')
                wordList = intersection(lst, wordList)
                word = lst[0]