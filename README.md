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


