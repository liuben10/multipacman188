# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util, sys, search, searchAgents

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]
    
    def getMin(self, pos, List):
        return min([util.manhattanDistance(pos, posIter) for posIter in List])
    
#    def evaluationFunction(self, currentGameState, action):
#        """
#        Design a better evaluation function here.
#
#        The evaluation function takes in the current and proposed successor
#        GameStates (pacman.py) and returns a number, where higher numbers are better.
#
#        The code below extracts some useful information from the state, like the
#        remaining food (newFood) and Pacman position after moving (newPos).
#        newScaredTimes holds the number of moves that each ghost will remain
#        scared because of Pacman having eaten a power pellet.
#
#        Print out these variables to see what you're getting, then combine them
#        to create a masterful evaluation function.
#        """
#        # Useful information you can extract from a GameState (pacman.py)
#        successorGameState = currentGameState.generatePacmanSuccessor(action)
#        newPos = successorGameState.getPacmanPosition()
#        newFood = successorGameState.getFood()
#        newGhostStates = successorGameState.getGhostStates()
#        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
#
#        minGhostDistance = self.minGhostDistance(newPos, newGhostStates)
#        score = successorGameState.getScore()
#        surroundingFood = self.surroundingFood(newPos, newFood)
#        avgFoodDistance = self.avgFoodDistance(newPos, newFood)
#        return 2.0/minGhostDistance + score + surroundingFood + 10.0/avgFoodDistance
#
#    def avgFoodDistance(self, newPos, newFood):
#        distances = []
#        for x, row in enumerate(newFood):
#            for y, column in enumerate(newFood[x]):
#                if newFood[x][y]:
#                    distances.append(manhattanDistance(newPos, (x,y)))
#        avgDistance = sum(distances)/float(len(distances)) if (distances and sum(distances) != 0) else 1
#        return avgDistance
#
#    def surroundingFood(self, newPos, newFood):
#        count = 0
#        for x in range(newPos[0]-2, newPos[0]+3):
#            for y in range(newPos[1]-2, newPos[1]+3):
#                if (0 <= x and x < len(list(newFood))) and (0 <= y and y < len(list(newFood[1]))) and newFood[x][y]:
#                    count += 1
#        return count
#
#    def minGhostDistance(self, newPos, newGhostStates):
#        distances = []
#        for ghostState in newGhostStates:
#            ghostCoordinate = ghostState.getPosition()
#            distances.append(manhattanDistance(newPos, ghostCoordinate))
#        if distances and min(distances) != 0:
#            return min(distances)
#        return 1
    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        if successorGameState.isWin() :   return 5555 
        if successorGameState.isLose() :  return -5555
        
        newPos = successorGameState.getPacmanPosition()
        oldFood = currentGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        #print '\nnewPos '+str(newPos)
        #print 'oldFood '+str(oldFood.asList())
        #print "score %d" % successorGameState.getScore()
        closestCapsule = 0
        "obtain food score"
        newFood = successorGameState.getFood()
        newfoodList = newFood.asList()
        closestFood = self.getMin(newPos, newfoodList)
        foodScore = 80 / closestFood
        
        
        "obtain capsuleScore"
        capsuleList = successorGameState.getCapsules()
        closestCapsule = self.getMin(newPos, capsuleList) if capsuleList else 0
        capsuleScore = 80/closestCapsule if capsuleList else 0
        #print "capScore: ", capsuleScore
        totalScaredTime = sum(newScaredTimes)
        "obtain ghost score"
        closestGhost = 1
        ghostPositions = [ghostState.getPosition() for ghostState in newGhostStates if ghostState.scaredTimer == 0]
        ghostScore = 1
        if ghostPositions:
            closestGhost = self.getMin(newPos, ghostPositions)
            if closestGhost <= 1 and totalScaredTime == 0:
                return -200
            elif closestGhost <= 1 and totalScaredTime > 0:
                print "Hello"
                return 5555
        else:
            return 5555
        ghostScore = 10.0 * closestGhost
        "a new evaluation function."
        heuristic = successorGameState.getScore() + (foodScore + capsuleScore) / ghostScore + totalScaredTime
        #print heuristic
        return heuristic

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        self.state = 'min'

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
        
    #    def Value(self, depth, agent, state):
    #        if depth == self.depth:
    #            return self.evaluationFunction(state)
    #        else:
    #            actions = state.getLegalActions(agent)
    #            if len(actions) > 0:
    #                if self.state == 'min':
    #                    v = float("inf")
    #                else:
    #                    v = float("-inf")
    #            else:
    #                v = self.evaluationFunction(state)
    #            for action in actions:
    #                if self.state == 'max':
    ##                    print "MAXVALUE"
    ##                    print "agent: ", agent
    #                    agent = 0
    #                    self.state = 'min'
    #                    print "SWITCHING TO MIN"
    #                    score = self.Value(depth, agent+1, state.generateSuccessor(agent, action))
    #                    if score > v:
    #                        v = score
    #                else:
    ##                    print "MINVALUE"
    ##                    print "numAgents:" , state.getNumAgents()
    ##                    print "agent: ", agent
    #                    if agent == state.getNumAgents()-1 and self.state == 'min':
    #                        print "SWITCHING TO MAX"
    #                        self.state = 'max'
    #                        agent = 0
    #                        score = self.Value(depth+1, agent, state.generateSuccessor(agent, action))
    #                        if score < v:
    #                            v = score
    #                    else:
    #                        self.state = 'min'
    #                        score = self.Value(depth, agent+1, state.generateSuccessor(agent, action))
    #                        if score < v:
    #                            v = score
    #            return v
    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        v = float('-inf')
        nextAction = Directions.STOP
        for action in gameState.getLegalActions(0):
                temp = self.minValue(0, 1, gameState.generateSuccessor(0, action))
                if temp > v and action != Directions.STOP:
                        v = temp
                        nextAction = action
        return nextAction
        util.raiseNotDefined()

    def maxValue(self, depth, agent, state):
                if depth == self.depth:
                        return self.evaluationFunction(state)
                else:
                        actions = state.getLegalActions(agent)
                        if len(actions) > 0:
                                v = float('-inf')
                        else:
                                v = self.evaluationFunction(state)
                        for action in actions:
                                s = self.minValue(depth, agent+1, state.generateSuccessor(agent, action))
                                if s > v:
                                        v = s
                        return v
 
    def minValue(self, depth, agent, state):
                if depth == self.depth:
                        return self.evaluationFunction(state)
                else:
                        actions = state.getLegalActions(agent)
                        if len(actions) > 0:
                                v = float('inf')
                        else:
                                v = self.evaluationFunction(state)
 
                        for action in actions:
                                if agent == state.getNumAgents() - 1:
                                        s = self.maxValue(depth+1, 0, state.generateSuccessor(agent, action))
                                        if s < v:
                                                v = s
                                else:
                                        s = self.minValue(depth, agent+1, state.generateSuccessor(agent, action))
                                        if s < v:
                                                v = s
                        return v
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        v = float('-inf')
        nextAction = Directions.STOP
        alpha = float('-inf')
        beta = float('inf')
        for action in gameState.getLegalActions(0):
                if v > beta:
                    continue
                alpha = max(v, alpha)
                temp = self.minValue(-1, 1, gameState.generateSuccessor(0, action), alpha , beta)
                if temp > v and action != Directions.STOP:
                        v = temp
                        nextAction = action
        if 'getLegalPacmanActions' in dir(gameState):
            print nextAction
        if nextAction == Directions.NORTH:
            print "++++++++++++++++"
            print "alpha: " , alpha
            print "beta: " , beta
            print "depth: " , self.depth
            print "V: " , v
            
            
            print "++++++++++++++++"
        return nextAction
        util.raiseNotDefined()
        
    def maxValue(self, depth, agent, state, alpha, beta):
                if depth == self.depth:
                        return self.evaluationFunction(state)
                else:
                        actions = state.getLegalActions(agent)
                        if len(actions) > 0:
                                v = float('-inf')
                        else:
                                v = self.evaluationFunction(state)
                        for action in actions:
                                v = max(v, self.minValue(depth, agent+1, state.generateSuccessor(agent, action), alpha, beta))
                                if v > beta:
                                        return v
                                alpha = max(v, alpha)
                        return v
                    
    def minValue(self, depth, agent, state, alpha, beta):
                if depth == self.depth:
                        return self.evaluationFunction(state)
                else:
                        actions = state.getLegalActions(agent)
                        if len(actions) > 0:
                                v = float('inf')
                        else:
                                v = self.evaluationFunction(state)
                               
                        for action in actions:
                                if agent == state.getNumAgents() - 1:
                                        v = min(v, self.maxValue(depth+1, 0, state.generateSuccessor(agent, action), alpha, beta))
                                        if v < alpha:
                                                return v
                                        beta = min(v, beta)
                                else:
                                        v = min(v, self.minValue(depth, agent+1, state.generateSuccessor(agent, action), alpha, beta))
                                        if v < alpha:
                                                return v
                                        beta = min(v, beta)
                        return v

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        v = float('-inf')
        nextAction = Directions.STOP
        for action in gameState.getLegalActions(0):
                temp = self.minValue(0, 1, gameState.generateSuccessor(0, action))
                if temp > v and action != Directions.STOP:
                        v = temp
                        nextAction = action
        return nextAction
        util.raiseNotDefined()
        
        
    def maxValue(self, depth, agent, state):
                if depth == self.depth:
                        return self.evaluationFunction(state)
                else:
                        actions = state.getLegalActions(agent)
                        if len(actions) > 0:
                                v = float('-inf')
                        else:
                                v = self.evaluationFunction(state)
                        for action in actions:
                                score = self.minValue(depth, agent+1, state.generateSuccessor(agent, action))
                                if score > v:
                                    v = score
                        return v
                    
    def minValue(self, depth, agent, state):
                if depth == self.depth:
                        return self.evaluationFunction(state)
                else:
                        v = 0
                        actions = state.getLegalActions(agent)
                        actionLength = len(actions)
                        for action in actions:
                                if agent == state.getNumAgents() - 1:
                                        v += float(self.maxValue(depth+1, 0, state.generateSuccessor(agent, action))) / actionLength
                                else:
                                        v += float(self.minValue(depth, agent+1, state.generateSuccessor(agent, action))) / actionLength
                        return v

def betterEvaluationFunction(currentGameState):
        """
          Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
          evaluation function (question 5).
    
          DESCRIPTION: <write something here so we know what you did>
        """
        "*** YOUR CODE HERE ***"
        newPos = currentGameState.getPacmanPosition()
        newFood = currentGameState.getFood()
        newGhostStates = currentGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
 
        if currentGameState.isLose(): 
            return -5555
        if currentGameState.isWin(): 
            return 5555
        score = 0.0
        

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

