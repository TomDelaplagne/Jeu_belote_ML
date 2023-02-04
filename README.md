# Jeu_belote_ML
The purpose of this repository is to create the perfect IA for the french belote game : 'la coinche', first I'll build a game playable in shell program then i'll try to create an algorythm based on the regret minimization one to know the perfect strategie for the game
There is a switch for my algorythm to be able to use it in the game
I created a neural network to learn the game and to be able to play against it

## Neural algorythm
For now my algorythm is based trying to create a neural network to learn the game, for now the algorithm is playing against dumb players but it'll start soon play against itself. I'm using two layers of 16 neurons with no bias for now. I'm doing a Monte Carlo simulation without 1000 input for each iteration. I'm also using the BFGS method of the scipy.optimize.minimize function. 
### Problems
Here are the problems I'm facing right now :

 - First, my program is really slow, I want to know if there is a way to make it faster
 - Second, I'm not sure if my algorythm is working, I'm not sure if it's learning or not, I'm not sure if it's playing well or not. I'm not yet able to train a complete set of neurons so I need more time to train it

## Regret minimization algorythm
I think this algorithm is what I'll need later

## Way of improvement
 - I'll need to make my program faster
 - I'll need to give more parameters about the game to my neural network
 - Maybe I could do math to decrease the number of parameters I need to give to my neural network (I'm not sure if it's possible)
 - I need to find a way to train my neural network faster or to do it not entirely by hand but saving results to base my next training on it
 
