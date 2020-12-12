import random

from mesa import Agent

from SIR_agent_2020.random_walk import RandomWalker  #RandomWalker from wolf_sheep example


class Susceptible_with_mask(RandomWalker):
    '''
    An individual who is susceptible but with mask. the infected rate will lower than normal susceptibles. This class has a fluid population with random
    chance of leaving and joining the model
    '''
    def __init__(self, pos, model, moore):
        super().__init__(pos, model, moore=moore)
        self.sick = False           #Are they sick?
        self.recovered = False      #Have they recovered?

    def step(self):
        '''
        A model step. Move, see if they get sick, continue.
        Sickness can occur if susceptible is nearby infected. Infection Rate
        is multiplied by amount of nearby infected neighbors.
        Chance to generate new susceptible if random.random() is above the
        population increase rate (alpha).
        '''
        self.random_move()  #From RandomWalker, agent moves randomly
        left = False
        # If there are infected people nearby, chance to become Infected
        #Chance multiplied by amount of infected agents nearby
        x, y = self.pos
        if (x > 15 and x<35 and y>15 and y< 35):#the area with high population dencity
            this_cell = self.model.grid.get_neighbors((x,y), moore=True, include_center = True) #Find all neighbors ()
            infected = [obj for obj in this_cell if isinstance(obj, Infected)] #Are those neighbors infected?
            if len(infected) > 0:   #If any neighbors are infected, do this
                if random.random() < self.model.beta*len(infected)*1.2*0.7: #Infection chance increace since it in the high population area, multiplied by amount of infected neighbors
                    #create new infected individual from Susceptible
                    new_infected = Infected(self.pos, self.model, True) #If infection successful, place new infected agent there
                    self.model.grid.place_agent(new_infected, new_infected.pos)
                    self.model.schedule.add(new_infected)   #Adds new infected agent to schedule

                    # Infect the individual
                    self.model.grid._remove_agent(self.pos, self)   #Removes the masked susceptible agent, who has become infected
                    self.model.schedule.remove(self)    #Removes susceptible from schedule
                    left = True
        else:
            this_cell = self.model.grid.get_neighbors((x,y), moore=True, include_center = True) #Find all neighbors ()
            infected = [obj for obj in this_cell if isinstance(obj, Infected)] #Are those neighbors infected?
            if len(infected) > 0:   #If any neighbors are infected, do this
                if random.random() < self.model.beta*len(infected)*0.7: #Infection chance, multiplied by amount of infected neighbors
                    #create new infected individual from Susceptible
                    new_infected = Infected(self.pos, self.model, True) #If infection successful, place new infected agent there
                    self.model.grid.place_agent(new_infected, new_infected.pos)
                    self.model.schedule.add(new_infected)   #Adds new infected agent to schedule

                    # Infect the individual
                    self.model.grid._remove_agent(self.pos, self)   #Removes the susceptible agent, who has become infected
                    self.model.schedule.remove(self)    #Removes susceptible from schedule
                    left = True

        if (random.random() < self.model.epsilon) and not left: #Population decay rate, if random.random() less than epsilon, susceptible agent leaves model
            self.model.grid._remove_agent(self.pos, self)   #Removes susceptible agent from model
            self.model.schedule.remove(self)    #Removes susceptible from schedule

        if random.random() < self.model.alpha:  #Population increase rate, if random.random() less than growth rate, spawn new susceptible agent in model
            new_masked_susceptible = Susceptible_with_mask(random.choice(self.model.grid.get_neighborhood((x,y), moore=True, include_center = True)), self.model, True)
            self.model.grid.place_agent(new_masked_susceptible, new_masked_susceptible.pos)   #places susceptible agent on model
            self.model.schedule.add(new_masked_susceptible)    #adds susceptible agent to schedule


class Susceptible(RandomWalker):
    '''
    An individual who is susceptible. This class has a fluid population with random
    chance of leaving and joining the model
    '''

    def __init__(self, pos, model, moore):
        super().__init__(pos, model, moore=moore)
        self.sick = False           #Are they sick?
        self.recovered = False      #Have they recovered?

    def step(self):
        '''
        A model step. Move, see if they get sick, continue.
        Sickness can occur if susceptible is nearby infected. Infection Rate
        is multiplied by amount of nearby infected neighbors.
        Chance to generate new susceptible if random.random() is above the
        population increase rate (alpha).
        '''
        self.random_move()  #From RandomWalker, agent moves randomly
        left = False
        # If there are infected people nearby, chance to become Infected
        #Chance multiplied by amount of infected agents nearby
        x, y = self.pos
        if (x > 15 and x<35 and y>15 and y< 35):#the area with high population dencity
            this_cell = self.model.grid.get_neighbors((x,y), moore=True, include_center = True) #Find all neighbors ()
            infected = [obj for obj in this_cell if isinstance(obj, Infected)] #Are those neighbors infected?
            if len(infected) > 0:   #If any neighbors are infected, do this
                if random.random() < self.model.beta*len(infected)*1.2: #Infection chance increace since it in the high population area, multiplied by amount of infected neighbors
                    #create new infected individual from Susceptible
                    new_infected = Infected(self.pos, self.model, True) #If infection successful, place new infected agent there
                    self.model.grid.place_agent(new_infected, new_infected.pos)
                    self.model.schedule.add(new_infected)   #Adds new infected agent to schedule

                    # Infect the individual
                    self.model.grid._remove_agent(self.pos, self)   #Removes the susceptible agent, who has become infected
                    self.model.schedule.remove(self)    #Removes susceptible from schedule
                    left = True
        else:
            this_cell = self.model.grid.get_neighbors((x,y), moore=True, include_center = True) #Find all neighbors ()
            infected = [obj for obj in this_cell if isinstance(obj, Infected)] #Are those neighbors infected?
            if len(infected) > 0:   #If any neighbors are infected, do this
                if random.random() < self.model.beta*len(infected): #Infection chance, multiplied by amount of infected neighbors
                    #create new infected individual from Susceptible
                    new_infected = Infected(self.pos, self.model, True) #If infection successful, place new infected agent there
                    self.model.grid.place_agent(new_infected, new_infected.pos)
                    self.model.schedule.add(new_infected)   #Adds new infected agent to schedule

                    # Infect the individual
                    self.model.grid._remove_agent(self.pos, self)   #Removes the susceptible agent, who has become infected
                    self.model.schedule.remove(self)    #Removes susceptible from schedule
                    left = True

        if (random.random() < self.model.epsilon) and not left: #Population decay rate, if random.random() less than epsilon, susceptible agent leaves model
            self.model.grid._remove_agent(self.pos, self)   #Removes susceptible agent from model
            self.model.schedule.remove(self)    #Removes susceptible from schedule

        if random.random() < self.model.alpha:  #Population increase rate, if random.random() less than growth rate, spawn new susceptible agent in model
            new_susceptible = Susceptible(random.choice(self.model.grid.get_neighborhood((x,y), moore=True, include_center = True)), self.model, True)
            self.model.grid.place_agent(new_susceptible, new_susceptible.pos)   #places susceptible agent on model
            self.model.schedule.add(new_susceptible)    #adds susceptible agent to schedule

