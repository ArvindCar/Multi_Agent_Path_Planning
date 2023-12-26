# Multi-Agent Path Planning in Dynamic Gridworld
## Introduction
As an individual new to the domain of path planning, this report serves as a journey into some of the conventional path planning methods. The focus of our exploration centers on the applications of A* in multi-agent path planning scenarios, particularly within the context of holonomic robots navigating environments replete with both stationary and dynamic obstacles.

## Gridworld Setup
The grid world game is a very classical application of reinforcement learning. Configured as a 25 x 25 grid, this environment encapsulates essential components crucial for developing and evaluating path planning algorithms. We assume the robot starts in the top left corner of the board, to navigate through the grid to reach the end state. Strategic obstacles, marked in white, are interspersed throughout the grid, posing challenges that necessitate the robot's ability to learn optimal paths while avoiding collisions. Dynamic obstacles, marked in grey, add an additional layer of complexity, as their positions update with each time step. Using a graph-based algorithm like A* allowed us to take advantage of pre-existing knowledge of the environment, to make a more complex grid world, with 6 triangular agents with random start and end states, along with static and dynamic obstacles.
<p align=”center”>
  <img src = "https://github.com/ArvindCar/Multi_Agent_Path_Planning/assets/55990528/3e1d3981-2ca1-4c5a-a4c7-184aa8517975" width = "300" />
  <img src = "https://github.com/ArvindCar/Multi_Agent_Path_Planning/assets/55990528/05ca8d9e-0a31-4574-ad1a-2403b89850cd" width = "300" />
</p>

