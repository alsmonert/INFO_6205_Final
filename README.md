# Susceptible, Infected, and Recovered Model

Adapted from the mesa agent-based modeling package in python. Using the structural framework of the wolf_sheep model found [here](https://github.com/projectmesa/mesa-examples/tree/master/examples/WolfSheep). We accredit mesa for their hard work and development efforts. Without which, this projects would not have come to fruition.


## Summary

The model focuses on basic population interactions where we look at the spread of a disease throughout a fluid group of individuals. In the model, new people can enter the simulation. Every new agent enters susceptible. New agents are added to the neighborhood of a current agent in the model. There are also infected agents in the model. Infected agents are individuals that are currently being affected by the disease. If an infected person and a susceptible person come within contact, then a random number is generated and compared against the infection rate to determine how the disease spreads. At each new iteration, there is also a random chance that an infected individual can become recovered. Thus, the three agents we are working with are susceptible, infected, and recovered. In the end, we have decided to add a new agent that is Susceptible_with_mask. It has a lower rate of being infected than normal susceptible people.

The population dynamics included in this model are people coming and going at adjustable rates. New people are added only to the susceptible class, but an individual in any class has a chance of leaving the model regardless of health status. There is a 10 x 10 space in the center of the map, which represents the city area. It has a higher infection rate and a higher recovery rate due to the better hospital severice.

We did not incorporate viral mutations into this model specifically. Instead, we established a rule that if a recovered individual interacts with at least three infected individuals, they can become sick again. This is meant to model mutations because people can get repeat infections, or a new strain can arise based on the need to transmit but the inability to do so based on previous infections.

The model will end when there are no more sick people because there is no longer an infection to spread and thus no reason to continue observing the agents.

## Installation

To install the dependencies use pip and the requirements.txt in this directory. e.g.

```
    > pip install -r requirements.txt
```
The directory lists each of the required modules and a command to make sure they are up to date with the latest versions. **Note:** The latest version of `tornado` is incompatible with the mesa visualization tools we implement here. The tornado version used in this model is version `4.5.2`, which requirements will install.

## How to Run

To run the model interactively, run ``run.py`` in this directory. e.g.

```
    > python run.py
```

Then open your browser to [http://127.0.0.1:8521/](http://127.0.0.1:8521/) and press Reset, then Run.

**Note:** Mac users using the OnePassword extension in Google Chrome may face permission issues where mesa is unable to launch the visualization in the browser due to the security put in place by OnePassword. In order to work around this issue, open a Google Chrome window, login to your OnePassword extension, then close the browser and relaunch the mesa visualization. This should "unlock" the browser. If this persists, try setting your default browser to something other than a browser where OnePassword is enabled.

**Note:** The mesa visualization package has a current issue where the DataCollector object which creates the live-updating graphs does not get reset or reinitialized when the `Reset` button is pressed. The graph will first plot the previous model's execution, and then it will plot the data from this new visualization. **In order to get mesa to produce a new graph of the new simulation without the old data present**, close the browser, kill the mesa kernel, and relaunch by running `python run.py`. The configure the settings for the model, hit `Reset` and then `Run`.

## Files

* `agents.py` : File where the agents in the model are defined as well as the rules of the interactions. The three classes, Susceptible, Infected, and Recovered. The classes here inherit from the RandomWalker class.

* `random_walk.py` : Class defined by the mesa developers. Defines an agent that walks randomly around the model's grid and interacts with other agents. Has only a few base properties for moving and defining the neighborhood.

* `model.py` : File that defines the Grid where the agents will move and interact as well as the parameters used by the agents for their rules of interactions. Parameters are:
  * alpha: Rate at which population increases.
  * beta: Rate at which the infection spreads.
  * gamma: Rate at which infected people recover.
  * epsilon: Rate at which population decreases.
  * delta: Rate at which the infected people dead.
  * verbose: Prints the counts of each class out at the command line for each time step.

The descriptions of these parameters is seen in the interactive visualization, but defined by the above names in the model.

* `schedule.py` : Functions defined by mesa for getting counts of agents by classes, how to carry out the `step` function at each iteration, and additional functions for executing the model and the rules of interactions.

* `server.py` : Takes the agents from the model and makes the visualization using some open source images from Google. Each new `launch` of the server calls a new instance of the SIR model class. DataCollector information is then used to create a graph in the browser window. Sliders for user parameter input is also defined here.

* Resources directory: Stores images used by server.

* `__init__.py` : Empty. Useful for package construction to define the `import *` method. Not used in our model but preserved from original mesa project.

## Further Reading

This model is based off of the mesa wolf_sheep model, which is largely based off of the NetLogo Wolf-Sheep Predation Model:

* Wilensky, U. (1997). NetLogo Wolf Sheep Predation model. http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation. Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.

* Venkatramanan, S. et. al. Using data-driven agent-based models for forecasting emerging infectious diseases. Epidemics 22 (2018) 43–49.

* Willem, L. (2015). Agent-Based Models For Infectious Disease Transmission. Universiteit Antwerpen and Universiteit Hasselt. Dissertation.
