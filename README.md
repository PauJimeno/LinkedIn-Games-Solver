# SMTQueens
SMTQueens is a solver for the daily [Queens](https://www.linkedin.com/games/queens/) LinkedIn puzzle game.
The base of the solver is an encoding using the [SAT Module Theories](https://en.wikipedia.org/wiki/Satisfiability_modulo_theories), popularly used to encode many [Constraint Satisfaction Problems (CSP)](https://en.wikipedia.org/wiki/Constraint_satisfaction_problem).

## The encoding
As said, an encoding has been used to solve the Queens puzzle, let's have a look at how it's been done.
### Queens rules (constraints)
The Queens puzzle is based on four easy to understand rules.
1. $C_1$ **Each row** on the board must have **exactly one Queen** placed on it.
2. $C_2$ **Each column** on the board must have **exactly one Queen** placed on it.
3. $C_3$ **Each colour region** on the board must have **exactly one Queen** placed on it.
4. $C_4$ The **four diagonal cells** adjacent to a placed Queen must have **no Queens** placed on them.

Notice that in order to satisfy all the rules above, the board must be square, and the number of colours must be the same as the size of the board. 

### Variables used
To encode the constraints explained above, two variables have been used.
#### Queens ( Q )
This variable is an array of size $n$, where $n$ is the size of the board. The domain of this variable is $[0..n-1]$. The idea behind is that each position of the array represents a column and the value it takes is the row where the Queen is placed. If we ensure each position has a different value, we are essentially satisfying the first and second constraints.
#### Has Queen ( H )
In this case, the variable $H$ is a boolean variable of domain $[0,1]$ which is used for two things.
1. To know if a given $(i, j)$ cell contains a Queen.
2. To know the list of cells containing a Queen for each colour region.

This is done by creating a convenient data structure that references the same variable. The first data structure $S_1$ is a dictionary where each key is a pair of the position of a cell and each value is our $H$ variable, for example:
$S_1$ = { $(0,0)$: $H_1$, $(0,1)$: $H_2$, .. , $(n-1, n-1)$: $H_n$ }

The second data structure $S_2$ is also a dictionary, but in this case each key is a colour of the board, and each key is a list of the $H$ variable representing the cells that colour region has. For example:
$S_2$ = { $C_1$: $[H_1, H_3, H_6, H_4]$, $C_2$:  $[H_7, H_9]$, .. , $C_n$: $[H_8, H_n]$ }

| Variable | Size | Domain|
|--|--|--|
| Q | $1 \times n$ |	$[0..n-1]$ |
| H | $n \times n$ |	$[0,1]$ |

### Constraint implementation
As previously said, there are four constraint we need to satisfy in order to obtain the solution of the board $C_1$, $C_2$, $C_3$ and $C_4$.

#### Rows and Columns constraint
For $C_1$ and $C_2$, it is as simple as ensuring each value taken by the variable is different from each other, this is usually known as $alldiff(Q)$. In our case, since we are using [Z3](https://en.wikipedia.org/wiki/Z3_Theorem_Prover), the constraint syntax is as follows $Distinct(Q)$.
This way we ensure each column has exactly only one Queen (implicit from the variable viewpoint), and each row has exactly one Queen, thanks to the $Distinct(Q)$ constraint.

#### Colour region constraint
For the $C_3$, with the dictionary $S_2$, ensuring each region of colour has exactly one Queen is done like so:
$\forall C_i \in S_2: (\sum_{i = 1}^{len(C_i)} H_i) = 1$

Note that with this constraint, we are just ensuring that there is only one $H=1$ variable for each region, but there is no linking between the $Q$ variable and $H$ variable, the following constraint ensures that:

$\forall i \in 0..n, \forall j \in 0..n: (Q_i=j \implies S_1[(i,j)]=1) \vee (Q_i \neq j \implies S_1[(i,j)]=0)$

#### Diagonal cell constraint
Finally, we need to ensure each adjacent diagonal to a placed Queen is free ($C_4$), to do this the next constraint is used.
Note that the constraint, the variable  ${adj}=[(-1, 1), (1, 1), (-1, -1), (1, -1)]$ is used to get the adjacent cells relative to $(0,0)$.

$\forall i \in 0..n, \forall j \in 0..n: (S_1[i][j]=1) \implies (\bigvee_{x, y \in adj} S_1[(i+x,j+y)]=0)$






