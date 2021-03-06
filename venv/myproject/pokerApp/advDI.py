import os

import psycopg2 as psycopg2
from contextlib import closing
from django.db import connection
from django.utils import timezone
import psycopg2

# from django.db import models
# from pokerApp.models import *

#conn = psycopg2.connect("host=localhost dbname=poker user=hani password=hanihani1 ")
#cur = conn.cursor()
#def insert_game():
#    Game.objects.create(number_of_hands=10, game_type="Springsteen",duration= "long")
#cur.execute("INSERT INTO pokerApp_game VALUES (%s, %s, %s)", ('1', 'hello', 'long'))
#conn.commit()
#insert_game()

# for p in Game.objects.raw('SELECT * FROM myapp_person'):
#     print (p)

newFile = open("/home/syed/Documents/AdvDI/Hands1/Part1/HH20170728 Alamak - $0.01-$0.02 - USD No Limit Hold'em.txt",
               'r')
with newFile as myfile:
    # for line in myfile:
    data = myfile.read()

def countNumberOfHands(freshData, listy,filename):
    countOfHands = 0
    #newData = One Hand
    newData = freshData.split("\n\n\n")
    positions = []
    lineNo = 0
    line = 0
    Hands1 = {}

    Hands1["tableID"] = filename
    Hands1["game_name"] = filename.split('-')[0]
    Hands1["game_type"] = filename.split('-')[-1].split('.txt')[0]

    notes = []
    moves = []
    phase = ""
    hand = []
    test = []
    meow = []
    for i in newData:
        hand = i.split("\n")
        #Limiting hands data
        #if lineNo <5:
        #print (hand)
        moves = []
        positions = []
        listy = {}
        preflop = flop = turn = river = False
        if hand[0] == "" and hand[1] != "":
            for i in range(len(hand)):

                    if "*** HOLE CARDS ***" in hand[i]:
                        preflop = True
                        flop = False
                        turn = False
                        river = False
                    elif "*** FLOP ***" in hand[i]:
                        # listy["Phase"] = "Flop"
                        flop = True
                        preflop = False
                        turn = False
                        river = False
                    elif "*** TURN ***" in hand[i]:
                        # listy["Phase"] = "Turn"
                        turn = True
                        preflop = False
                        flop = False
                        river = False
                    elif "*** RIVER ***" in hand[i]:
                        # listy["Phase"] = "River"
                        river = True
                        preflop = False
                        flop = False
                        turn = False

                    if preflop == True:
                        listy["Phase"] = "Preflop"
                        phase = "Preflop"
                    elif flop == True:
                        listy["Phase"] = "Flop"
                        phase = "Flop"
                    elif turn == True:
                        listy["Phase"] = "Turn"
                        phase = "Turn"
                    elif river == True:
                        listy["Phase"] = "River"
                        phase = "River"
                    else:
                        listy["Phase"] = "None"
                        phase = "PreFlop"

                    listy["HandID"] = hand[1].split(' ')[2]
                    listy["TimeStamp"] = hand[1].split('-')[1]
                    listy["GameType"] = hand[1].split(':')[1].split('-')[0]
                    listy["TableName"] = hand[2].split("'")[1]
                    listy["MaxNoOfPlayers"] = hand[2].split(' ')[2][0]
                    listy["Button"] = hand[2].split('#')[1].split(' ')[0]
                    if hand[i].split(' ', 1)[0] == "Seat":
                        if "in chips" in hand[i]:
                            positions.append({"Seat": hand[i].split(' ')[1], "Player": hand[i].split(' ')[2],
                                              "StackSize": hand[i].split(' ')[3][1:]})
                    if "posts small blind" in hand[i]:
                            listy["SmallBlind"] = hand[i].split(':')[0]
                    if "posts big blind" in hand[i]:
                            listy["BigBlind"] = hand[i].split(':')[0]
                    if ":" in hand[i].split(' ')[0]:
                            moves.append({"Player": hand[i].split(':')[0], "Action": hand[i].split(':')[1], "Phase": phase})
                    if "collected" in hand[i] and "Seat" not in hand[i]:
                            listy["Winner"] = hand[i].split(' ')[0]
                            listy["Winner_Amount"] = hand[i].split(" ")[2]
                            print(listy["Winner"] + " " + listy["Winner_Amount"])
            listy["Positions"] = positions
            listy["moves"] = moves
            test.append(listy)

    Hands1["Hands"] = test
    return Hands1

