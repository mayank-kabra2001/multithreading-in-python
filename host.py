import socket
import sys
import time
import random 

#created all the required list to store the values .
all_connections = []
all_address = []
question_list = []
players = []
players_score = [] 

#this function is used to create socket ..
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))

#this function is used  bind that socket ...
#sometimes we uses the port so that port is busy so we can use another port as done in exception ..
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        port = port - 1
        print("That port is already occupied so trying to new port")
        bind_socket()

#this fxn is used to accept all the connection that are being made that is all the clients that are trying to connect .
#in this we are closing all the previous connection that have been established and deleting those store addres and connection ..
#s.accept() gives a tuple of conn and address value ..
#we are appending all the connections and addresses that are being established .
def accepting_connections():
    for c in all_connections:
    	c.close()

    del all_connections[:]
    del all_address[:]

    i=0 
    while (i < No_of_players):
        try:
            conn, address = s.accept()
            s.setblocking(1)  # prevents timeout

            all_connections.append(conn)
            all_address.append(address)

            print("Connection has been established :" + address[0])
            i = i+1
        except:
            print("Error accepting connections")

#these are the instruction that will be printed on the server screen i.e. host screen 
def instructions():
	print("welcome to the quiz!!")
	print("instruction--")
	print("quiz will be of 5 points , right answer = +1 , wrong answer = -0.5 , each person will have 10 seconds to answer the buzzer")
	print("\n")
	print("further instruction --")
	print("remember if u want to answer press 'y' and enter you will be given a chance to answer . NOTE - Answer should be started with a capital letters and all other small")
	print("\n")

#this fxn will open the questionfile and append all the questions in a list by seperating them with a line .
def questionlist(fname):
	for question in open(fname):
		question = question.rstrip()
		question_list.append(question)

#this fxn is used to pick a random question every time question is asked and if a question is asked it is not repeated again by deleting that question from list .  
def question_generator():
	ques = random.sample(question_list , 1)
	return ques
	question_list.remove(ques)

#this is used to display scores.
def scores():
	for i in range(No_of_players):
		print("score of player {} is {}".format(i , players_score[i]))

#this fxn is used to ansk answers from client who has pressed the buzzer ..
#answer will be asked only to that client who has pressed the buzzer and this is taken care from player which is actually the connection .
#client will be showed if his anser is correct or not . 
#after every answer of a question score will be displayed on the screen . 
def ask_answer(player , ans):
	data = player.recv(1024).decode()
	if(data == ans):
		player.send("correct -> +1".encode())
		players_score[players.index(player)] += 1 
		scores()
	else:
		player.send("Wrong -> -0.5".encode())
		players_score[players.index(player)] -= 0.5
		scores()

#this fxn is used to append all the connections as players and putting questions in a list ,,
#this is just like establishing the whole setup of the game .
def establising_players_file():
	for i in range(No_of_players):
		players.append(all_connections[i])
		players_score.append(0) 

	filename = "questions.txt"
	questionlist(filename)

#this wait fxn is used to ask the client to press the buzzer for only 10sec . i.e. client has only 10sec to press the buzzer if he wants to answer . 
#this fxn will take care which client has the buzzer first and will ask to that client about answer .
#this is done by storing the client buzzer reply . if he has pressed then data stores is "y" if nothing is pressed by client then "n" . 
#it also takes care of the fact that if no has answered the question . 
def wait(ans):
	delay = 11
	iterator = 0
	breaked = False

	time.sleep(delay)
	data = []
	for i in range(No_of_players):
		data.append(players[i].recv(1024).decode())

	
	for i in range(No_of_players):
		if data[i] == "y":
			ask_answer(players[i] , ans)
			print("\n")
			breaked = True
			break
		if data == "n":
			continue
			iterator += 1		

	if(iterator == No_of_players):
		print("nobody gives the answer ... so moving to next question")

		
#this fxn is used to generate question and put it on the screen . 
#in questions file there is both questions and answer .. so we give questions on every client screen and stored the answer .. it will be used to check with the client answer .
#all the client screen will be asked the question .
def run_quiz():
	while (max(players_score) < 5):
		question = ""
		question_gen = []
		question = question_generator() 
		question_gen.append(question[0].split(' -Answer: '))
		ques = question_gen[0][0]
		ans = question_gen[0][1]

		for connection in all_connections:
			connection.send(ques.encode())

		wait(ans)

#after the quiz is over all connections need to be closed .. 
#all tored connections need to be deleted . 
def end_quiz():
	for i in range(No_of_players):
		print("players {} score   = {}".format(i+1 , players_score[i]))
	
	print ("winner = player {}".format(players_score.index((max(players_score))) + 1))
	
	for c in all_connections:
		c.close()

	del all_connections[:]
	del all_address[:]

#it will ask how many no. of players are playing 
No_of_players = int(input("no of players playing:"))

#it only start the quiz by having all fxn . 
def start():
	create_socket()
	bind_socket()
	accepting_connections() 
	instructions()
	establising_players_file()
	run_quiz()
	end_quiz()

if __name__ == '__main__':
	start()
