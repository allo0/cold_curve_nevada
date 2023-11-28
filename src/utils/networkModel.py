import json
import socket

from configs import logConf

logger = logConf.logger


class Network:
    def __init__(self, player, init_network=False, player_index=None):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 12345
        self.addr = (self.server, self.port)
        if init_network:
            self.p = self.connect(player)
        self.player_index = player_index

    def getP(self):
        return self.p

    def connect(self, player):
        try:
            self.client.connect(self.addr)
            self.client.settimeout(5)  # Set a timeout of 5 seconds

            # Send initial player data to the server
            initial_data = player.get_player_data()
            self.client.sendall(json.dumps(initial_data).encode('utf-8'))

            # Receive initial data from the server
            initial_data_json = self.client.recv(2048).decode('utf-8')
            initial_data = json.loads(initial_data_json)

            return initial_data
        except socket.timeout as e:
            logger.warning(f"Connection timed out: {e}")
        except Exception as e:
            logger.warning(f"Connection error: {e}")
        finally:
            self.client.close()

    def get_player_index(self):
        return self.player_index

    def send(self, data):
        try:
            # Convert data to JSON string
            json_data = json.dumps(data)

            # Send data size
            size = len(json_data)
            self.client.sendall(size.to_bytes(4, byteorder='big'))
            # Send JSON data
            self.client.sendall(json_data.encode('utf-8'))

            self.client.shutdown(socket.SHUT_WR)  # Shutdown the write end to signal the end of the data
            logger.info("Sent data to server")

            data = self.client.recv(2048)
            logger.info("Received data from server: %s", data)

            if data:
                # Receive acknowledgment or other response from the server if needed
                response = self.client.recv(2048).decode('utf-8')
                return response
        except socket.error as e:
            logger.error(e)

    def handle_disconnect(self):

        logger.info("Disconnected from the server.")

    def close(self):
        self.client.close()
