import gym
import numpy as np

from hyperparameters import BATCH_SIZE


class Environment:
    def __init__(self, problem, should_render=False):
        self.problem = problem
        self.env = gym.make(problem)
        self.should_render = should_render

    def number_of_states(self):
        return self.env.observation_space.shape[0]

    def number_of_actions(self):
        return self.env.action_space.n

    def reshape_state(self, state):
        return np.reshape(state, [1, self.number_of_states()])

    def close(self):
        self.env.close()

    def run_episode(self, agent):
        state = self.reshape_state(self.env.reset())
        total_reward = 0
        number_of_frames = 0
        while True:
            number_of_frames += 1
            if self.should_render:
                self.env.render()

            action = agent.act(state)

            state_prime, reward, done, info = self.env.step(action)
            state_prime = self.reshape_state(state_prime)

            agent.observe((state, action, reward, state_prime, done))
            if agent.memory.length() > BATCH_SIZE:
                agent.replay()

            state = state_prime
            total_reward += reward

            if done:
                break

        agent.brain.target_model_update()
        agent.update_epsilon()
        return total_reward, number_of_frames