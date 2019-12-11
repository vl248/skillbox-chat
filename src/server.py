#  Created by Artem Manchenkov
#  artyom@manchenkoff.me
#
#  Copyright © 2019
#
#  Сервер для обработки сообщений от клиентов
#
#  Ctrl + Alt + L - форматирование кода
#
from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory, connectionDone
from twisted.protocols.basic import LineOnlyReceiver


class ServerProtocol(LineOnlyReceiver):
    factory: 'Server'
    login: str = None
    logins: list = []
    content_log: list = []

    def connectionMade(self):
        # Потенциальный баг для внимательных =)
        self.factory.clients.append(self)

    def connectionLost(self, reason=connectionDone):
        self.factory.clients.remove(self)

    def lineReceived(self, line: bytes):
        content = line.decode()

        if self.login is not None:
            content = f"Message from {self.login}: {content}"
            self.content_log.append(content)
            if len(self.content_log) > 10:
                del self.content_log[0]

            for user in self.factory.clients:
                if user is not self:
                    user.sendLine(content.encode())
        else:
            # login:admin -> admin
            if content.startswith("login:"):
                self.login = content.replace("login:", "")
                if self.login not in self.logins:
                    self.sendLine("Welcome you, ".encode() + self.login.encode())
                    self.logins.append(self.login)
                    self.send_history()
                else:
                    self.sendLine("Login ".encode() + self.login.encode() + " already taken! Choose another.".encode())
                    self.transport.loseConnection()
            else:
                self.sendLine("Invalid login".encode())

    def send_history(self):
        for history_line in self.content_log:
            self.sendLine(history_line.encode())

class Server(ServerFactory):
    protocol = ServerProtocol
    clients: list

    def startFactory(self):
        self.clients = []
        print("Server started")

    def stopFactory(self):
        print("Server closed")


reactor.listenTCP(1234, Server())
reactor.run()
