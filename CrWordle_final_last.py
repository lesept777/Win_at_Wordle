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

import pandas as pd
import textdistance
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

#Find the intersection of 2 lists
def intersection(lst1, lst2):
    if len(lst1) == 0 or len(lst2) == 0:
        return []
    return list(set(lst1) & set(lst2))

# minimax : choose the word that minimizes the maximum number of guesses
"""
pour chaque mot M1 de la liste :
    pour chaque mot M2 différent de M1 :
        calculer le nombre de coups pour trouver M2 à partir de M1
        prendre le maximum
renvoyer le M1 qui a le minimum, le plus haut dans la liste
    
"""
def minimax (lst, initial):
    minN = 100
    nlst = len(lst)
    k = 0
    bestWord = ''
    for word in lst:
        maxN = 0
        for target in initial:
            if word != target:
                n = countGuesses (word, target, lst)
                maxN = max(n, maxN)
        if (nlst - k)%10 == 0:
            print(nlst-k,end='')
        else:
            print('.',end='')
        if maxN < minN:
            minN = maxN
            bestWord = word
        k += 1
    return bestWord, minN

# Count the guesses necessary to find a target, beginning with a word
def countGuesses (word, target, lst):
    n = 0
    s = score(word, target)
    while s != '+++++':
        _ , lst = search(s, word, lst)
        word = select(word, lst)
        s = score(word, target)
        # print('suggest='+word+'   target='+target+'  score: '+str(s))
        if not lst:
            return 0
        n += 1
    return n

# Try to use as many different letters in the word
def diversity(word):
    return len(set(word)) / 5

# Try to maximize the number of different letters used in the alphabet
def nottested(word):
    n = 1
    for letter in word:
        if letter in alphabet:
            n +=1
    return n

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

# Search words in a list matching a given 'target' score
def search(target, guess, wordList):
    count = 0
    lst = []
    for test in wordList:
        if score(guess, test) == target:
            count += 1
            lst.append(test)
    return count, lst

# Select in the list the farthest word from last guess
def select(guess, lst):
    if len(lst) == 1:
        return lst[0]
    maxdist = 0
    # number = 0
    bestword = ''
    for word in lst:
        # dist = textdistance.bwtrle_ncd.distance(guess, word)
        # dist = textdistance.mra.distance(guess, word)
        # dist = textdistance.editex.distance(guess, word)
        dist = textdistance.entropy_ncd.distance(guess, word)
        dist *= diversity(word)
        dist *= nottested(word)
        # print(word+' dist = '+str(dist)+ ' ('+str(maxdist)+')')
        if dist > maxdist:
            maxdist = dist
            bestword = word
        #     number = 0
        # if dist == maxdist:
        #     number += 1
    return bestword

def longDistance(lst, previousWord):
    maxdist = 0
    bestword = ''
    for word in lst:
        # print(word,end=' ')
        dist = textdistance.entropy_ncd.distance(previousWord, word)
        # print(dist)
        if dist > maxdist:
            maxdist = dist
            bestword = word
    return bestword, maxdist

# Main code for playing Wordle & Absurdle
def findWordle (word, wordList, opt):
# Main loop : search for words fitting the scores, and reduce the search scope
    found = False
    while not found:
        previousWord = word
        for letter in word:
            alphabet[ord(letter)-97]='-'
        s = input ("Enter your score: ")
        if s == '':
            s = '+++++'
        
        # Unknown word or change suggestion
        if s == '0':
            print('A few more suggestions: choose one...')
            for i in range(min(5,len(wordList))):
                print(wordList[i], end = ' ')
            word = input ("Enter your new guess: ")
            continue

        # Found the target!!!
        elif s == '+++++':
            print('Congratulations !!!')
            found = True

        # Very bad guess
        elif s == '-----':
            print("That wasn't a good guess. Try playing a word with several vowels such as: \nadieu, about, above, crane, ratio, audio, tears, stare...")
            word = input ("Enter your new guess: ")

        # Normal guess: provide suggestion
        else:
            count, wordList = search(s, word, wordList)
            # No fitting word: did you make a mistake???
            if count == 0:
                import sys
                sys.exit('no matching word: please try again from the beginning')

            # Suggest a new word: 2 options
            else:
                if opt == '1' and count < 80:
                # Try minimax if less than 80 possibilities and playing Absurdle: 
                    print(f'Found {count} matching words : launching minimax')
                    suggest, _ = minimax(wordList, initial)
                    print(f'--> my suggestion: {suggest}')

                # Standard suggestion (good for Wordle)
                else:
                    suggest = select(word, wordList)
                    if count == 1:
                        print(f'The solution is {suggest}')
                        found = True
                    else:
                        if textdistance.entropy_ncd.distance(suggest, previousWord) < 0.1:
                            suggest, _ = longDistance(wordList, previousWord)
                        print(f'Found {count} matching words --> my suggestion: {suggest}')   
                word = suggest
                
                # Print several suggestions when less than 6 possibilities
                # You can select a different one by inputting 0 when asked for the score
                if 1 < count < 6:
                    print ('Possible words are: ',end = ' ')
                    for i in range(min(5,len(wordList))):
                        print(wordList[i], end = ' ')
                    print()
    
