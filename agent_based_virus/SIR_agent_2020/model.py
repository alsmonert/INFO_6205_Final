import random

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from SIR_agent_2020.agents import Susceptible, Susceptible_with_mask, Infected, Recovered
from SIR_agent_2020.schedule import RandomActivationByHealth


class SIR(Model):
    '''
    A susceptible, infected, and recovered agent based model built using mesa. Built
    on top of wolf_sheep model by mesa.
    '''

    height = 50 #starting height/width for the board
    width = 50

    description = 'A model for simulating sick, infected, and recovered individuals.'

    def __init__(self,
                 initial_susceptible,
                 initial_infected,
                 initial_recovered,
                 initial_susceptible_with_mask,
                 gamma,
                 beta,
                 epsilon,
                 alpha,
                 height=height, width=width, verbose = False):
        '''
        Create a new SIR model.
        parameters:
            initial_infected:int, initial number of susceptible individuals
            initial_susceptible_with_mask:int, initial number of masked susceptible individuals
            initial_recovered:int, initial number of infected individuals
            initial_recovered:int, initial number of recovered individuals
            gamma:float, infection rate
            beta: float, recovery rate
            epsilon:float, removal rate
            alpha:float, entry rate to board
            height:int, width of board
            width:int, width of board
        '''
        #initializing the datacolector with initial susceptible/infected/recovered
        self.datacollector = DataCollector(
            {"Susceptible": lambda m: initial_susceptible,
            "Susceptible_with_mask": lambda m: initial_susceptible_with_mask,
             "Infected": lambda m: initial_infected,
             "Recovered": lambda m: initial_recovered})

        # Set starting parameters for board and rates
        self.height = height
        self.width = width
        self.initial_susceptible = initial_susceptible
        self.initial_susceptible_with_mask = initial_susceptible_with_mask
        self.initial_infected = initial_infected
        self.initial_recovered = initial_recovered
        self.beta = beta/100
        self.gamma = gamma/100
        self.epsilon = epsilon/100
        self.alpha = alpha/100
        self.verbose = verbose

        #sets up grid and data collector to store values
        self.schedule = RandomActivationByHealth(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            {"Susceptible": lambda m: m.schedule.get_health_count(Susceptible),
            "Susceptible_with_mask": lambda m: m.schedule.get_health_count(Susceptible_with_mask),
             "Infected": lambda m: m.schedule.get_health_count(Infected),
             "Recovered": lambda m: m.schedule.get_health_count(Recovered)})

        # Creates a susceptible individual:
        for i in range(self.initial_susceptible):
            x = random.randrange(self.width) #random x within board
            y = random.randrange(self.height) #random y within board
            susceptible = Susceptible((x, y), self, True) #sets location as susceptible
            self.grid.place_agent(susceptible, (x, y)) #places agent on board
            self.schedule.add(susceptible) #adds agent to model schedule

        # Creates a musked susceptible individual:
        for i in range(self.initial_susceptible_with_mask):
            x = random.randrange(self.width) #random x within board
            y = random.randrange(self.height) #random y within board
            susceptible_with_mask = Susceptible_with_mask((x, y), self, True) #sets location as masked susceptible
            self.grid.place_agent(susceptible_with_mask, (x, y)) #places agent on board
            self.schedule.add(susceptible_with_mask) #adds agent to model schedule

        # Creates an infected individual:
        for i in range(self.initial_infected):
            x = random.randrange(self.width) #random x within board
            y = random.randrange(self.height) #random y within board
            infected = Infected((x, y), self, True) #sets location as infected
            self.grid.place_agent(infected, (x, y)) #places infected on board
            self.schedule.add(infected) #adds agent to model schedule

        # Creates a recovered individual:
        for i in range(self.initial_recovered):
            x = random.randrange(self.width) #random x within board
            y = random.randrange(self.height) #random y within board
            recovered = Recovered((x, y), self, True) #sets location as recovered
            self.grid.place_agent(recovered, (x, y)) #places agent on board
            self.schedule.add(recovered) #adds agent to model scheduler

        self.running = True
        self.datacollector.collect(self) #runs the lamda functions in the datacollector and stores the values

    def step(self):
        '''
        Function to take one time step of our model
        '''
        self.datacollector.collect(self) #runs the lamda functions in the datacollector and stores the values
        self.schedule.step() #model takes one step
        if self.verbose:
            print([self.schedule.time,
                   self.schedule.get_health_count(Susceptible),
                   self.schedule.get_health_count(Susceptible_with_mask),
                   self.schedule.get_health_count(Infected),
                   self.schedule.get_health_count(Recovered)])

        if self.schedule.get_health_count(Infected) == 0: #if number of infected is equal to zero, stop running
            self.running = False

    def run_model(self, step_count=200):
        '''
        Function for running model.
        Parameters:
        step_count:int, number of times the function will run
        '''
        #print statements for number of initial individuals
        if self.verbose:
            print('Initial number susceptible: ',
                  self.schedule.get_health_count(Susceptible))
            print('Initial number masked susceptible: ',
                  self.schedule.get_health_count(Susceptible_with_mask))
            print('Initial number infected: ',
                  self.schedule.get_health_count(Infected))
            print('Initial number recovered: ',
                self.schedule.get_health_count(Recovered))

        for _ in range(step_count):
            self.datacollector.collect(self) #runs the lamda functions in the datacollector and stores the values
            self.step() #calls the step function

        #print statements for number of final individuals
        if self.verbose:
            print('Final number susceptible: ',
                  self.schedule.get_health_count(Susceptible))
            print('Final number masked susceptible: ',
                  self.schedule.get_health_count(Susceptible_with_mask))
            print('Final number infected: ',
                  self.schedule.get_health_count(Infected))
            print('Final number recovered: ',
                self.schedule.get_health_count(Recovered))
