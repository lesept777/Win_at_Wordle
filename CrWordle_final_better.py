# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 09:22:15 2022

@author: Lesept

Dependency : textdistance (pip install textdistance)

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

import textdistance

def diversity(word):
    return len(set(word)) / 5

# Compute the score of a word
def score(word, Wordle):
    score = "-----"
    nomore = []

    for i in range(len(word)):
        if Wordle[i] == word[i]:
            Wordle = Wordle[:i]+'0'+Wordle[i+1:]
            score  = score[:i]+'+'+score[i+1:]

    for j in range(len(word)):
        if score[j]=='+': continue
        comp = [i for i in range(len(Wordle)) if Wordle.startswith(word[j], i)]
        if comp == []:
            res = '-'
        else:
            comp2 = []
            for i in range(len(comp)):
                if comp[i] not in nomore:
                    comp2.append(comp[i])
            if comp2 != []:
                res = '='
                nomore.append(comp2[0])
                score  = score[:j] + res + score[j+1:]
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

# Select in the list the farthest word from last guess
def select(guess, lst):
    if len(lst) == 1:
        return lst[0]
    maxdist = 0
    number = 0
    bestword = ''
    for word in lst:
        # dist = textdistance.bwtrle_ncd.distance(guess, word)
        dist = textdistance.entropy_ncd.distance(guess, word)
        # dist = textdistance.mra.distance(guess, word)
        # dist = textdistance.editex.distance(guess, word)
        dist *= diversity(word)
        if dist > maxdist:
            maxdist = dist
            bestword = word
            number = 0
        if dist == maxdist:
            number += 1
    return bestword
    
# 
# Main code
# 

if __name__ == '__main__':
    filename = "Dict-5757.txt"          # uncomment for english game
    # filename = "Dict-FR-7980.txt"     # uncomment for french game
    found = False

# Create the initial list of words    
    wordList = []
    with open(filename) as file:
        Lines = file.readlines()
        for line in Lines:
            line = line[:-1].lower().split()
            for i in range(len(line)):
                wordList.append(line[i])
    
    print('When asked for the score, enter 0 if the word was unknown \nor you want to change the guess I suggest.')
    word = input ("Enter your initial guess: ")
# Main loop : search for words fitting the scores, and reduce the search scope
    while not found:
        s = input ("Enter your score: ")
        if s == '0':
            print('A few more suggestions: choose one...')
            for i in range(min(5,len(wordList))):
                print(wordList[i], end = ' ')
            word = input ("Enter your new guess: ")
            continue
        elif s == '+++++':
            print('Congratulations !!!')
            found = True
        elif s == '-----':
            print("That wasn't a good guess. Try playing a word with several vowels such as: adieu, about, above...")
        else:
            count, wordList = search(filename, s, word, wordList)
            if count == 0:
                import sys
                sys.exit('no matching word: please try again from the beginning')
            else:
                suggest = select(word, wordList)
                print(f'Found {count} matching words --> my suggestion: {suggest}')
                word = suggest
                if count < 6:
                    print ('Possible words are: ',end = ' ')
                    for i in range(min(5,len(wordList))):
                        print(wordList[i], end = ' ')
                    print()
