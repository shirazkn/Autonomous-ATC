#### Autonomous Air Traffic Conflict-Resolution

We are using reinforcement learning to develop an air-traffic controller DQN. Here, I'm conducting preliminary investigation as part of a larger group project.
<br>

I'm currently implementing 2-aircraft conflict-resolution, to eventually be generalized to *n* aircrafts...


***

#### INSTALLATION
Installing dependencies,
- On **MacOS** with Python 3.6x, use `pip install -r requirements.txt`
- On **MacOS** with Python 3.7x, check `README_VENV.md` for instructions.
- On **Windows/Linux** you can install the Python(x,y) bundle which has all the dependencies. See resources below.

Running BlueSky,
- Run `python check.py` to verify BlueSky installation.
- Run `python BlueSky.py` to launch the gui.
- Use the Bluesky command `IC ML/2-AC.scn` to look at my WIP implementation.

#### RESOURCES
**Installation and Guides** <br>
BlueSky Wiki : https://github.com/TUDelft-CNS-ATM/bluesky/wiki
BlueSky Installation : http://homepage.tudelft.nl/7p97s/BlueSky/download.html
<br><br>
**Other**<br>
BlueSky can be integrated with BADA, which models the performance of different aircraft types. Can be used to set state-action constraints and costs.
https://simulations.eurocontrol.int/solutions/bada-aircraft-performance-model/
 
---

### *PROBLEM OVERVIEW*
#### DEFINITIONS <br>
**Conflict-resolution / CR** : The preemptive action that's taken whenever two aircrafts are projected to collide with (or come dangerously close to) each other
**Agent** : The air traffic controller (or the neural net)<br><br>
**State** : The float-valued column vector that has enough information embedded in it, to render each conflict-resolution time-step a Markov Decision Process. <br><br>
**State-action space** : The sub-space of conflict-resolution actions that can be taken (and are admissible) at any given state.<br><br>
**Loss** : Inversely proportional to 'reward' in RL. ATC incurs a lower (or no) loss for more desirable conflict-resolution actions.<br><br>
**Policy** : The relationship that maps the state to the optimal action at any CR time-step.

***

#### TD-LEARNING
The 1-step temporal difference (TD) update equation is given by,

<img src="images/qlearning_TD.png" alt="drawing" width="600"/> <br>
<sup>Source : https://towardsdatascience.com/@takuma.seno </sup><br>
where **Q(s,a)** is the expected return for taking action *a* at state *s*.
Once our algorithm has converged (or once *Q* $\rightarrow$ *Q**), our policy would involve choosing actions that maximize this return.
#### NEURAL NETWORKS

When the state-action space is continuous, it is infeasible to store Q-values for each {*s*, *a*} point, so we cannot use classical Q-learning.

Instead, we use an incremental Neural Network that learns a continuous **Q-function** Q*(s,a). Once Q* is learnt, the optimal policy is then $\pi^*$ = *argmax*$_a$($Q^*(s,a)$).

The qualities desirable from a Q-Learning Neural Net implementation are,

<img src="images/QL_essentials.png" alt="drawing" width="400"/> <br>
<sup> Source: http://users.cecs.anu.edu.au/~rsl/rsl_papers/99ai.kambara.pdf </sup>


A setback that most naive DQN implementations suffer from is that of poor or non-convergence
of the Q-function.
A reason for this is the correlation between adjacent state-action transitions. For eg. consider a temporal difference update at {s,a}. 
<br>
<img src="images/iid_stateaction.png" alt="drawing" width="500"/> <br>
<sup> Source: ? </sup>
<br>
The update also 'pulls' with it all the Q-values in its neighborhood - a consequence of approximating Q(s,a) with a continuous function.

Two popular rectifications for this problem are :

- **Experience Replay** : Take action based on policy, then update/improve policy based on an i.i.d. sample of 
recently experienced transitions. A drawback is that this cannot be extended to classical RL ideas such as eligibility traces or n-step TD.
- **Network Switching** : Developed by Deepmind and subsequently incorporated into Tensorflow, actions are taken based on one network,
while the target Q-function is stored in another network that's kept frozen for T iterations. At the Tth iteration, both networks are synchronized.
This solves the problem of having to 'chase a moving target'. This method is compatible with multi-step learning methods.

Some specific DQN frameworks, with their drawbacks, are :
- CMAC-based Q-Learning: Does not fulfil *Action Selection* criteria
- Q-AHC: Does not fulfil *Generalization* requirements
- Q-Kohonen, Q-Radial: Piecewise constant actions


