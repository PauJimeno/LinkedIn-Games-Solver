
# LinkedIn Games Solver
LinkedIn-Games-Solver is a solver for the daily [Queens](https://www.linkedin.com/games/queens/) and [Zip](https://www.linkedin.com/games/zip/) LinkedIn puzzle games.

It automatically fetches the puzzle information from the games webpage, then it prints the solution as well as saving the board informnation in a `.json` file.

The base of the solver is an encoding using the [SAT Module Theories](https://en.wikipedia.org/wiki/Satisfiability_modulo_theories), popularly used to encode many [Constraint Satisfaction Problems (CSP)](https://en.wikipedia.org/wiki/Constraint_satisfaction_problem).

# 1. How to use the solver locally
## Set up the project
1. Clone the repository in the desired directory
	```bash
	git clone https://github.com/PauJimeno/SMTQueens.git
	```
2. Create a virtual environment using the Python version 3.10
	```bash
	python  -m  venv  venv
	```
3. Activate virtual environment
	```bash
	source venv/Scripts/activate
	```
4. Install the project (from the project root)
	```bash
	pip install -e .
	```
## Use the solver
Two console commands have been defined in order to use the solver.
This commands will automatically run the main application, fetching the puzzle, solving it, printing the solution and saving the solved instance into a `.json` file. 
```bash
zip_solver
queens_solver
```

# 2. Queens Game encoding
As said, an encoding has been used to solve the Queens puzzle, let's have a look at how it's been done.
## Queens constraints
The Queens puzzle is based on four easy to understand rules.
1. $C_1$ **Each row** on the board must have **exactly one Queen** placed on it.
2. $C_2$ **Each column** on the board must have **exactly one Queen** placed on it.
3. $C_3$ **Each colour region** on the board must have **exactly one Queen** placed on it.
4. $C_4$ The **four diagonal cells** adjacent to a placed Queen must have **no Queens** placed on them.

Notice that in order to satisfy all the rules above, the board must be square, and the number of colour regions must be the same as the size of the board. 

## Variables used
To encode the constraints explained above, two variables have been used.
### Queens $Q$
This variable is an array of size $n$, where $n$ is the size of the board. The domain of this variable is $[0..n-1]$. The idea behind is that each position of the array represents a column and the value it takes is the row where the Queen is placed. If we ensure each position has a different value, we are essentially satisfying the first and second constraints.
### Has Queen $H$
In this case, the variable $H$ is a boolean variable of domain $[0,1]$ of size $m=n \cdot n$ used for two things.
1. To know if a given $(i, j)$ cell contains a Queen.
2. To know the list of cells containing a Queen for each colour region.

This is done by creating a convenient data structure that references the same variable. The first data structure $S_1$ is a dictionary where each key is a pair of the position of a cell and each value is our $H$ variable, for example:
$S_1$ = { $(0,0)$: $H_1$, $(0,1)$: $H_2$, .. , $(n-1, n-1)$: $H_m$ }

The second data structure $S_2$ is also a dictionary, but in this case each key is a colour of the board, and each value is a list of the $H$ variable representing the cells that colour region has. For example:
$S_2$ = { $C_1$: $[H_1, H_3, H_6, H_4]$, $C_2$:  $[H_7, H_9]$, .. , $C_n$: $[H_8, H_m]$ }

| Variable | Size | Domain     |
|----------|------|------------|
| $Q$      | $n$  | $[0..n-1]$ |
| $H$      | $m$  | $[0,1]$    |

## Constraint implementation
As previously said, there are four constraint we need to satisfy in order to obtain the solution of the board $C_1$, $C_2$, $C_3$ and $C_4$.

### Rows and Columns constraint
For $C_1$ and $C_2$, it is as simple as ensuring each value taken by the variable is different from each other, this is usually known as $alldiff(Q)$ constraint. In our case, since we are using [Z3](https://en.wikipedia.org/wiki/Z3_Theorem_Prover), the constraint syntax is as follows $Distinct(Q)$.
This way we ensure each column has exactly only one Queen (implicit from the variable viewpoint), and each row has exactly one Queen, thanks to the $Distinct(Q)$ constraint.

### Colour region constraint
For the $C_3$, with the dictionary $S_2$, ensuring each region of colour has exactly one Queen is done like so:
$\forall C_i \in S_2: (\sum_{k = 1}^{len(C_i)} H_k) = 1$

Note that with this constraint, we are just ensuring that there is only one $H=1$ variable for each region, but there is no linking between the $Q$ variable and $H$ variable, the following constraint is needed:

$\forall i \in 0..n, \forall j \in 0..n: (Q_i=j \implies S_1[(i,j)]=1) \wedge (Q_i \neq j \implies S_1[(i,j)]=0)$

### Diagonal cell constraint
Finally, we need to ensure each adjacent diagonal cell to a placed Queen is free ($C_4$), to do this the next constraint is used.
Note that the constraint uses the variable  ${adj}=[(-1, 1), (1, 1), (-1, -1), (1, -1)]$ to get the adjacent cells relative to $(0,0)$.

$\forall i \in 0..n, \forall j \in 0..n: (S_1[i][j]=1) \implies (\bigwedge_{x, y \in adj} S_1[(i+x,j+y)]=0)$

# 3. Zip Game Encoding
The Zip encoding made, is a bit simpler than the queens one, but it is much interesting because it doesn't revolve around a set of well-defined constraints, instead a way to represent a path is needed.
## Zip Constraints
The zip puzzle has two very easy to understand constraints:
- $C_1$ The path must use each cell of the board.
- $C_2$ The path must go through each number dot in an increasing order.

## Variables used
To represent a path a single variable has been used.

### Path $P$
The path will be represented with the variable $P$, the idea behind this variable is to have a number for each cell of the board, this value will represent the sequence of a path that will need to be strictly increasing.
To do this, $P$ is a variable of size $n \times n$ and its domain is $[0..n-1]$, where $n$ is the size of the board (which is always square).

| Variable | Size         | Domain     |
|----------|--------------|------------|
| $P$      | $n \times n$ | $[0..n-1]$ |

## Constraint implementation
To ensure $P$ defines a coherent and increasing path through each cell of the board two constraints have been used.

### Path propagation
The idea behind this constraint is to define the behaviour of a path, to do this it is as simple as ensuring that for each $P[i][j]$ cell in the board (except the first and last number points) there is exactly one accessible neighbouring cell with the value $P[i][j]-1$ and one with the value of $P[i][j]+1$.
Since the variable $P$ is of size $n \times n$ the $C_1$ constraint is implicitly satisfied.
The constraint formalization, which uses three functions looks like this:
- Accessible neighbouring cells $adj(x, y)$
- Is start $is\\_start(x, y)$
- Is end $is\\_end(x, y)$

Forward propagation\
$\forall i \in 0..n, \forall j \in 0..n: \lnot is\\_end(i, j) \implies (\sum_{x,y \in adj(i,j)} P_{x,y} = P_{i,j}+1) = 1$

Backwards propagation\
$\forall i \in 0..n, \forall j \in 0..n: \lnot is\\_start(i, j) \implies (\sum_{x,y \in adj(i,j)} P_{x,y} = P_{i,j}-1) = 1$

This constraint alone is enough to define a coherent path that starts and end in the corresponding cells and occupies the entire board.
But we can help the solver a little bit with the next constraint.

### Start and end cells
Since we know the positions of the starting and ending cells we can define their values ($0, n-1$), so the solver doesn't need to figure it out by himself.
Two functions are used for this constraint:
- Start cell $start()$
- End cell $end()$

$x,y \in start(): P_{x,y}=0$\
$x,y \in end(): P_{x,y}=n-1$

### Path sequence
The last part of the encoding is satisfying $C_2$, with the current viewpoint this can easily be archived.
The constraint uses the following function:
- $points$ which is an ordered list of $x,y$ positions for each point cell

$\forall i \in 0..len(points)-2: P_{points[i]}<P_{points[i+1]}$


# 4. Additional information
## File structure
There are two basic directories:
### Source code `/src`
This directory contains the core components of the main application:
- `/src/solver` has the encoding definition for every game as well as a Solver class used to interact with the encodings and the Z3 solver.
- `/src/scraper` contains the code for the scraping of the games website information
- `/src/visualizer` includes the console and image printing code to represent the solver's found solution in a user-friendly way.
- `/src/base` here we will find the definition of the main functions called from the console commands.

### Resources `/resources`
This directory contains the puzzles solved and some variable definitions later used in the code.
- `/resources/instances` here we will find the puzzle information (including solution) for all the games supported.
- `/resources/solved_boards` this directory holds the images of the solved boards (currently only queens game)
- `/resources/variables` contains a `.json` file where all the styles for the `visualizer` are defined, from colours to text style. It also contains a `.json` file for all the html literals used in the scraping process.

