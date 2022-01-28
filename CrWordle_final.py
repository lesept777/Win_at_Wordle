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
# 
# Main code
# 

if __name__ == '__main__':
    filename = "Dict-5757.txt"          # uncomment for english game
    # filename = "Dict-FR-7980.txt"     # uncomment for french game
    found = False
    lst = []

# Create the initial list of words    
    wordList = []
    with open(filename) as file:
        Lines = file.readlines()
        for line in Lines:
            line = line[:-1].lower().split()
            for i in range(len(line)):
                wordList.append(line[i])
        
    word = input ("Enter your initial guess: ")
# Main loop : search for words fitting the scores, and reduce the search scope
    while not found:
        s = input ("Enter your score (or 0 if the word was unknown): ")
        if s == '0':
            print('A few more suggestions: choose one...')
            for i in range(min(5,len(lst))):
                print(lst[i], end = ' ')
            word = input ("Enter your new guess: ")
            continue
        elif s == '+++++':
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
