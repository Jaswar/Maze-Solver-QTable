# Maze-Solver-QTable
A Q Learning/Q Table approach to solving a maze.

Description: This code tries to solve a randomly generated maze by using a Q-Table. This means that every cell in a maze has got some certain value defining how 'good' it is to be in this cell. Bot moves by searching for the highest q valued cell in its closest neighbourhood. Each Q-value in a given cell is updated with q learning algorithm that takes into consideration the reward bot got by reaching this state, value of the next state, gamma (also known as the discount factor), learning rate.

Required libraries:
- numpy
- pygame

My specs:
- i7-7700HQ Processor
- 16GB RAM
- NVIDIA Quadro M1200 4GB graphics card

Training: In order to increase performance, initially bot will not perform any moves, therefore current path will not be displayed. Actually, at the beginning bot does not have any route to follow, as it starts searching for the path from the end. You can see in the console however how far a bot is from solving the maze. It shows which closest cell has got a q-value of over zero, which means that a path has been found from this point to the very end of a maze. Once the distance equals 1, bot will start moving, meaning it found the path. There is no guarantee that first path will be the shortest one, but after time it should find the most optimal route. 

This way of solving a maze is quicker than genetic algoritm, especially after some certain performance upgrades.
