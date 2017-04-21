'''
Lea Gould & ZiYang Gaoz
CS111 Winter 2017
3/15/2017

This is a battleship game that is text-based and should be 
launched and played in terminal. It is a module which contains a Computer class, 
a Battleship_text class and a battleship_game class.
They are called in main function to start the actual game with the play method.
'''

import random
import pprint

class Computer:
    
    def __init__(self, a_difficulty):
        self.difficulty = a_difficulty
        self.bigship = None
        self.accumulated_target = []
        self.guess_list = []

    def get_compcoord(self, bigship):
        '''
        Generating random numbers for coordinates for computer's 4 ships depending on
        level of difficulty. Generating 2nd coordinate for second half of ship.
        '''
        bigship = []
        for i in range(4):
            fault = 17
            while fault >= 16:
                if self.difficulty == 5:
                    x_value = random.randint(2,4)
                    y_value = random.randint(2,4)
                elif self.difficulty == 7:
                    x_value = random.randint(2,6)
                    y_value = random.randint(2,6)
                elif self.difficulty == 10:
                    x_value = random.randint(2,9)
                    y_value = random.randint(2,9)

                base = [x_value, y_value]
                generate = [[x_value + 1, y_value], [x_value, y_value - 1],
                            [x_value, y_value + 1], [x_value - 1, y_value]]

                choose = random.randint(0,3)
                generate = generate[choose]

                if base not in bigship and generate not in bigship:
                    bigship.append(base)
                    bigship.append(generate)
                    fault = 15
                else:
                    fault = 17
        
        self.bigship = bigship

        return bigship

    def get_randguess(self, combine):
        '''
        Generating random numbers as coordinates as a guess.
        Takes in list of user ship coordinates as a parameter to compare 
        list of computer guessed coordinates to user's actual ship coordinates.
        '''
        target = []
        another_round = 17
        while another_round >= 16:
            if self.difficulty == 5:
                x_target = random.randint(1,5)
                y_target = random.randint(1,5)
                target = [x_target, y_target]
            elif self.difficulty == 5:
                x_target = random.randint(1,7)
                y_target = random.randint(1,7)
                target = [x_target, y_target]
            elif self.difficulty == 10:
                x_target = random.randint(1,10)
                y_target = random.randint(1,10)
                target = [x_target, y_target]
            
            while target in self.guess_list:
                if self.difficulty == 5:
                    x_target = random.randint(1,5)
                    y_target = random.randint(1,5)
                    target = [x_target, y_target]
                elif self.difficulty == 7:
                    x_target = random.randint(1,7)
                    y_target = random.randint(1,7)
                    target = [x_target, y_target]
                elif self.difficulty == 10:
                    x_target = random.randint(1,10)
                    y_target = random.randint(1,10)
                    target = [x_target, y_target]
                
            self.guess_list.append(target)
            print("Computer guess:", target)
            print(combine)
            if target in combine and target not in self.accumulated_target:
                self.accumulated_target.append(target)
                print("Oh No! The computer has hit your ship! And he gets another turn! ")
                target1 = self.get_calcguess(x_target,y_target)
                print(target1)
                if target1 in combine and target1 not in self.accumulated_target:
                    print("He hits you again and he's gettin another turn! ")
                    self.accumulated_target.append(target1)
                    self.guess_list.append(target1)
                    another_round = 17
                else:
                    print("Yay! The computer missed your ship! Now it's your turn! ")
                    another_round = 15
            else:
                print("Yay! The computer missed your ship! Now it's your turn! ")
                another_round = 15
        self.accumulated_target.sort()
        return self.accumulated_target

    def get_calcguess(self, x_target, y_target):
        '''
        Called into get_randguess method after a correct guess has been made 
        to make a calculated guess about the second half of the ship's 
        coordinates, either left, right, up or down.
        '''
        if x_target == 0:
            calculate = [[x_target + 1, y_target], [x_target, y_target - 1],
                  [x_target, y_target + 1]]
        elif y_target == 0:
            calculate = [[x_target + 1, y_target],
                  [x_target, y_target + 1], [x_target - 1, y_target]]
        else:
            calculate = [[x_target + 1, y_target], [x_target, y_target - 1],
                  [x_target, y_target + 1], [x_target - 1, y_target]]
        numchoose = random.randint(0,3)
        target1 = calculate[numchoose]
        return target1


class BattleshipGame:
    def __init__(self, a_difficulty):
        self.difficulty = a_difficulty
        self.battleship_txt = BattleshipText(a_difficulty, 4)
        self.computer = Computer(a_difficulty)
        

    def play(self):
        '''
        Launching the game by calling in methods from computer and 
        battleship_text class in order of inputting ship coordinates and then guessing 
        opponent's coordinates. Taking lists from each class to compare 
        guessed coordinates and original coordinates and finishes the game if all have 
        been guessed.
        '''
        list1 = self.battleship_txt.get_coord(self.battleship_txt.combine)
        list1.sort()
        list2 = self.computer.get_compcoord(self.computer.bigship)
        print("The computer has chosen its ships' coordinates")
        list2.sort()
        list3 = self.battleship_txt.get_target_coord(self.computer.bigship)
        list3.sort()
        list4 = self.computer.get_randguess(self.battleship_txt.combine)
        list4.sort()
        while list1 != list4 and list2 != list3:
            print("Next Turn: ")
            print("Your coords:", list1)
            print("You hit computer at:  ", list3)
            print("Computer hits you at: ", list4)
            self.battleship_txt.get_target_coord(self.computer.bigship)
            self.computer.get_randguess(self.battleship_txt.combine)
        if list1 == list4:
            print("Sorry the computer wins! ")
        elif list2 == list3:
            print("You beat the computer! ")
        else:
            print("Something just went terribly wrong! ")


