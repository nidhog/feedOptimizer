# -*- coding: utf-8 -*-
"""
Quora Challenge: Feed Optimizer - Quick and Dirty Solution Proposal

Created on Wed Jan 14 10:29:27 2015

@author: ismail.elouafiq
"""
class Story(object):
    """
    Simple Story Object
    
    @param score:  score of the story
    
    @param height: height of the story
    
    @param time:   time of the story
    """
    def __init__(self, storyId, time, score, height):
        self.id = storyId
        self.score = score
        self.height = height
        self.time = time

class StoryContainer(object):
    """
    Main object that computes the optimal solution
    
    @param stories : list containing all the recent stories
    """
    def __init__(self):
        self.stories = []
    def addStory(self, story):
        self.stories.append(story)
    # Remove the stories not within the window
    def slideWindow(self, time, window):
        if(self.stories):
            limit = time-window
            while(self.stories and self.stories[0].time<limit):
                self.stories.pop(0)
                
class StoryTeller(object):
    """
    Main object that computes the optimal solution
    
    @param window:         size of the time window
    
    @param height:         total height in pixels
    
    @param currentTime:    the time of the last event captured
    
    @param nextId:         Id of the upcoming story
    
    @param recentStories:  stories within the time window
    """
    def __init__(self, window, height):
        self.window = window
        self.height = height
        self.currentTime = 0
        self.nextId = 1
        self.recentStories = StoryContainer()
    # Update the time at each captured event 
    def updateTime(self, time):
        self.currentTime = time   
    def validTime(self, time):
        if(time>= (self.currentTime-self.window) and time <= self.currentTime):
            return True
        else:
            return False
    # Return the id of the story and increment next id
    def getCurrentId(self):
        currentId = self.nextId
        self.nextId += 1
        return currentId
    # Add a story and update recentStories
    def addStory(self, time, score, height):
        self.updateTime(time)
        storyId = self.getCurrentId()
        story = Story(storyId, time, score, height)
        if(self.validTime(time)):
            self.recentStories.addStory(story)
    # Return the output to be printed in stdout 
    def getAnswer(self, time):
        self.updateTime(time)
        maximumScore = 0
        idList = []
        self.recentStories.slideWindow(self.currentTime, self.window)
        stories = self.recentStories.stories
        if(stories):
            isInList = self.getScoreAndList([story.score for story in stories],[story.height for story in stories])
            totalNumberOfStories = len(isInList)
            idList = [stories[i].id for i in range(totalNumberOfStories) if isInList[i]]
            maximumScore = sum([stories[i].score for i in range(totalNumberOfStories) if isInList[i]])
            number = len(idList)
            return maximumScore, number, idList
        else:
            return 0,0,[]
    
    # ------------------- 0-1 Knapsack DP Solution ---------------------------
    # Initialize cost matrix
    def costMatrixInit(self, nRows, nColumns):
	return [[0 for i in range(nColumns)] for j in range(nRows)]
    # Get Significant Elements
    def getCheck(self, heights,costMatrix):
        i = len(costMatrix)-1
        currentH =  len(costMatrix[0])-1
        check = []
        for k in range(i+1):
            check.append(0)			
        while (i >= 0 and currentH >=0):
            if (i==0 and costMatrix[i][currentH] >0 )or costMatrix[i][currentH] != costMatrix[i-1][currentH]:
                check[i] =1
                currentH = currentH-heights[i]
            i-=1
        return check
    # Compute cost and return elements
    def getScoreAndList(self, scores, heights):
    	n = len(scores)
    	costMatrix = self.costMatrixInit(n, (self.height)+1)
    	for i in range(0,n):
    		for j in range(0, self.height + 1):
    			if (heights[i] > j):
    				costMatrix[i][j] = costMatrix[i-1][j]
    			else:
    				costMatrix[i][j] = max(costMatrix[i-1][j],scores[i] +costMatrix[i-1][j-heights[i]])
    	return self.getCheck(heights,costMatrix)

class Answer(object):
    def __init__(self, answer):
        self.score, self.numberOfStories, self.idList = answer
    def __str__(self):
        s = str(self.score)
        s += " "+str(self.numberOfStories)
        for k in self.idList:
            s+=" "+str(k)
        return s

if __name__=="__main__":
    N, W, H = [int(k) for k in raw_input().strip().split()]
    # instantiate feed optimizing object
    feedOptimizer = StoryTeller(W, H)
    for i in range(N):
        event = [c for c in raw_input().strip().split()]
        if(event):
            # act according to the type of the event
            eventType = event[0]
            if(eventType=='S'):
                # store time, score and height of the story event
                time, score, height = [int(k) for k in event[1:]]
                # update current time
                feedOptimizer.addStory(time, score, height)
            if(eventType=='R'):
                # get the time of the reload event
                time = int(event[1])
                # output answer to stdout
                print Answer(feedOptimizer.getAnswer(time))
