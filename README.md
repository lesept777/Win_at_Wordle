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