class Infected(RandomWalker):
    '''
    An individual who is infected. These agents have the chance of infecting susceptible agents,
    recovering, and leaving the system through our liquid population model
    '''

    def __init__(self, pos, model, moore):
        super().__init__(pos, model, moore=moore)
        self.sick = True        #Are they sick?
        self.recovered = False  #Have they recovered?

    def step(self):
        '''
        A model step. Infected agents will move randomly and have the chance to spread their infection.
        Infected agents also have a chance of recovering, as well as leaving the system.
        '''
        self.random_move()  #From RandomWalker, agent moves randomly
        left = False

        x, y = self.pos
        if (x > 15 and x<35 and y>15 and y< 35):#the area with high population dencity
            if random.random() < self.model.gamma*1.25:  #If random.random() less than recovery rate (gamma), agent will become recovered, the recovered rate will be little bit higher than other area
                new_recovered = Recovered(self.pos, self.model, True)   #If recovery happens, place new recovered agent there
                self.model.grid.place_agent(new_recovered, new_recovered.pos)   #Place recovered agent on board
                self.model.schedule.add(new_recovered)  #Add new recovered agent to schedule
                self.model.grid._remove_agent(self.pos, self)   #Remove infected agent from board
                self.model.schedule.remove(self)    #Remove infected agent from schedule
                left = True
        else:
            if random.random() < self.model.gamma:  #If random.random() less than recovery rate (gamma), agent will become recovered
                new_recovered = Recovered(self.pos, self.model, True)   #If recovery happens, place new recovered agent there
                self.model.grid.place_agent(new_recovered, new_recovered.pos)   #Place recovered agent on board
                self.model.schedule.add(new_recovered)  #Add new recovered agent to schedule
                self.model.grid._remove_agent(self.pos, self)   #Remove infected agent from board
                self.model.schedule.remove(self)    #Remove infected agent from schedule
                left = True

        if (random.random() < (self.model.delta + self.model.epsilon)) and not left: #If random.random() less than the sum of population decay rate (epsilon) and mortalty Rate (delta), agent will leave model
            self.model.grid._remove_agent(self.pos, self)   #Removes agent from model
            self.model.schedule.remove(self)    #Removes agent from schedule


class Recovered(RandomWalker):
    '''
    An individual who is recovered. Infected agents have a chance to become Recovered.
    Recovered agents have a chance to leave the system through our liquid population model.
    Recovered agents also have a chance to become infected if there are more than 3 Infected
    agents nearby.
    '''

    def __init__(self, pos, model, moore):
        super().__init__(pos, model, moore=moore)
        self.sick = False       #Are they sick?
        self.recovered = True   #Have they recovered?

    def step(self):
        '''
        A model step. Recovered agents will move randomly.
        Recovered agents also have a chance of becoming infected, as well as leaving the system.
        '''
        self.random_move() #From RandomWalker, agent moves randomly
        left = False

        if random.random() < self.model.epsilon: #If random.random() less than population decay rate (epsilon), agent will leave model
            self.model.grid._remove_agent(self.pos, self)   #Remove agent from model
            self.model.schedule.remove(self)    #Remove agent from schedule
            left = True

        x, y = self.pos
        this_cell = self.model.grid.get_neighbors((x,y), moore=True, include_center = True) #Find all neighbors ()
        infected = [obj for obj in this_cell if isinstance(obj, Infected)]  #Are those neighbors infected?
        if (len(infected) > 3) and not left:    #If 3 of those neighbors are infected, do this
            #create new infected individual from Susceptible
            new_infected = Infected(self.pos, self.model, True) #Creates new infected agent
            self.model.grid.place_agent(new_infected, new_infected.pos) #Places new infected agent where recovered agent was
            self.model.schedule.add(new_infected)   #Adds new infected agent to schedule

            # Infect the individual
            self.model.grid._remove_agent(self.pos, self)   #Removes recovered agent from model
            self.model.schedule.remove(self)    #Removes recovered agent from schedule
