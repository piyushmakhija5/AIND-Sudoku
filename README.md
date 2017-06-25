# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: In the reduce_puzzle function which  is used iteratively to satisfy eliminate and only_choice constraint, we add another constraint for naked twins. This way in every iteration, after checkingfor existing constraints, our code will now also check for naked twin condition.

In the naked_twins function, we first look for all twins and store them in a twins_dict dcitionary. Next we check if any of these twins satisfy the naked_twins condition i.e. if any key in the twin_dict has exactly 2 value elements. We add such elements to the naked_twins dictionary. Next from this dictionary we identify the unit where we can apply this constraint and replace the possible values in the  identified boxes

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Identify Diagonal elements and add them to unitlist(i.e. list of constraints used for normal sudoku). This will add an additional constraint for the system needed to be satisfied for diagonal sudoku puzzle

To identify diagonal elements we zip the the 'rows list'+'inverse column list' and 'inverse row list'+'column list' to get the diagonal and anti-diagonal.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

