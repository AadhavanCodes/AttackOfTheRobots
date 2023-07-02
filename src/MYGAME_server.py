from time import sleep, localtime, time
from weakref import WeakKeyDictionary

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

import socket
import pygame
import toolbox


class ClientChannel(Channel):
    """
    This is the server representation of a single connected client.
    """

    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        self.number = 0

    def Close(self):
        self._server.DelPlayer(self)

    #####################################
    ### Server-side Network functions ###
    #####################################

    """
    Each one of these "Network_" functions defines a command
    that the client will ask the server to do.
    """

    def Network_hi(self, data):
        """
        Network_hi just prints a message
        """
        print("OMG a client just said hi to me")


class MyGameServer(Server):
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        """
        Server constructor function. This is the code that runs once
        when the server is made.
        """
        Server.__init__(self, *args, **kwargs)
        self.clock = pygame.time.Clock()
        self.players = WeakKeyDictionary()

        self.game_width = 1000
        self.game_height = 650

        print('Server launched')

    def Connected(self, player, addr):
        """
        Connected function runs every time a client
        connects to the server.
        """
        self.players[player] = True
        print("Player " + str(player.number) + " joined from " + str(addr))
        self.PrintPlayers()

    def DelPlayer(self, player):
        """
        DelPlayer function removes a player from the server's list of players.
        In other words, 'player' gets kicked out.
        """
        del (self.players[player])
        print("Deleting Player" + str(player.addr))
        self.PrintPlayers()

    def PrintPlayers(self):
        """
        PrintPlayers prints the number of each connected player.
        """
        print("players: ", [p.number for p in self.players])

    def SendToAll(self, data):
        """
        SendToAll sends 'data' to each connected player.
        """
        for p in self.players:
            p.Send(data)

    def Update(self):
        """
        Server Update function. This is the function that runs
        over and over again.
        """
        self.Pump()
        self.clock.tick(30)


ip = toolbox.getMyIP()
port = 5555
server = MyGameServer(localaddr=(ip, port))
print("Host IP: " + ip)

"""This is the loop that keeps going until the server is killed"""
while True:
    server.Update()
