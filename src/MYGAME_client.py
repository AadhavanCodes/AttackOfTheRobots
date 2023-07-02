import pygame
import toolbox
import random
from PodSixNet.Connection import ConnectionListener, connection
from time import sleep

running = True


class MyGameClient(ConnectionListener):
    def __init__(self, host, port):
        """
        Client constructor function. This is the code that runs once
        when a new client is made.
        """
        ConnectionListener.__init__(self)

        # Start the game
        pygame.init()
        pygame.mixer.pre_init(buffer=1024)
        game_width = 1000
        game_height = 650
        self.screen = pygame.display.set_mode((game_width, game_height))
        self.clock = pygame.time.Clock()

        self.connected = False

        self.Connect((host, port))

    def update(self):
        """
        Client update function. This is the function that runs over and
        over again, once every frame of the game.
        """
        connection.Pump()
        self.Pump()

        # Set running to False if the player clicks the X or presses esc
        global running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # Tell pygame to update the screen
        pygame.display.flip()
        self.clock.tick(30)
        pygame.display.set_caption("GET CONNECTED! fps: " + str(self.clock.get_fps()))

    def ShutDown(self):
        """
        Client ShutDown function. Disconnects and closes the game.
        """
        self.connected = False
        connection.Close()
        pygame.quit()
        exit()

    #####################################
    ### Client-side Network functions ###
    #####################################
    """
    Each one of these "Network_" functions defines a command
    that the server will tell you (the client) to do.
    """

    def Network_connected(self, data):
        """
        Network_connected runs when you successfully connect to the server
        """
        self.connected = True
        print("Connection successful!")


    def Network_error(self, data):
        """
        Network_error runs when there is a server error
        """
        print('error:', data['error'][1])
        self.ShutDown()

    def Network_disconnected(self, data):
        """
        Network_disconnected runs when you disconnect from the server
        """
        print('Server disconnected')
        self.ShutDown()


# Remember to change this line to the commented line if you are on a different computer!

ip = "192.168.86.242"  # input("Please enter the host's IP address: ")
port = 5555
thisClient = MyGameClient(ip, port)

"""This is the loop that keeps going until the game is closed"""
while running:
    thisClient.update()

thisClient.ShutDown()
