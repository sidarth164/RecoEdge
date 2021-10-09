import attr
from thespian.actors import Actor


class Trainer(Actor):

    class Command(object):
        pass

    @attr.s
    class RequestModel(Command):
        dataset = attr.ib()

    def receiveMessage(self, msg, sender):
        if isinstance(msg, self.RequestModel):
            pass
        else:
            pass
