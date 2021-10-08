#Adapted from https://github.com/qlan3/gym-games
import gym
from gym import spaces

from minatar import Environment


class BaseEnv(gym.Env):
    metadata = {'render.modes': ['human', 'array']}

    def __init__(self, display_time=50, **kwargs):
        self.game_name = 'Game Name'
        self.display_time = display_time
        self.init(**kwargs)

    def init(self, use_minimal_action_set=False, **kwargs):
        self.game = Environment(env_name=self.game_name, **kwargs)
        self.use_minimal_action_set = use_minimal_action_set
        self.action_set = self.game.env.action_map
        if(self.use_minimal_action_set):
            self.action_space = spaces.Discrete(len(self.game.minimal_action_set()))
        else:
            self.action_space = spaces.Discrete(self.game.num_actions())
        self.observation_space = spaces.Box(0.0, 1.0, shape=self.game.state_shape(), dtype=bool)

    def step(self, action):
        if(self.use_minimal_action_set):
            action = self.game.minimal_action_set()[action]
        reward, done = self.game.act(action)
        return (self.game.state(), reward, done, {})

    def reset(self):
        self.game.reset()
        return self.game.state()

    def seed(self, seed=None):
        self.game = Environment(env_name=self.game_name, random_seed=seed)
        return seed

    def render(self, mode='human'):
        if mode == 'array':
            return self.game.state()
        elif mode == 'human':
            self.game.display_state(self.display_time)

    def close(self):
        if self.game.visualized:
            self.game.close_display()
        return 0