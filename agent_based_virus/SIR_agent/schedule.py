import random
from collections import defaultdict

from mesa.time import RandomActivation


class RandomActivationByHealth(RandomActivation):
    '''
    A scheduler which activates each type of agent once per step, in random
    order, with the order reshuffled every step.

    This is equivalent to the NetLogo 'ask health...' and is generally the
    default behavior for an ABM.

    Assumes that all agents have a step() method.
    '''
    agents_by_health = defaultdict(list)

    def __init__(self, model):
        super().__init__(model)
        self.agents_by_health = defaultdict(list)

    def add(self, agent):
        '''
        Add an Agent object to the schedule
        
        '''
        self.agents.append(agent) # An Agent to be added to the schedule.
        agent_class = type(agent) 
        self.agents_by_health[agent_class].append(agent) # An Agent to be added to the schedule.

    def remove(self, agent):
        '''
        Remove all instances of a given agent from the schedule.
        '''

        while agent in self.agents: 
            self.agents.remove(agent) # remove agent

        agent_class = type(agent)
        while agent in self.agents_by_health[agent_class]:
            self.agents_by_health[agent_class].remove(agent)

    def step(self, by_health=False):
        '''
        Executes the step of each agent health, one at a time, in random order.
        '''
        if by_health: # If True, run all agents of a single health before running the next one.
            for agent_class in self.agents_by_health:
                self.step_health(agent_class) 
            self.steps += 1
            self.time += 1
        else: # if not, 
            super().step()

    def step_health(self, health):
        '''
        Shuffle order and run all agents of a given health.
        '''
        agents = self.agents_by_health[health] # Class object of the health to run.

        random.shuffle(agents) # random shuffled the agents
        for agent in agents:
            agent.step() # run agents of a given health

    def get_health_count(self, health_class):
        '''
        Returns the current number of agents of certain health in the queue.
        '''
        # print(health_class, len(self.agents_by_health[health_class]))
        return len(self.agents_by_health[health_class])
