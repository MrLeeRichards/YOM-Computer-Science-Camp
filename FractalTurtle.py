from turtle import *

def fractalTurns(pattern, iterations, turnList = []):
   if iterations <= 1:
      return turnList
   else:
      newTurnList = [] + turnList
      for turn in pattern:
         newTurnList += [turn] + turnList
      return fractalTurns(pattern, iterations - 1, newTurnList)

pattern = []

nextAngle = input("Angle (x to end): ")
while nextAngle != 'x':
   pattern.append(int(nextAngle))
   nextAngle = input("Angle (x to end): ")

iterations = int(input("iterations: ")) + 1
speed = max(1000 / ((len(pattern) + 1) ** (iterations + 1)), 1)

turns = fractalTurns(pattern, iterations)

delay(0)
pendown()
pencolor("white")
bgcolor("black")
for turn in turns:
   forward(int(speed))
   right(turn)
forward(int(speed))

done()