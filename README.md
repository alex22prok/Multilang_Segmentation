# Homework 3: Word Segmentation Two Ways

## Name: 

## Part 1: Preliminaries

1. What is your NLTK version number?
    3.9.1
        C:\Users\Prok>py
        Python 3.13.7 (tags/v3.13.7:bcee1c3, Aug 14 2025, 14:15:11) [MSC v.1944 64 bit (AMD64)] on win32
        Type "help", "copyright", "credits" or "license" for more information.
        >>> import nltk
        >>> nltk.__version__
        '3.9.1'
        >>> exit

2. How many utterances are in the training set?
        50207

3. How many utterances are in the test set?
        12552

4. Why is it important to have a separate training and test set?
    Because the model will likely peform much bettter on the data it was trained on. Testing with a separate set allows for unbiased evaluation and measures how well the model can generalize

## Part 3: Calculating a Baseline

5. What were the training precision, recall, and F1 scores for the baseline segmenter on the training and test data?
    Training
    P: 63.46        R: 100.0                F1: 77.65       

    Testing
    P: 64.53        R: 100.0                F1: 78.44

6. Where these higher or lower than you expected? Why do you think the numbers were in this range?
    Recall is 100 because we never miss a boundary, Precision is higher than expected because I thought 1 syllable words would be less common. Many one syllable words or low syllable words mean few incorrect guessing at non-word buondaries. 

## Part 4: Transitional Probability Segmenter

7. What were the precision, recall, and F1 scores for the training and test data?
    Training
    P: 96.59        R: 47.86                F1: 64.01

    Testing
    P: 96.69        R: 42.35                F1: 58.9

8. Why did the training scores outperform the test scores?


9. Why do you think the transitional probability model did so poorly?


10. Would using larger n-grams help here? Why?


## Part 5: Subtractive Segmenter

11. What were the precision, recall, and F1 scores for the training and test data?
    [{0}, set(), {0, 1}, {0, 1}, {0}, {0}, {0}, set(), {0, 1, 2}, {0}]
    [{0}, set(), {0, 1}, {0, 1}, {0, 2}, {0}, {0}, set(), {0, 1, 2}, {0}]
    Training
    P: 94.22        R: 86.89                F1: 90.41

    [set(), {0}, {0, 1, 2, 3, 4, 5}, {0, 1}, {0, 1}, set(), {0, 1, 2, 4, 5}, {0}, {0, 1}, {0, 1}]
    [set(), {0, 1, 2, 3, 4}, {0, 1, 2, 4, 5}, {0, 1}, {0, 1}, set(), {0, 1, 2, 4, 5}, {0}, {0, 1}, {0, 1}]
    Testing
    P: 94.78        R: 81.13                F1: 87.43

12. If we change the reward from 1 to 10, will that affect the results? Why or why not?


13. What if we change the reward to -1?


14. If we added a requirement that every word have just one primary stressed vowel (indicated with a 1 in ARPABET), would we be more likely to have over-segmentation or under-segmentation? Why or why not?


## Questionnaire

1. How long did it take you to complete this assignment?


2. Which aspects of this assignment did you find particularly challenging? Was anything frustrating?


3. How difficult was this assignment for you on a scale of 1 (trivial) to 10 (impossible)?


4. What resources did you use in completing this assignment?
