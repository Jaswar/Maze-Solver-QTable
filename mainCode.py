# -*- coding: utf-8 -*-
"""
Created on Mon May 20 18:05:38 2019

@author: janwa
"""
import numpy as np
import pygame

np.random.seed()

class Environment(object):
    
    def __init__(self):
        self.width = 900
        self.height = 900
        self.nRows = 100
        self.nColumns = 100
        self.wallRatio = 0.3
        self.gamma = 0.9
        self.alpha = 0.9
        self.boxSize = 3
        self.moveReward = 0.0001
        
        self.maze = np.zeros((self.nRows, self.nColumns))
        self.qTable = np.zeros((self.nRows, self.nColumns))
        self.rewards = np.zeros((self.nRows*self.nColumns, self.nRows*self.nColumns))
        self.screen = pygame.display.set_mode((self.width, self.height))
        
        
        
        for i in range(self.nRows):
            for j in range(self.nColumns):
                if np.random.rand() < self.wallRatio:
                    self.maze[i][j] = 1
        
        
        
        for i in range(min(self.boxSize, self.nRows)):
            for j in range(min(self.boxSize, self.nColumns)):
                self.maze[i][j] = 0
                self.maze[self.nRows - i - 1][self.nColumns - j - 1] = 0
        
        
        for i in range(self.nRows*self.nColumns):
            row = int(i / self.nColumns)
            column = i % self.nColumns
            if self.maze[row][column] != 1:
                if column > 0:
                    if self.maze[row][column - 1] != 1:
                        self.rewards[i][row*self.nColumns + column - 1] = self.moveReward
                    else:
                        self.rewards[i][i] = self.moveReward
                else:
                        self.rewards[i][i] = self.moveReward
                        
                if column < self.nColumns - 1:
                    if self.maze[row][column + 1] != 1:
                        self.rewards[i][row*self.nColumns + column + 1] = self.moveReward
                    else:
                        self.rewards[i][i] = self.moveReward
                else:
                        self.rewards[i][i] = self.moveReward
                        
                if row > 0:
                    if self.maze[row - 1][column] != 1:
                        self.rewards[i][(row - 1)*self.nColumns + column] = self.moveReward
                    else:
                        self.rewards[i][i] = self.moveReward
                else:
                        self.rewards[i][i] = self.moveReward     
                
                if row < self.nRows - 1:
                    if self.maze[row + 1][column] != 1:
                        self.rewards[i][(row + 1)*self.nColumns + column] = self.moveReward
                    else:
                        self.rewards[i][i] = self.moveReward
                else:
                        self.rewards[i][i] = self.moveReward
            
        
        self.qTable = self.rewards.copy()
        self.rewards[self.nRows*self.nColumns - 1][self.nColumns*self.nRows - 1] = 1000
        self.posx = 0
        self.posy = 0
        self.drawMaze()
        
        
    def drawMaze(self):
        self.screen.fill((0,0,0))
        cellWidth = self.width/self.nColumns
        cellHeight = self.height/self.nRows
        
        for i in range(self.nRows):
            for j in range(self.nColumns):
                if self.maze[i][j] == 1:
                    pygame.draw.rect(self.screen, (255,255,255), (cellWidth*j, cellHeight*i, cellWidth, cellHeight))
                    
        pygame.draw.rect(self.screen, (255, 0, 0), (cellWidth*self.posx, cellHeight*self.posy, cellWidth, cellHeight))
        pygame.display.flip()
    
    def step(self):
        pos = np.random.randint(0, self.nColumns*self.nRows)
        row = int(pos / self.nColumns)
        column = pos % self.nColumns
        while self.maze[row][column] == 1:
            pos = np.random.randint(0, self.nColumns*self.nRows)
            row = int(pos / self.nColumns)
            column = pos % self.nColumns
        
        actions = list()
        for i in range(self.nColumns*self.nRows):
            if self.rewards[pos][i] != 0:
                actions.append(i)
        
        action = np.random.choice(actions)
        
        TD = self.rewards[pos][action] + self.gamma * self.qTable[action, np.argmax(self.qTable[action])] - self.qTable[pos][action]
        self.qTable[pos][action] += self.alpha * TD
        
    def play(self):
        self.posx = 0
        self.posy = 0
        for i in range(int(2 * pow(pow(self.nRows, 2) + pow(self.nColumns, 2), 0.5))):
            action = np.argmax(self.qTable[self.posy*self.nRows + self.posx])
            self.posx = action % self.nRows
            self.posy = int(action / self.nRows)
            self.drawMaze()
            
            if self.posx == self.nColumns - 1 and self.posy == self.nRows - 1:
                break
                   
    
env = Environment()
t = env.rewards 
i = 0
while True:
    i += 1
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
    env.step()
    if i % 30000 == 0:
        print('Showing the results')
        env.play()
    Q = env.qTable
          
        
        
