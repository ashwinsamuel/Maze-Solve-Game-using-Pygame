# Maze Solver Game

An agent in a gridworld navigates its way from its current position to a target position where the maze is not known initially. 

Similar search challenges arise frequently in real-time computer games, such as Starcraft and robotics. To control characters in such games, the player can click on known or unknown terrain, and the game characters then move autonomously to the location that the player clicked on. The characters observe the terrain within their limited field of view and then remember it for future use but do not know the terrain initially (due to “fog of war”). The same situation arises in robotics, where a mobile platform equipped with sensors builds a map of the world as it traverses an unknown environment.

I implemented an A star search algorithm and compared its variants to find path from source to target cell. Animations were rendered using PyGame. The variants in order of their efficiency are:
1. Adaptive forward A*
2. Forward A* (tie breaking preference given to nodes with 'greater' G value)
3. Backward A*
4. Forward A* (tie breaking preference given to nodes with 'smaller' G value)


![image](https://user-images.githubusercontent.com/39940488/197607406-ff6ad26a-465e-43cb-a5a9-ebf886eeae42.png)



<B> RESULTS: </B>

1) Forward A* with tie breaker as node with greater g-value is far better

<img width="469" alt="image" src="https://user-images.githubusercontent.com/39940488/199108530-0fef6d4c-dee8-4a5b-ad00-abc80eb9fec1.png">


2) Forward A* is far better than backward A*

<img width="455" alt="image" src="https://user-images.githubusercontent.com/39940488/199108805-bbaac5c4-d789-46dc-8489-c403d29b1535.png">

3) Adaptive A* is slightly better than Forward A*

<img width="455" alt="image" src="https://user-images.githubusercontent.com/39940488/199109132-6b5a340b-e930-4509-93a3-cb35dc01ebb8.png">


