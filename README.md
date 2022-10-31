A star search and its varients are implemented to find path from source(top left) to target(bottom right). The variants in order of their efficiency are:
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


