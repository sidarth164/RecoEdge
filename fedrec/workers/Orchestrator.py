import attr
from thespian.actors import Actor


class Orchestrator(Actor):

    class Command(object):
        pass

    @attr.s
    class UpdateConfig(Command):
        config = attr.ib()

    @attr.s
    class ReceiveModel(Command):
        dataset = attr.ib()

    def receiveMessage(self, msg, sender):
        if isinstance(msg, self.UpdateConfig):
            pass
        elif isinstance(msg, self.ReceiveModel):
            pass
        else:
            pass
