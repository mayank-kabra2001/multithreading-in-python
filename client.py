import socket 
import signal
import time

# socket.AF_INET = this function will estabish a connection over IPv4 or IPv6 . 
# socket.SOCK_STREAM = will create a TCP/IP connection . 
# if we want UDP connection then socket.SOCK_DGRAM is used . 
client  = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
client.connect((socket.gethostname() , 9999)) 


# this whole fxn will take care of the fact that client can only answer the buzzer for 10sec .. 
# i.e. client will be asked and input i.e. if he wants to press the buzzer ..and input is asked only for 10sec .. this fxn will take care of that . 
class AlarmException(Exception):
    pass

def alarmHandler(signum, frame):
    raise AlarmException

def take_input(timeout=10):
    signal.signal(signal.SIGALRM, alarmHandler)
    signal.alarm(timeout)
    try:
        text = input("You have 10s to press the buzzer:")
        signal.alarm(0)
        return text
    except AlarmException:
        print ('\ntimeout. Continuing...')
    signal.signal(signal.SIGALRM, signal.SIG_IGN)
    return ""

# this fxn will send answer to host so that he can confirm if answer is true or not . 
def give_answer():
    answer = input("Give answer:")
    client.send(answer.encode())
    print("\n")

print("quiz is starting and here is the question :")
print("\n")

# this is the whole client program in which he will recieve teh question and will ask to press the buzzer and if pressed .. he will be given a chance to answer . 
# meanwhile answering the question by client , all the other clients will wait until the new question arrives . 
def client_program():
    while True : 
        ques = client.recv(1024).decode()
        print(ques)       	
        print(ques)
        input = take_input()
        if(input == "y"):
            client.send("y".encode())
            give_answer()
            continue
        else:
            client.send("n".encode())
            print("\n")
            print("waiting for next question")
            print("\n")
            time.sleep(1)
            continue

if __name__ == '__main__':
    client_program()
    client.close()	