# Main code for playing Quordle (the strategy is a little bit different)
def quordle (word, WL):
    scores = pd.DataFrame(columns = ["0", "1","2","3"])
    guesses = [word]
    found = [False] * 4
    count = [0] * 4
    wordList = [WL] * 4
    goodWords = [''] * 4
    inter = WL
    foundAll = False
    nbTrials = 0
    print('When entering scores, use space as separator.')
    
    while not foundAll:
        previousWord = word
        for letter in word:
            alphabet[ord(letter)-97]='-'

        ans = input("Enter the 4 scores: ")
        if ans=='0':
            # Unknown word or change suggestion
            print('A few more suggestions: choose one...')
            for i in range(4):
                if not found[i]:
                    print(wordList[i][:min(6,len(wordList))])
            word = input ("Enter your new guess: ")
            guesses[len(guesses)-1] = word
            continue
        else:
            s = list(map(str, ans.split()))
            
        scores.loc[len(scores)] = s
        
        nbFound = 0
        for i in range(4):
            if s[i] == '+++++': 
                found[i] = True
                nbFound += 1
                if scores.iloc[nbTrials-1,i] != '+++++':
                    goodWords[i] = word
        if nbFound == 4:
            # Finished!!!
            print(f'Congratulations !!! Found in {nbTrials+1} guesses.')
            foundAll = True
            continue
        # elif nbFound !=0: print(f'Guess number {nbTrials}: found {nbFound} solutions')
            
        if nbFound > 1 or nbTrials > 4:
        # Running out of time: try to find remaining solutions
            minN = 100000
            for i in range(4):
                if not found[i]:
                    wList = WL
                    for j in range(nbTrials+1):
                        countJ, wList = search(scores.iloc[j,i], guesses[j], wList)
                    if countJ == 0:
                        print(f"Can't find a guess for word {i}... searching again...")
                        wList = []
                        maxdist = 0
                        bestword = ''
                        for i in range(nbTrials+1):
                            word, distance = longDistance(WL, guesses[i])
                            wList.append(word)
                            if distance > maxdist:
                                maxdist = distance
                                bestword = word
                        word = bestword
                        minN = i
                    elif countJ < minN:
                        minN = countJ
                        k = 0
                        while wList[k] in guesses: k += 1
                        word = wList[k]
            guesses.append(word)
            print(f'Found {minN} matching words ---> my suggestion: {word}')
            if minN < 6 and len(wList) > 1: print(f'Other words are: {wList}')
            
        # Normal guess: provide suggestion
        else:
            foundOneMore = False
            for i in range(4):
                if not found[i]:
                    count[i], wordList[i] = search(s[i], word, wordList[i])
            # Found one of the wordles?
                if not found[i] and count[i] == 1:
                    found[i] = True
                    suggest = wordList[i][0]
                    print(f'Solution for Wordle {i} is {suggest}')
                    word = suggest
                    foundOneMore = True
                    goodWords[i] = word
                    break
                else:
                    if not found[i]:
                        x = wordList[i]
                        temp = intersection(inter, x)
                        if len(temp) !=0:
                            inter = temp
            countInter = len(inter)
            # Intersection of the possibilities is not empty
            if countInter != 0:
                if not foundOneMore:
                    suggest = select(word, inter)
#                    print (f'previousWord = {previousWord}')
                    if textdistance.entropy_ncd.distance(suggest, previousWord) < 0.1:
                        suggest, _ = longDistance(inter, previousWord)
                        # suggest, _ = longDistance(wordList, previousWord)
                    else:
                        for w in inter:
                            for x in goodWords:
                                if textdistance.entropy_ncd.distance(w,x) < 0.2:
                                    inter.remove(w)
                        suggest = inter[0]
                        if suggest == previousWord and len(inter) > 1: suggest = inter[1]
                    print(f'Found {countInter} matching words --> my suggestion: {suggest}')   
                word = suggest
                guesses.append(word)
            # Intersection is empty (should never happen)
            else:
                import sys
                sys.exit('no matching word: please try again from the beginning, verify your answers')

        nbTrials += 1
# 
# Main code
# 

if __name__ == '__main__':
    filename = "Dict-5757.txt"          # uncomment for english game
    # filename = "Dict-FR-7980.txt"     # uncomment for french game

# Create the initial list of words    
    wordList = []
    with open(filename) as file:
        Lines = file.readlines()
        for line in Lines:
            line = line[:-1].lower().split()
            for i in range(len(line)):
                wordList.append(line[i])
    initial = wordList
    
    print('Options:')
    print('0 : standard Wordle (hit enter)')
    print('1 : Absurdle')
    print('2 : Quordle')
    print('3 : Squabble (blitz)')
    opt = input ('Which game are you playing? ')
    
    print('When asked for the score, enter 0 if the word was unknown ')
    print('or if you want to change the guess I suggest.')
    word = input ("Enter your initial guess: ")
    
    if opt == '0' or opt == '1':
        findWordle (word, wordList, opt)
    elif opt == '2':
        quordle (word, wordList)
    else:
        print('When entering scores, hit <Enter> for +++++.')
        while True:
            findWordle (word, wordList, opt)
            word = input ("Enter your initial guess: ")