class BattleshipText:

    def __init__(self, a_difficulty, a_numship = 4):
        self.numship = a_numship
        self.difficulty = a_difficulty
        self.combine = None
        self.guessed = []
        self.accumulated_target_user = []
        self.matrix = [[0 for i in range(a_difficulty)] for j in range(a_difficulty)]


    def get_coord(self, combine):
        '''
        Getting input coordinates from user to place ships depending on difficulty
        and number of ships they want to use. Calling two sets of coordinates
        into a list and making sure that they are next to each other, otherwise
        game starts over.
        '''

        coord = []
        combine = []
        for i in range (4):
            fault = 17
            while fault >= 16:

                if self.difficulty == 5:
                    limit = 3
                    while limit > 2:
                        x_value_str1 = input("Please insert your first grid value for x between 1-5: ")
                        x_value1 = int(x_value_str1)
                        y_value_str1 = input("Please insert your first grid value for y between 1-5: ")
                        y_value1 = int(y_value_str1)
                        x_value_str2 = input("Please insert your second grid value for x between 1-5: ")          
                        x_value2 = int(x_value_str2)
                        y_value_str2 = input("Please insert your second grid value for y between 1-5: ")
                        y_value2 = int(y_value_str2)
                        if x_value1 not in range (1, 6) or y_value1 not in range (1, 6) or x_value2                                                     not in range (1, 6) or y_value2 not in range (1, 6):
                            print("Wrong range! Please notice the range limit and input again! ")
                            limit = 3
                        elif (x_value1 != x_value2 or abs(y_value1 - y_value2) != 1) and (y_value1                                                           != y_value2 or abs(x_value1 - x_value2) != 1):
                            print("Notice the coords should be connected! Input again please! ")
                            limit = 3
                        else:
                            limit = 1



                elif self.difficulty == 7:
                    limit = 3
                    while limit > 2:
                        x_value_str1 = input("Please insert your first grid value for x between 1-7: ")
                        x_value1 = int(x_value_str1)
                        y_value_str1 = input("Please insert your first grid value for y between 1-7: ")
                        y_value1 = int(y_value_str1)
                        x_value_str2 = input("Please insert your second grid value for x between 1-7: ")          
                        x_value2 = int(x_value_str2)
                        y_value_str2 = input("Please insert your second grid value for y between 1-7: ")
                        y_value2 = int(y_value_str2)
                        if x_value1 not in range (1, 8) or y_value1 not in range (1, 8)                                                                 or x_value2 not in range (1, 8) or y_value2 not in range (1, 8):                       
                            print("Wrong range! Please notice the range limit and input again! ")
                            limit = 3
                        elif (x_value1 != x_value2 or abs(y_value1 - y_value2) != 1) and (y_value1 != y_value2                                         or abs(x_value1 - x_value2) != 1):
                            print("Notice the coords should be connected! Input again please! ")
                            limit = 3
                        else:
                            limit = 1
                        

                elif self.difficulty == 10:
                    limit = 3
                    while limit > 2:
                        x_value_str1 = input("Please insert your first grid value for x between 1-10: ")
                        x_value1 = int(x_value_str1)
                        y_value_str1 = input("Please insert your first grid value for y between 1-10: ")
                        y_value1 = int(y_value_str1)
                        x_value_str2 = input("Please insert your second grid value for x between 1-10: ")         
                        x_value2 = int(x_value_str2)
                        y_value_str2 = input("Please insert your second grid value for y between 1-10: ")
                        y_value2 = int(y_value_str2)
                        if x_value1 not in range (1, 11) or y_value1 not in range (1, 11) or x_value2                                                   not in range (1, 11) or y_value2 not in range (1, 11):
                            print("Wrong range! Please notice the range limit and input again! ")
                            limit = 3
                        elif (x_value1 != x_value2 or abs(y_value1 - y_value2) != 1) and                                                               (y_value1 != y_value2 or abs(x_value1 - x_value2) != 1):
                            print("Notice the coords should be connected! Input again please! ")
                            limit = 3
                        else:
                            limit = 1
                            
                coord_one = [x_value1, y_value1]
                coord_two = [x_value2, y_value2]
                combine.append(coord_one)
                combine.append(coord_two)
                fault = 15

        self.combine = combine
        print(combine)
        return combine


    def get_target_coord(self, bigship):
        '''
        Getting input from user to make target guess of computer ship coordinates, 
        making sure that the input is in range of the grid size. Showing the coordinates
        that they input on a matrix and using 1 to show that they hit target,
        and 2 to show that they missed. Accumulating guessed coordinates to a list 
        to be used and saved to the matrix to show user where they've already guessed.
        '''
        target = []
    
        if self.difficulty == 5:
            x_target = 15
            y_target = 15
            while x_target not in range (1, 6) or y_target not in range (1, 6):
                print("Make sure to put values within correct range! ")
                x_target = input("Please guess x_value: ")
                x_target = int(x_target)
                y_target = input("Please guess y_value: ")
                y_target = int(y_target)
                target = [x_target, y_target]
                #self.guessed.append(target)
                if target in bigship and target not in self.accumulated_target_user:
                    self.accumulated_target_user.append(target)
                    self.matrix[x_target-1][y_target-1] = 1
                    pprint.pprint(self.matrix) 
                    print("Hooray! You hit your opponent's ship! Go for another turn! ")
                    x_target = 10
                
            else:
                self.matrix[x_target-1][y_target-1] = 2
                pprint.pprint(self.matrix) 
                print("Sorry you didn't hit another ship! Now it's the computer's turn! ")
                x_target = 1
                
        
        elif self.difficulty == 7:
            x_target = 15
            y_target = 15    
            while x_target not in range (1, 8) or y_target not in range (1, 8):
                print("Make sure to put values within correct range! ")
                x_target = input("Please guess x_value: ")
                x_target = int(x_target)
                y_target = input("Please guess y_value: ")
                y_target = int(y_target)
                target = [x_target, y_target]
                #self.guess_list.append(target)
                if target in bigship and target not in self.accumulated_target_user:
                    self.accumulated_target_user.append(target)
                    self.matrix[x_target-1][y_target-1] = 1
                    pprint.pprint(self.matrix) 
                    print("Hooray! You hit your opponent's ship! Go for another turn! ")
                    x_target = 10
            else:
                self.matrix[x_target-1][y_target-1] = 2
                pprint.pprint(self.matrix) 
                print("Sorry you didn't hit another ship! Now it's the computer's turn! ")
                x_target = 1
        
        elif self.difficulty == 10:
            x_target = 15
            y_target = 15    
            while x_target not in range (1, 11) or y_target not in range (1, 11):
                print("Make sure to put values within correct range! ")
                x_target = input("Please guess x_value: ")
                x_target = int(x_target)
                y_target = input("Please guess y_value: ")
                y_target = int(y_target)
                target = [x_target, y_target]
                #self.guess.append(target)
                if target in bigship and target not in self.accumulated_target_user:
                    self.accumulated_target_user.append(target)
                    self.matrix[x_target-1][y_target-1] = 1
                    pprint.pprint(self.matrix) 
                    print("Hooray! You hit your opponent's ship! Go for another turn! ")
                    x_target = 13
            else:
                self.matrix[x_target-1][y_target-1] = 2
                pprint.pprint(self.matrix) 
                print("Sorry you didn't hit another ship! Now it's the computer's turn! ")
                x_target = 1

            
        self.accumulated_target_user.sort()
        self.matrix
        
        return self.accumulated_target_user
        return self.matrix
    

