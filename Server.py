import socket
from threading import Thread

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 12345
# använder separator som skiljer på namn och meddelandet för att göra meddelandet tydligt
separator = "<SEP>"

# Använder set() för att hantera klienter så det går snabbt och inte blir dubbleter
client_sockets = set()

# Skapar socket med IPv4 och TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f"Listening as {SERVER_HOST}:{SERVER_PORT}")

def listen_for_client(cs):
    """
    funktion som hanterar en klientanslutning. tar emot meddelanden från
    klienten, skickar dem vidare till alla andra anslutna klienter och
    stänger anslutningen när det behövs.
    """
    while True:
        try:
            # Ta emot meddelande från klienten
            msg = cs.recv(1024).decode('utf-8')
            # gör så att programmet breakar från loopen ifall inget meddelande tas emot ifrån klienten
            if not msg:
                break
            msg = msg.replace(separator, ": ") # Ersätter separatorn med (: ) så att meddelandet blir snyggt och tydligt
        except Exception as e:
            print(f"Error: {e}")
            break
        
        # Broadcasta meddelandet till alla andra klienter
        for client_socket in client_sockets:
            if client_socket != cs:  # Ser till att inte skicka tillbaka meddelandet till den som skicka
                try:
                    client_socket.send(msg.encode('utf-8')) # skickar meddelandet till alla klienter
                # hanterar fel vid sändning med except som stänger ner klient socket och tar bort den ifrån client_sockets
                except Exception as e:
                    print(f"Error broadcasting to client: {e}")
                    client_socket.close()
                    client_sockets.remove(client_socket)

    # Ta bort klienten från uppsättningen och stäng anslutningen när loopen är klar
    cs.close()
    client_sockets.remove(cs)

while True:
    client_socket, client_address = s.accept()
    print(f"{client_address} connected.")
    client_sockets.add(client_socket)

    # Starta en ny tråd för att köra listen_for_client för varje klient
    t = Thread(target=listen_for_client, args=(client_socket,))
    # gör tråden till en daemon tråd så den automatiskt avslutas när huvudprogrammet avslutas 
    t.daemon = True
    t.start()
