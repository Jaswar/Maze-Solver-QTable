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
        self.nRows = 40
        self.nColumns = 40
        self.wallRatio = 0.3
        self.gamma = 0.9
        self.learningRate = 0.01
        self.boxSize = 3
        
        
        self.maze = np.zeros((self.nRows, self.nColumns))
        self.qTable = np.zeros((self.nRows, self.nColumns))
        self.rewards = np.zeros((self.nRows, self.nColumns))
        self.screen = pygame.display.set_mode((self.width, self.height))
        
        
        
        for i in range(self.nRows):
            for j in range(self.nColumns):
                if np.random.rand() < self.wallRatio:
                    self.maze[i][j] = 1
        
        for i in range(min(self.boxSize, self.nRows)):
            for j in range(min(self.boxSize, self.nColumns)):
                self.maze[i][j] = 0
                self.maze[self.nRows - i - 1][self.nColumns - j - 1] = 0

                
        
        self.rewards[self.nRows - 1][self.nColumns - 1] = 1000
        self.qTable[self.nRows - 1][self.nColumns - 1] = 10
        
        self.drawMaze()
        pygame.display.flip()
        
    def drawMaze(self):
        cellWidth = self.width/self.nColumns
        cellHeight = self.height/self.nRows
        
        for i in range(self.nRows):
            for j in range(self.nColumns):
                if self.maze[i][j] == 1:
                    pygame.draw.rect(self.screen, (255,255,255), (cellWidth*j, cellHeight*i, cellWidth, cellHeight))
        
     
    def calcNewQValue(self, reward, qcs, qns):
        qcs += self.learningRate*(reward + self.gamma*qns)
        return qcs
        
    def step(self):
        x = np.random.randint(0, self.nColumns)
        y = np.random.randint(0, self.nRows)
        
        maxValue = 0
        while maxValue == 0 or self.maze[y][x] == 1:
            x = np.random.randint(0, self.nColumns)
            y = np.random.randint(0, self.nRows)
            qValues = np.zeros((4))
            if x < self.nColumns - 1:
                qValues[0] = self.qTable[y][x + 1]
            if x > 0:
                qValues[1] = self.qTable[y][x - 1]
            if y < self.nRows - 1:
                qValues[2] = self.qTable[y + 1][x]
            if y > 0:
                qValues[3] = self.qTable[y - 1][x]
            
            maxValue = np.max(qValues)
        
        action = np.random.randint(0,4)
        if action == 0: #RIGHT
            if x < self.nColumns-1:
                if self.maze[y][x + 1] == 1:
                    self.qTable[y][x] = self.calcNewQValue(self.rewards[y][x], self.qTable[y][x], self.qTable[y][x])
                else:
                    self.qTable[y][x] = self.calcNewQValue(self.rewards[y][x + 1], self.qTable[y][x], self.qTable[y][x + 1])
            else:
                self.qTable[y][x] = self.calcNewQValue(self.rewards[y][x], self.qTable[y][x], self.qTable[y][x])
        elif action == 1: #LEFT
            if x > 0:
                if self.maze[y][x - 1] == 1:
                    self.qTable[y][x] = self.calcNewQValue(self.rewards[y][x], self.qTable[y][x], self.qTable[y][x])
                else:
                    self.qTable[y][x] = self.calcNewQValue(self.rewards[y][x - 1], self.qTable[y][x], self.qTable[y][x - 1])
            else:
                self.qTable[y][x] = self.calcNewQValue(self.rewards[y][x], self.qTable[y][x], self.qTable[y][x])
        elif action == 2: #DOWN
            if y < self.nRows - 1:
                if self.maze[y + 1][x] == 1:
                    self.qTable[y][x] = self.calcNewQValue(self.rewards[y][x], self.qTable[y][x], self.qTable[y][x])
                else:
                    self.qTable[y][x] = self.calcNewQValue(self.rewards[y + 1][x], self.qTable[y][x], self.qTable[y + 1][x])
            else:
                self.qTable[y][x] = self.calcNewQValue(self.rewards[y][x], self.qTable[y][x], self.qTable[y][x])
        elif action == 3: #UP
            if y > 0:
                if self.maze[y - 1][x] == 1:
                    self.qTable[y][x] = self.calcNewQValue(self.rewards[y][x], self.qTable[y][x], self.qTable[y][x])
                else:
                    self.qTable[y][x] = self.calcNewQValue(self.rewards[y - 1][x], self.qTable[y][x], self.qTable[y - 1][x])
            else:
                self.qTable[y][x] = self.calcNewQValue(self.rewards[y][x], self.qTable[y][x], self.qTable[y][x])
        
        pygame.display.flip()
        
    def play(self):
        cellWidth = self.width/self.nColumns
        cellHeight = self.height/self.nRows
        x = 0
        y = 0
        move = 0
        while move < int(pow(pow(self.nColumns, 2) + pow(self.nRows, 2), 0.5)*2):
            self.screen.fill((0,0,0))
            self.drawMaze()
            
            move += 1
            qValues = np.zeros((4))
            if x < self.nColumns - 1:
                qValues[0] = self.qTable[y][x + 1]
            if x > 0:
                qValues[1] = self.qTable[y][x - 1]
            if y < self.nRows - 1:
                qValues[2] = self.qTable[y + 1][x]
            if y > 0:
                qValues[3] = self.qTable[y - 1][x]
                
            action = np.argmax(qValues)
            if action == 0:
                if x < self.nColumns - 1:
                    if self.maze[y][x + 1] != 1:
                        x += 1
            elif action == 1:
                if x > 0:
                    if self.maze[y][x - 1] != 1:
                        x -= 1
            elif action == 2:
                if y < self.nColumns - 1:
                    if self.maze[y + 1][x] != 1:
                        y += 1
            elif action == 3:
                if y > 0:
                    if self.maze[y - 1][x] != 1:
                        y -= 1
            
            pygame.draw.rect(self.screen, (255, 0, 0), (cellWidth*x, cellHeight*y, cellWidth, cellHeight))
            #pygame.time.wait(1)
            pygame.display.flip()
                
    
env = Environment()
iteration = 0
table = list()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    iteration += 1 
    env.step()   
    if iteration % 1000 == 0:
        table = env.qTable
        dist = pow(pow(env.nColumns,2) + pow(env.nRows,2), 0.5)
        for i in range(env.nRows):
            for j in range(env.nColumns):
                if env.qTable[i][j] > 0:
                    d = pow(pow(i, 2) + pow(j, 2), 0.5)
                    if d < dist:
                        dist = d
        print('Closest above 0 cell distance: {:.4f}'.format(dist) + ' Epoch: ' + str(int(iteration / 1000)))
        if dist <= 1:
            env.play()
    if env.qTable[0][0] > 1.:
        break
        
        
        
        
        
        
        
        