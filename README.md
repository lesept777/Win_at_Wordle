# Win_at_Wordle
## Win when playing Wordle

If you are here, it means that you know what Wordle is. Play it here : https://www.powerlanguage.co.uk/wordle/

This Python script helps you to win, that is to find the correct word in 6 guesses or less.

To begin, choose as first guess a word with many vowels, it will be simpler for the script to converge. Some examples: adieu, about, above...

Type it in Wordle, the game answers with a color code: enter this answer using the following code
* use - for grey (letter not in the word)
* use = for yellow (misplaced letter)
* use + for green (correct place)

For example : -+==-

The script suggests a word : play it in Wordle.

Enter Wordle's answer until you find the correct word...

To play in French (https://wordle.louan.me/), just change the dictionnary file name :
```filename = "Dict-5757.txt```
to
```filename = "Dict-FR-7980.txt"```

## New version (Jan. 30, 2022)
Use `CrWordle_final_better.py` which finds in less guesses. It chooses the next guess by computing the distance with the previous one and chooses the largest distance in the list of possible candidate words.

At the cost of a dependency: install textdistance (*pip install textdistance*)

## Another version (Jan. 31, 2022)
Added a notion of letter diversity: now the suggestion  favors words with more varied letters (still `CrWordle_final_better.py`).

## Another version (Feb. 3, 2022)
Added the possibility of choosing another word, when there are up to 5 remaining possibilities. This because today's word was 'shard' and the code proposed 'shark' which was the Wordle a few days ago. In this case, enter 0 for the score then choose your word in the possibilities provided by the code.

## Another version (feb. 5, 2022)
I found the game Absurdle (https://qntm.org/files/absurdle/absurdle.html) a clone of Wordle, more difficult to play because it cheats... Actually, the target word isn't chosen at the beginning of the game and changes depending on your suggestions and their scores, in order to last as long as possible. Game in 6 or 7 is not unusual, game in 5 is quite rare.

I added the possibility of suggesting the new word using a kind of minimax algorithm: 
* for each initial word in the list of possible guesses, 
* for each target word in the total list of 5757 words, 
* minimize the maximum number of guesses necessary to find the target when beginning with the initial word

This may be much longer, as the minimax is used when the list of possible guesses has less than 80 elements. Try it: **CrWordle_final_minimax.py**. Answer y at the question about playing Absurdle.

## Another version (feb. 16, 2022) - maybe the last one
Another interesting and more challenging game : quordle (https://www.quordle.com/#/). Here, you must find 4 words at the same time, in 9 guesses or less. Enter your guess and quordle answers similarly to Wordle, but for the 4 words.

There is another dependancy: you must install pandas (*pip install pandas*). To play quordle, answer '2' at the first question of the code and then input the 4 answers of quordle separated by a space. Answer in the order upper-left upper-right lower-left lower-right. If the code suggests a word that quordle doesn't recognize, answer 0 as before and choose another word.

So the last final version is: **CrWordle_final_last.py**: Have fun!
