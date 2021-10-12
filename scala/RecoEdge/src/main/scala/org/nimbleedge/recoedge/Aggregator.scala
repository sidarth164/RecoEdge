package org.nimbleedge.recoedge

import akka.actor.typed.ActorRef
import akka.actor.typed.{Behavior, SupervisorStrategy}
import akka.actor.typed.scaladsl.{Behaviors, TimerScheduler}

object Aggregator {

  sealed trait Command

  object Command {
    case class StartCycle()                                 extends Command
    case class RegisterParent(parentRef: ActorRef[Command]) extends Command
    case class StartAggregation()                           extends Command
    case class TriggerTrainers()                            extends Command
  }

  // TODO: Add commands here

  def apply(): Behavior[Command] =
    Behaviors
      .supervise(
        Behaviors.withTimers[Command](timerScheduler => getAggregatorBehavior(None, timerScheduler))
      )
      .onFailure(SupervisorStrategy.restart)

  def getAggregatorBehavior(
      parentRefOpt: Option[ActorRef[Command]],
      timerScheduler: TimerScheduler[Command]
    ): Behavior[Command] =
    Behaviors.setup { _ =>
      Behaviors.receiveMessage {
        case Command.RegisterParent(parentRef) =>
          if (parentRefOpt.isEmpty) {
            getAggregatorBehavior(Some(parentRef))
          } else {
            // TODO: handle gracefully, send an error message
            Behaviors.same
          }
        case Command.StartCycle() =>
        // TODO: send info + trigger python sampling kafka process
        case Command.TriggerTrainers() =>
        // TODO: listen on kafka for the result
        case Command.StartAggregation() =>
        // TODO: will be done once we receive models, send the notification to kafka
        case _ =>
          Behaviors.unhandled
      }
    }

}
