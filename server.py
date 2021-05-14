import socket
import json
import sys
import argparse

from abalone_client import run

def subscribe(host, port, name):
    """
    Starts a socket client to send a subscription request to PI2CChampionshipRunner
    """
    with socket.socket() as s:
        print(">> Connecting to: {}:{} ...".format(host, server_port))
        try:
            s.connect((host, server_port))
            data_out = {
                "request": "subscribe",
                "port": port,
                "name": name,
                "matricules": ["18206", "0"]
                }
            s.send(json.dumps(data_out).encode("utf8"))
            result = json.loads(s.recv(1024).decode("utf8"))

            if result["response"] == "ok":
                print(">> Succesfully subscribed to PI2C Championship")
                listen_requests(host, port, name)

            elif result["response"] == "error":
                print(">> ERROR: {}".format(result["error"]))
            else:
                print("ERROR: Unknown message")
        except:
                raise SystemExit("Connection to PI2C Championship failed")

def listen_requests(host, port, name):
    """
    Starts a socket server to listen to incoming requests
    """
    with socket.socket() as sock:
        sock.bind((host, port))
        sock.listen()
        while True:
            try:
                connection, address = sock.accept()
                with connection:
                    data_in = connection.recv(1024).decode("utf8")
                    if data_in:
                        json_data = json.loads(data_in)
                        if json_data["request"] == "ping":
                            print(">> PING received")
                            pong_msg = json.dumps({"response": "pong"}).encode("utf8")
                            connection.send(pong_msg)
                        elif json_data["request"] == "play":
                            if json_data["state"]["players"][0] == name:
                                player_color = "B"
                            else:
                                player_color = "W"
                            board = json_data["state"]["board"]
                            try:
                                move = run(board, player_color)
                            except Exception as e: print(e)
                            if len(move["marbles"]) == 0 or move is None:
                                move_msg = json.dumps({"response": "giveup"}).encode("utf8")
                            else:
                                move_msg = json.dumps({"response": "move", "move": move, "message": "»»------------►"}).encode("utf8")
                            print("   moved: {} in direction: {}".format(move["marbles"], move["direction"]))
                            connection.send(move_msg)
                        else:
                            print("ERROR: Unknown message")

            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Abalone AI")
    parser.add_argument("name", help="choose a name, leave blank for default (default)")
    parser.add_argument("port", help="choose a port, leave blank for default (8026)")
    args = parser.parse_args()

    if len(sys.argv) > 2:
        name = str(sys.argv[1])
        port = int(sys.argv[2])
    else:
        port = 8026
        name = "default"

    host = "localhost"
    server_port = 3000
    subscribe(host, port, name)
