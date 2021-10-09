import attr
from thespian.actors import Actor


class Reception(Actor):

    class Command(object):
        pass

    @attr.s
    class Register(Command):
        role = attr.ib()
        id = attr.ib()
        kwargs = attr.ib()

    @attr.s
    class Discover(Command):
        role = attr.ib()

    class Healthy(Command):
        pass

    def receiveMessage(self, msg, sender):
        if isinstance(msg, self.Register):
            pass
        elif isinstance(msg, self.Discover):
            pass