def totalCounts():
    path = '/home/syed/Documents/AdvDI/Hands1/Part1/'
    totalFiles = 0
    totalHands = 0
    count = 0
    for filename in os.listdir(path):
        listy = {}
        if count == 0 :
            totalFiles = totalFiles + 1
            newData = open(path + filename, 'r')
            tempFileData = newData.read()
            result = countNumberOfHands(tempFileData, listy, filename)
            totalHands = totalHands + len(result["Hands"])
            count +=1

    return result
    #print("Total Hands:", totalHands)
    #print("Total Files:", totalFiles)

result = totalCounts()

#Insert into game
#p = Game(number_of_hands=len(result["Hands"]), game_type=result["game_type"], game_name=result["game_name"])
#p.save()

#Insert into hands
# orbit = 0
# for i in range(len(result["Hands"])):
#     if result["Hands"][i]:
#         if len(result["Hands"][i]["moves"]) > len(result["Hands"][i]["Positions"]):
#             orbit = 2
#         else:
#             orbit = 1
#         #
#         # print(result["Hands"][i]["showdown"])
#         # print(result["Hands"][i]["flop"])
#         # print(result["Hands"][i]["river"])
#         # print(result["Hands"][i]["turn"])
#
#         s = Hand(game_ID = ["HandID"], number_of_orbit = orbit, winner = result["Hands"][i]["Winner"],\
#              showdown = result["Hands"][i]["showdown"], flop = result["Hands"][i]["flop"] , river = result["Hands"][i]["river"] , turn = result["Hands"][i]["turn"] ,rake = "0", timeStamp = result["Hands"][i]["TimeStamp"], number_of_players = result["Hands"][i]["MaxNoOfPlayers"],\
#              button =result["Hands"][i]["Button"], big_blind =result["Hands"][i]["BigBlind"], small_blind=result["Hands"][i]["SmallBlind"])
#         s.save()

#Insert into PlyersInGAme
#handID, playerID, stacksize, seat
# for i in range(len(result["Hands"])):
#     if result["Hands"][i]:
#         for j in range(len(result["Hands"][i]["Positions"])):
#             s = PlayersInGame(player_ID = result["Hands"][i]["Positions"][j]["Player"], hand_ID  = result["Hands"][i]["HandID"], stack_size = result["Hands"][i]["Positions"][j]["StackSize"], seat = result["Hands"][i]["Positions"][j]["Seat"])
#             s.save();
#

#Insert into Move
# handID, player_ID, action, amount, phase, postion, indicators
# moves; player, action ,phase
# move = ""
# amount = ""
# for i in range(len(result["Hands"])):
#     if result["Hands"][i]:
#         for j in range(len(result["Hands"][i]["moves"])):
#             new = result["Hands"][i]["moves"][j]["Action"].split('$')
#             if len(new) > 2:
#                 move = new[0]
#                 amount = new[2].split(' ')[0]
#             if len(new) > 1 and len(new) < 3:
#                 move = new[0]
#                 amount = new[1].split(' ')[0]
#             elif len(new) < 2:
#                 move = new[0]
#                 amount = "0"
#
#
#             s = Move(         player_ID= result["Hands"][i]["moves"][j]["Player"],\
#                               hand_ID=result["Hands"][i]["HandID"],\
#                               action = move,\
#                               amount = amount,
#                               phase = result["Hands"][i]["moves"][j]["Phase"],
#                               postion = "button",
#                               indicators = "some_thing"
#                               )
#             s.save();

#Insert into Player
# m_ratio, player_name, hands_played, avrg_profit, avrg_stake, avrg_ROI, total_stake, player_since



