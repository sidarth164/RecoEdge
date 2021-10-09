import attr
from thespian.actors import Actor, ActorSystem, WakeupMessage

from fedrec.workers.Orchestrator import Orchestrator
from fedrec.workers.Reception import Reception
from fedrec.workers.Trainer import Trainer


class SamplingStrategy():
    pass


# noinspection PyAttributeOutsideInit
class Aggregator(Actor):

    class Command(object):
        pass

    @attr.s
    class Initialize(Command):
        worker_id = attr.ib()
        reception_ref = attr.ib()

    class HealthCheck(Command):
        pass

    @attr.s
    class RegisterOrchestrator(Command):
        orchestrator_ref = attr.ib()
        model_provider_ref_list = attr.ib()

    @attr.s
    class StartCycle(Command):
        iteration = attr.ib()
        threshold = attr.ib()
        sampling_strategy = attr.ib()
        aggregator = attr.ib()

    @attr.s
    class ReceiveModel(Command):
        dataset = attr.ib()

    def receiveMessage(self, msg, sender):
        if isinstance(msg, self.Initialize):
            self.initialize(msg)
            self.wakeupAfter(10, 'CheckIfInitialized')
        elif isinstance(msg, self.RegisterOrchestrator):
            self.orchestrator_ref = msg.orchestrator_ref
            self.model_provider_ref_list = msg.model_provider_ref_list
            self.initialized = True
        elif isinstance(msg, self.HealthCheck):
            self.send(sender, Reception.Healthy)
        elif isinstance(msg, self.StartCycle):
            sampled_model_providers = msg.sampling_strategy(self.model_provider_ref_list)
            self.aggregator = msg.aggregator
            self.updated_models = []
            self.threshold = msg.threshold
            for model_provider_ref in sampled_model_providers:
                self.send(model_provider_ref, Trainer.RequestModel())
            self.wakeupAfter(1800, 'CheckIfModelAggregated')
        elif isinstance(msg, self.ReceiveModel):
            self.updated_models.append(msg.dataset)
        elif isinstance(msg, WakeupMessage):
            if msg.payload == 'CheckIfInitialized':
                if not self.initialized:
                    # TODO: Stop it!
                    pass
            elif msg.payload == 'CheckIfModelAggregated':
                if len(self.updated_models) >= self.threshold:
                    aggregated_model = self.aggregator(self.updated_models)
                    self.send(self.orchestrator_ref, Orchestrator.ReceiveModel(aggregated_model))
        else:
            pass

    def initialize(self, init_msg):
        self.worker_id = init_msg.worker_id
        self.reception_ref = init_msg.reception_ref
        self.initialized = False
        self.send(self.reception_ref, Reception.Register(Aggregator, self.worker_id, None))