def main():
    '''
    Printing instruction, asking user for input on difficulty level and calling in 
    Battleship-game class to call in play method and launch the battleship game.
    '''
    print("Welcome to Battleship! ")
    strr = str("Instructions: 1. Choose a difficulty level depending on how big you ")
    strr += str("want the battelship grid to be, a difficulty level of 5 being a 5 by 5 grid,")
    strr += str("a difficulty level of 10 being a 7 by 7 grid, ")
    strr += str(" a difficulty level of 7 being a 10 by 10 grid.")
    print(strr)
    
    strr = str("              2. Then you will have to input coordinates for 4 ships, ")
    strr += str("which are all of length 2. Make sure that a ship should have two ")
    strr += str("connecting coordinates. For example: (1,4), (1,3) or (3,5), (2,5).")
    print(strr)

    strr = str("              3. After the computer has chosen its coordinates, ")
    strr += str("you will be asked to insert an x and y value to guess the computer's ships' ")
    strr += str("coordinates. If you guess right, a matrix will print out showing 1 ")
    strr += str("as a correct target, and you will be able to guess again and input a second x ")
    strr += str("and y value. If you guess wrong, a matrix will print out showing 2")
    strr += str("as a missed target and the computer will take its turn. The computer, similarly")
    strr += str("will guess again if it guesses a coorect target.")
    print(strr)
    
    strr = str("              Once all coordinates have been guessed, either by you the user, ")
    strr += str("or by the computer, the game will end. Good Luck and have fun! ")    
    
              
    difficulty = input("Choose a difficulty level from 5, 7 and 10: ")
    difficulty = int(difficulty)  
    while difficulty != 5 and difficulty != 7 and difficulty != 10:
        print("Difficulty level out of range! Please choose a difficulty level from 5, 7 and 10")   
        difficulty = input("Choose a difficulty level from 5, 7 and 10: ")
        difficulty = int(difficulty) 

    game = BattleshipGame(difficulty)
    
    game.play()


if __name__ == '__main__':
    main()