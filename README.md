			WELCOME TO THE QUIZ !!!

INTERFACE:

    • No: of questions will be given which is to be answered by the player . 
    • First player to reach a score of 5 points will be declared as winner .
    • When a question is asked there will be a buzzer that you need to press in 10sec which means  that if you want to answer the question you need to press “y” and press enter .
    • You will be given a chance to answer the question if you press the buzzer in less than 10sec .. correct answer will give +1 , but incorrect will give -0.5 ... if u dont press the buzzer than no marks will be deducted or added .
    • If any player answers the question then after answering scores will be shown of all players on host screen  

HOW TO RUN THE QUIZ :

    • First of all you need to install a python3 compiler .
    • Open the terminal and write “python3 host.py” . This will open the server side from where quiz will run .
    • It will be asked that how many players are playing . So fill the no: of players eg. 2 or 3 etc.
    • Now server will be waiting for the players so for players to join , open that no: of new terminals and run “python3 client.py” . This will open the client(player) side from where player will answer the question . 

DESCRIPTION:

    • This is based on a multiple client server program and code in written in python . 
    • We will bind to a port and connection will be established between client and server . 
    • All the details of code are written as comments in itself the code file . 
    • One issue is that once a file is opened in terminal it will tell you on which port it is running , but if it fails to bind the socket then it will try the another port which will appear on the server side . Then you need to change the port no: in client side in this way :
        ◦ Open client.py 
        ◦ go to 6th line i.e. : client.connect((socket.gethostname() , 9999))  
        ◦ initially it will connect to port no: 9999 
        ◦ but if it fails then change port no: (i.e. 9999) to new port no: which will be shown on  server screen .
    • There will a file named “question.txt” from which questions will be asked in a random manner (it should not be disclosed to players). 


