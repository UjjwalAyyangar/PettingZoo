from . import shogi_utils
import shogi

from pettingzoo import AECEnv
from gym import spaces
import numpy as np
import warnings
from pettingzoo.utils.agent_selector import agent_selector
from pettingzoo.utils import wrappers

def env():
    env = raw_env()
    env = wrappers.TerminateIllegalWrapper(env, illegal_reward=-1)
    env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.NaNRandomWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    return env

class raw_env(AECEnv):
    metadata = {'render.modes':['human']}

    def __init__(self):
        super().__init()
        self.board = shogi.Board()
        self.agents = ["player_{}".format(i) for i in range(2)]
        self._agent_selector = agent_selector(self.agents)

        self.action_spaces = {name: spaces.Discrete(9*9*139) for name in self.agents}
        self.observation_spaces = {name: spaces.Box(
            low=0, high=1, shape=(9, 9, 20),
            dtype=np.bool) for name in self.agents}

        self.rewards = None
        self.dones = None
        self.infos = {name: {} for name in self.agents}

        self.agent_selection = None
        self.num_agents = len(self.agents)


    def observe(self, agent):
        return shogi_utils.get_observation(self.board, self.agents.index(agent))

    def reset(self, observe=True):
        self.has_reset = True
        
        self.board = shogi.Board()
        
        self.agent_selection = self._agent_selector.reset()

        self.rewards = {name: 0 for name in self.agents}
        self.dones = {name: False for name in self.agents}
        self.infos = {name : {'legal_moves':[]} for name in self.agents}
        self.infos[self.agent_selection]['legal_moves'] = shogi_utils.legal_moves(self.board)

        if observe:
            return self.observe(self.agent_selection)
        else:
            return



    def set_game_result(self, result_val):
        for i, name in enumerate(self.agents):
            self.dones[name] = True
            result_coef = 1 if i==0 else -1
            self.rewards[name] = result_val * results_coef
            self.infos[name] = {'legal_moves': []}


    def step(self, action, observe=True):
        current_agent = self.agent_selection
        current_index = self.agents.index(current_agent)
        self.agent_selection = next_agent = self._agent_selector.next()


        chosen_move = shogi_utils.legal_moves(self.board)
        assert chosen_move in self.board.legal_moves
        self.board.push(chosen_move)


        next_legal_moves = shogi_utils.legal_moves(self.board)
        
        is_stale_or_checkmate = self.board.is_stalemate() or self.board.is_game_over()
        #not any(next_legal_moves)


        # need to comeback here

        is_repetition = self.board.is_fourfold_repetition()
        is_suicide = self.board.is_suicide_or_check_by_dropping_pawn()

        game_over = self.is_game_over()

        if game_over:
            result = self.board.result(claim_draw=True)
            result_val = shogi_utils.result_to_int(result)
            self.set_game_result(result_val)

        else:
            self.infos[current_agent] = {'legal_moves': []}
            self.infos[next_agent] = {'legal_moves': next_legal_moves}
            assert len(self.infos[next_agent]['legal_moves'])


        if observe:
            next_observation = self.observe(next_agent)
        else:
            next_observation = None

        return next_observation

    def render(self, mode='human'):
        print(self.board)


    def close(self):
        pass






























        
