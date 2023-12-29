# SmasHack: gotta smash 'em all! 👾

**Developed by:** the Hackward Hackers - [Daniele Bedini](https://github.com/danielebedini), [Francesca Poli](https://github.com/francescapoli98), [Gioele Modica](https://github.com/pavomod) and [Giovanni Criscione](https://github.com/gcriscione) \
**Course:** Artificial Intelligence Fundamentals, a.y. 2023/2024 \
**Master degree:** Computer Science, Artificial Intelligence curriculum 

<img src="https://apre.it/wp-content/uploads/2021/01/logo_uni-pisa.png" width="200" />

The project is based on an intelligent agent that plays a custom level in the Nethack rogue game. The agent is inserted into a room, which is the enviroment it has to percept. The agent has to firstly pick up and wield a weapon, then kill all the monsters and, finally, finish the level exiting through the stairs and win.

The agent's aim is to use a searching algorithm to reach the desired targets one at a time, following the order previously listed: weapon, monsters, stairs. At each step of the agent, the heuristic will evaluate the best possible move, taking into consideration the targets' order and placement, and the agent's health level represented as hit points: the heuristic needs to predict all the possible scenarios and choose the one that seems to be the most convenient at the moment in order to take a step in one direction. 

We solved this task by developing two different heuristics: 
- **Class-based heuristic:** the agent is told exaclty what to do considering the percepts received in input and fed to the heuristic function in a more direct approach.
- **Weighted sum-based heuristic:** the agent is guided by a system of priorities based off the percepts received in input, that converge into a weighted summation of all the targets' importance.


## Repository structure 
 ┣ 📄 `heuristic_FD.py`    // python file containing the weighted sum heuristic          
 ┣ 📄 `heuristic_GG.py`    // python file containing the direct heuristic    
 ┣ 📜 `report.ipynb`       // jupyter notebook with in-depth explanations, compared results and statistics  \
 ┗ 📄 `utils.py`           // python support file containing all the default background functions    