from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from SIR_agent_2020.agents import Susceptible,Susceptible_with_mask, Infected, Recovered
from SIR_agent_2020.model import SIR

"""
Citation:
The following code was adapted from server.py at
https://github.com/projectmesa/mesa/blob/master/examples/wolf_sheep/wolf_sheep/server.py
Author of original code: Taylor Mutch
"""

def agent_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Susceptible:
        portrayal["Shape"] = "SIR_agent_2020/resources/susceptible.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is Susceptible_with_mask:
        portrayal["Shape"] = "SIR_agent_2020/resources/Susceptible_with_mask.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2

    elif type(agent) is Infected:
        portrayal["Shape"] = "SIR_agent_2020/resources/infected.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 3

    elif type(agent) is Recovered:
        portrayal["Shape"] = "SIR_agent_2020/resources/recovered.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 4

    else:
        return
    return portrayal


canvas_element = CanvasGrid(agent_portrayal, 50, 50, 600, 600)
chart_element = ChartModule([{"Label": "Susceptible", "Color": "#FF0000"},
                             {"Label": "Susceptible_with_mask", "Color": "#FFFF00"},
                             {"Label": "Infected", "Color": "#99D500"},
                             {"Label": "Recovered", "Color":"#0000FF"}])

model_params = {"verbose": UserSettableParameter('checkbox', "Verbose?", False),
                "initial_susceptible": UserSettableParameter('slider', 'Initial Susceptible Population', 150, 0, 300),
                "initial_susceptible_with_mask": UserSettableParameter('slider', 'Initial maksed Susceptible Population', 150, 0, 300),
                "initial_infected": UserSettableParameter('slider', 'Initial Infected Population', 150, 0, 300),
                "initial_recovered": UserSettableParameter('slider', 'Initial Recovered Population', 0, 0, 300),
                "gamma": UserSettableParameter('slider', "Recovery Rate", 0, 1, 100),
                "epsilon": UserSettableParameter('slider', "Population Decrease Rate", 15, 0, 50),
                "alpha": UserSettableParameter('slider', "Population Increase Rate", 20, 0, 50),
                "beta": UserSettableParameter('slider', "Infection Rate", 0, 1, 100),
                "delta": UserSettableParameter('slider', "mortalty Rate", 5, 1, 15)}

server = ModularServer(SIR, [canvas_element, chart_element], "Susceptible, Susceptible_with_mask, Infected, Recovered", model_params)
