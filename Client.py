import socket
from threading import Thread
# väljer SERVER_HOST "127.0.0.1" för att använda localhost
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 12345
seperator = "<SEP>"

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # skapar en socket och ansluter till servern
    print(f"Connecting to {SERVER_HOST}:{SERVER_PORT}")
    s.connect((SERVER_HOST, SERVER_PORT))
    print("Connected.")
except Exception as e:
    print(f"Could not connect to server. Error: {e}")
    exit()
# skapar en variable för att kunna använda senare så man kan identifiera vem som skrev meddelandet för tydligare chatt
name = input("Enter your name:")
print(f"Welcome {name}")

def listen_for_messages():
    """
    funktion som  lyssnar efter inkommande meddelanden från servern och
    när ett meddelande tas emot skriver den ut det i konsolen.

    Funktionen körs i en separat tråd för att användaren ska kunna ta emot meddelanden samtidigt som den själv skriver.
    """

    while True:
        try:
            message = s.recv(1024).decode('utf-8')
            if not message:
                print("Server connection closed.")
                break
            print("\n" + message)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

t = Thread(target=listen_for_messages)
# använder daemon tråd för att tråd snabbt ska avslutas när användaren disconnectar servern
t.daemon = True
# startar tråden så att listen_for_messages körs samtidigt som huvudprogrammet
t.start()

while True:
    send_msg = input()
    if send_msg.lower() == 'q':
        break
    #formatarear meddelandet med namn och seperatorn så det blir tydligt vem som skickade meddelandet
    send_msg = f"{name}{seperator}{send_msg}"
    try:
        s.send(send_msg.encode('utf-8'))
    except Exception as e:
        print(f"Error sending message: {e}")
        break

s.close()