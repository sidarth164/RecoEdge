import attr
from thespian.actors import Actor


class Aggregator(Actor):

    class Command(object):
        pass

    @attr.s
    class DiscoverTrainer(Command):
        config = attr.ib()

    @attr.s
    class StartCycle(Command):
        iteration = attr.ib()

    @attr.s
    class ReceiveModel(Command):
        dataset = attr.ib()

    def receiveMessage(self, msg, sender):
        if isinstance(msg, self.DiscoverTrainer.__class__):
            pass
        elif isinstance(msg, self.StartCycle.__class__):
            pass
        elif isinstance(msg, self.ReceiveModel.__class__):
            pass
        else:
            pass
