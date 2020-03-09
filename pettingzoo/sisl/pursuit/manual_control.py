import numpy as np
from .pursuit import env as _env
import time


def manual_control(**kwargs):
    xs = 5
    ys = 5
    obs_range = 3
    n_evaders = 1
    n_pursuers = 2

    # obs_range should be odd 3, 5, 7, etc
    env = _env(n_pursuers=n_pursuers, n_evaders=n_evaders, xs = xs, ys = ys, obs_range = obs_range)

    env.reset()

    done = False
    
    global _quit_loop, _actions, _agent_id
    _quit_loop = np.array([0])
    _actions = np.array([4]*env.num_agents)
    _agent_id = np.array([0])
    
    # ------ controlling pursuers ------ 
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    
    def on_key(event):
        # print('you pressed', event.key)
        if event.key == "escape":
            _quit_loop[0] = 1
            # break
        if event.key == "backspace":
            env.reset()
        if event.key == "j":
            # pressing 'j' moves the focus of control to the next agent
            # control rolls over to the first agent
            _agent_id[0] = (_agent_id[0] + 1) % env.num_agents
        if event.key == "k":
            # pressing 'k' moves the focus of control to the previous agent
            # control rolls over to the lastagent
            _agent_id[0] = (_agent_id[0] - 1) % env.num_agents
        if event.key == "left":
            # p1: left
            _actions[_agent_id[0]] = 0
        if event.key == "right":
            # p1: right
            _actions[_agent_id[0]] = 1
        if event.key == "up":
            # p1: up
            _actions[_agent_id[0]] = 3
        if event.key == "down":
            # p1: down
            _actions[_agent_id[0]] = 2
    
    cid = fig.canvas.mpl_connect('key_press_event', on_key)
    # ------ controlling pursuers ------ 
    
    done = False
    num_frames = 0
    total_reward = 0

    while not done:
        num_frames += 1
        env.render()
        if _quit_loop[0]:
            break
        # actions should be a dict of numpy arrays
        action_dict = dict(zip(env.agents, _actions))
        for a in _actions:
            reward, d, info = env.last()
            obs = env.step(a)
            if d:
                done = True
            total_reward += reward
        print("step reward = ", total_reward, " f: ", num_frames, " d: ", d)
        if done:
            print("Total reward", total_reward, done)
    
        _actions = np.array([4]*env.num_agents)
    

    env.render()
    time.sleep(2)
    env.close()
