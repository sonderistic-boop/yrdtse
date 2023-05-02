#make game class, with a run method, and a main method
#game should be 810x770
#game will have a stadium, a ball, and two teams
#game will have a run method, which will run the game
#game 
import pygame as pg
import math
import sys


import gameMultiplayer.logic.physics as physics
import gameMultiplayer.logic.collisions as col
from gameMultiplayer.entities.pawn import Pawn
from gameMultiplayer.entities.ball import Ball
import gameMultiplayer.entities.stadium.stadiums as stadiums


class Game():
    def __init__(self,players,time,maxScore,stadium):

        pg.init()
        
        #declares the parent screen, which is the screen that the game surface will be drawn on
        #declares which stadium the game will be played on
        self.stadium = stadium
        self.gameState = "gameStart"
        self.gameState = "game"

        #numerous game states, "gameStart","game","goalScored","gameEnd"
        self.gameTimerEvent = pg.USEREVENT+1
        self.goalTimerEvent = pg.USEREVENT+2
        self.gameEndTimerEvent = pg.USEREVENT+3
        self.gameTimer = pg.time.set_timer(self.gameTimerEvent,1000)

        #declares how long the game will last
        self.time = time
        #declares the maximum score the game will be played to
        self.maxScore = maxScore

        self.colours = {
            "team1" : "red",
            "team2" : "blue"
            }

        self.team1= {}
        self.team2 = {}

        self.team1Score = 0
        self.team2Score = 0

        
        
        
        #load game surface, load players, load ball, load stadium
        

        self.screen = pg.Surface((1600,950),pg.SRCALPHA)

        
        
        self.stadiumType = getattr(stadiums,stadium)
        #put stadium in the middle of the screen
        self.stadium = self.stadiumType(self.screen,(100,100),[self.colours["team1"],self.colours["team2"]])
        self.stadiumSize = (self.screen.get_width()//2-((self.stadium.bounds["x2"]-self.stadium.bounds["x1"])//2),self.screen.get_height()//2-((self.stadium.bounds["y2"]-self.stadium.bounds["y1"])//2))
        self.stadium = None
        self.stadium = self.stadiumType(self.screen,self.stadiumSize,[self.colours["team1"],self.colours["team2"]])
    
        
        
        self.ball = Ball(self.screen,(self.stadium.bounds["middle"][0],self.stadium.bounds["middle"][1]),(30,30))
        
        #load players, and add them to the left and right team dictionaries. initial position will be the middle-left of the stadium for the left team, and the middle-right of the stadium for the right team
        for index,player in enumerate(players["team1"]):
            self.team1[player] = Pawn(player,self.colours["team1"],False,self.screen,
                                      (self.stadium.bounds["x1"]+200,(self.stadium.bounds["y1"]+30)+(index*75)),
                                      (70.3,70.3))

            #set the initial position of the player to the middle-left of the stadium, depending on the number of players on the team and the size of the stadium starting from the middle



            #self.team1[i] = Pawn(i,self.colours["team1"],False,self.screen,(),(70.3,70.3))          
        
        for index,player in enumerate(players["team2"]):
            self.team2[player] = Pawn(player,self.colours["team2"],False,self.screen,
                                      (self.stadium.bounds["x2"]-200,(self.stadium.bounds["y1"]+30)+(index*75)),
                                      (70.3,70.3))

            #set the initial position of the player to the middle-right of the stadium, depending on the number of players on the team and the size of the stadium starting from the middle

            #self.team2[i] = Pawn(i,self.colours["team2"],False,self.screen,(),(70.3,70.3)) 

        
        
        
        #add sprite groups for ball, players, stadium parts

        #self.ballGroup = pg.sprite.GroupSingle(self.ball)


        self.playerGroup = pg.sprite.Group()
        self.playerGroup.add(self.team1.values())
        self.playerGroup.add(self.team2.values())


        self.stadiumBoundsGroup = pg.sprite.Group()
        self.stadiumBoundsGroup.add(self.stadium.lines.values())
        self.stadiumBoundsGroup.add(self.stadium.collidingGoals.values())

        self.stadiumGoalGroup = pg.sprite.Group()
        self.stadiumGoalGroup.add(self.stadium.goals.values())



    def main(self):
        #check for collisions, check for goals, check for time, check for score
        #update the ball, update the players
        #render the stadium, render the ball, render the players
        
        for event in pg.event.get():
            if event.type == self.gameTimerEvent:
                if self.gameState == "game":
                    self.time -= 1
                if self.time == 0:
                    self.gameEnd()
                    pg.time.set_timer(self.gameTimerEvent,0)
            if event.type == self.goalTimerEvent:
                pg.time.set_timer(self.goalTimerEvent,0)
                self.reset()
                self.gameState = "game"
                
                
            if event.type == self.gameEndTimerEvent:
                pg.time.set_timer(self.gameEndTimerEvent,0)
                return "gameOver"
        self.collisionChecker()
        self.updatePhysics()
        self.render()
           


    def render(self):
        #draw the stadium, draw the ball, draw the players
        self.stadium.render()
        for i in self.playerGroup:
            i.render()
        self.ball.render()
        
        
        

    def updatePhysics(self):
        #update the ball, update the players
        self.ball.updatePhysics()
        for i in self.playerGroup:
            i.updatePhysics()
        
    
    def collisionChecker(self):
        #check for collisions between the ball and the players, and the ball and the stadium
        #check for collisions between the players and the stadium
        #check for collisions between the players and the other players
        #check for collisions between the ball and the goals
        #check for collisions between the players and the goals
        

        #check for collisions between the ball and the players
        ballPlayerCollisions = pg.sprite.spritecollide(self.ball,self.playerGroup,False,pg.sprite.collide_mask)

        ballStadiumCollisions = pg.sprite.spritecollide(self.ball,self.stadiumBoundsGroup,False,pg.sprite.collide_mask)

        ballGoalCollisions = pg.sprite.spritecollide(self.ball,self.stadiumGoalGroup,False,pg.sprite.collide_mask)

        playerStadiumCollisions = pg.sprite.groupcollide(self.playerGroup,self.stadiumBoundsGroup,False,pg.sprite.collide_mask)

        playerPlayerCollisions = pg.sprite.groupcollide(self.playerGroup,self.playerGroup,False,False,pg.sprite.collide_mask)

        

        for i in ballGoalCollisions:
            if self.gameState == "game":
                self.goalScored(i)


        
        self.wallCollision(self.ball,self.stadium)
            
        
        for i in ballPlayerCollisions:
            
            if i.kicking:
                i.kicking = False
                physics.thrust(self.ball,i)
            else:
                physics.objectCollision(self.ball,i)
            
        
        for i in playerPlayerCollisions:
            for j in playerPlayerCollisions[i]:
                if i != j:
                    physics.objectCollision(i,j)
                

        
    """  
        for i in playerStadiumCollisions:
            for j in playerStadiumCollisions[i]:
                physics.objectCollision(i,j)
        
        
        """
        
        
        
    

    def wallCollision(self,ball,stadium):
        # if the ball collides with the stadium, bounce it off the stadium
        
        restitution = lambda a : a* 0.8
        
        if ball.position[0] < stadium.bounds["x1"] and (ball.position[1] < stadium.bounds["y3"] or ball.position[1] + ball.h > stadium.bounds["y4"]):
            ball.position[0] = stadium.bounds["x1"]
            ball.velocity[0] *= -1
            ball.velocity = restitution(ball.velocity)
            
            
        elif ball.position[0]+ball.w > stadium.bounds["x2"] and (ball.position[1] < stadium.bounds["y3"] or ball.position[1] + ball.h > stadium.bounds["y4"]):
            ball.position[0] = stadium.bounds["x2"] - ball.w
            ball.velocity[0] *= -1
            ball.velocity = restitution(ball.velocity)
            
        elif ball.position[1] < stadium.bounds["y1"]:
            ball.position[1] = stadium.bounds["y1"]
            ball.velocity[1] *= -1
            ball.velocity = restitution(ball.velocity)
            
        elif ball.position[1] + ball.h > stadium.bounds["y2"]:
            ball.position[1] = stadium.bounds["y2"] - ball.h
            ball.velocity[1] *= -1
            ball.velocity = restitution(ball.velocity)
            
        elif ball.position[0] < stadium.bounds["x1"] - 79:
            ball.velocity[0] *= -1
            ball.velocity = restitution(ball.velocity)
            
        elif ball.position[0] + ball.w > stadium.bounds["x2"] + 79:
            
            ball.velocity[0] *= -1
            ball.velocity = restitution(ball.velocity)
            
        elif ball.position[1] < stadium.bounds["y3"] and (ball.position[0] < stadium.bounds["x1"] or ball.position[1] + ball.w > stadium.bounds["x2"]):
            
            ball.velocity[1] *= -1
            ball.velocity = restitution(ball.velocity)
            
        elif (ball.position[1] + ball.h > stadium.bounds["y4"]) and (ball.position[0] < stadium.bounds["x1"] or ball.position[1] + ball.w > stadium.bounds["x2"]):
            
            ball.velocity[1] *= -1
            ball.velocity = restitution(ball.velocity)
        
#SOME REASON COLLISIONS WITH THE X2 GOAL AREN'T WORKING AS INTENDED, FIX THIS
        

        

    def goalScored(self,goal):
        
        if goal.team == self.colours["team1"]:
            self.team2Score += 1
            if self.team2Score == self.maxScore:
                self.gameEnd()
            else:
                self.gameState = "goalScoredTeam2"
        elif goal.team == self.colours["team2"]:
            self.team1Score += 1
            if self.team1Score == self.maxScore:
                self.gameEnd()
            else:
                self.gameState = "goalScoredTeam1"

        print("goal scored")
        
        pg.time.set_timer(self.goalTimerEvent,5000)

    def gameEnd(self):
        if self.team1Score > self.team2Score:
            self.gameState = "gameEndTeam1"
        elif self.team1Score < self.team2Score:
            self.gameState = "gameEndTeam2"
        else:
            self.gameState = "gameEndDraw"
        pg.time.set_timer(self.gameEndTimerEvent,5000)

    def reset(self):
        self.ball.reset()
        for i in self.playerGroup:
            i.reset()

    def getData(self):
        data = {
            "gameState" : self.gameState,
            "ball" : self.ball.getData(),
            "players" : {
                "team1" : {},
                "team2" : {}
                },
            "score" : {
                "team1" : self.team1Score,
                "team2" : self.team2Score
                },
            "timeRemaining" : self.time
            }

        for i in self.team1:
            data["players"]["team1"][i] = self.team1[i].getData()
        for i in self.team2:
            data["players"]["team2"][i] = self.team2[i].getData()

        return data
    
    def updatePlayer(self,username,ReceivingClientData):
        if username in self.team1:
            self.team1[username].update(ReceivingClientData)
        elif username in self.team2:
            self.team2[username].update(ReceivingClientData)

    

    




        
        

        
    
