import numpy as np
import matplotlib.pyplot as plt


class HouseEnvironment:
    def __init__(self, grid_string):
        self.size = 25
        self.grid = np.zeros((self.size, self.size), dtype=int)
        self.exit = (self.size - 2, self.size - 1)
        self._parse_grid_string(grid_string)

    def _parse_grid_string(self, grid_string):
        lines = grid_string.strip().split('\n')
        for i, line in enumerate(lines):
            for j, char in enumerate(line.strip().split(' ')):
                if char == '#':
                    self.grid[i][j] = 1
        self.grid[self.exit] = 0

    def display(self):
        for row in self.grid:
            print(' '.join(['#' if cell == 1 else '.' for cell in row]))


class QLearningAgent:
    def __init__(self, environment, slip_up_probability):
        self.env = environment
        self.q_table = np.zeros((environment.size, environment.size, 4))
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 0.5
        self.slip_up_probability = slip_up_probability
        self.actions = ['up', 'down', 'left', 'right']
        self.rewards = []

    def train(self, episodes):
        self.rewards = np.zeros(episodes)
        epsilon_decay = 0.99
        min_epsilon = 0.01
        max_iterations = 1000

        for episode in range(episodes):
            state = (1, 1)
            total_reward = 0
            done = False
            for _ in range(max_iterations):
                if np.random.rand() < self.epsilon:
                    action = np.random.choice(self.actions)
                else:
                    action_index = np.argmax(self.q_table[state[0], state[1], :])
                    action = self.actions[action_index]

                next_state, reward, done = self.take_action(state, action)
                total_reward += reward

                old_value = self.q_table[state[0], state[1], self.actions.index(action)]
                next_max = np.max(self.q_table[next_state[0], next_state[1]])
                new_value = (1 - self.learning_rate) * old_value + self.learning_rate * (
                        reward + self.discount_factor * next_max)
                self.q_table[state[0], state[1], self.actions.index(action)] = new_value

                state = next_state

                if done:
                    break

            self.rewards[episode] = total_reward
            self.epsilon = max(min_epsilon, self.epsilon * epsilon_decay)

            progress = (episode + 1) / episodes
            bar_length = 20
            block = int(round(bar_length * progress))
            text = "\rProgress: [{0}] {1:.2f}%".format("#" * block + "-" * (bar_length - block), progress * 100)
            print(text, end="")

        print()

    def take_action(self, state, action):
        if np.random.rand() < self.slip_up_probability:
            action = np.random.choice(self.actions)

        x, y = state
        if action == 'up':
            next_x, next_y = x - 1, y
        elif action == 'down':
            next_x, next_y = x + 1, y
        elif action == 'left':
            next_x, next_y = x, y - 1
        elif action == 'right':
            next_x, next_y = x, y + 1

        if next_x < 0 or next_y < 0 or next_x >= self.env.size or next_y >= self.env.size or self.env.grid[
            next_x, next_y] == 1:
            return (x, y), -100, True
        elif (next_x, next_y) == self.env.exit:
            return (next_x, next_y), 1000, True
        else:
            return (next_x, next_y), -1, False


def draw_normalized_q_table_heatmap(q_table):
    best_q_values = np.max(q_table, axis=2)

    normalized_q_values = (best_q_values - np.min(best_q_values)) / (np.max(best_q_values) - np.min(best_q_values))

    plt.figure(figsize=(10, 10))
    heatmap = plt.imshow(normalized_q_values, cmap='viridis')
    plt.colorbar(heatmap)
    plt.title('Normalized Heatmap of the Q-table')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.show()


grid_string = """
# # # # # # # # # # # # # # # # # # # # # # # # #
# . . . . . . . . . . . . . . . . . . . . . . . #
# . . . . . . . . . . . . . . . . . . . . . . . #
# . . . . . . . . . . . . . . . . . . . . . . . #
# . . . . . . . . . # . . . . # . . . . # . . . #
# . # . . # # # # # # # # # # # # # # # # . . . #
# . # . . # . . . . . . . . . . . . . . . . . . #
# . # # . # . . . . . . . . . . . . . . . . . . #
# . # . . # . . . . . . . . . . . . . . . . . . #
# . # . # # . . . . # . . . . # . . . . # . . . #
# . # . . # . . . # # . # # # # . # # # # . # # #
# . # # . # . . . . . . . . . . . . . . # . . . #
# . # . . # . . . . # . . . . # . . . . # # # . #
# . # . # # . . . . # # # # # # . . . . # . . . #
# . # . . # . . . # # . . . . . # . . . # . # . #
# . # # . # . . . . . . . . . . # # # # # . # # #
# . # . . # . . . . . . . . . . . . . . . . # . #
# . # . # # . . . . . . # . . . . . . . . . . . #
# . # . . # . . . . . . . . . . . . . . . . . . #
# . # # . # # # # # # # # # # # # # # # # . . . #
# . # . . . # . . . # . . . # . . . . . # . . . #
# . # . # . . . # . . . # . . . # . # . . . . . #
# . # # # # # # # # # # # # # # # # # # # . . . #
# . . . . . . . . . . . . . . . . . . . . . . . .
# # # # # # # # # # # # # # # # # # # # # # # # #
"""

house = HouseEnvironment(grid_string)
house.display()

agent = QLearningAgent(house, 0.01)
agent.train(10000)
print(agent.epsilon)

plt.figure(figsize=(12, 6))

plt.plot(agent.rewards, label='Total Reward per Episode')

plt.title('Q-learning Agent Rewards Over Time')
plt.xlabel('Episode')
plt.ylabel('Total Reward (Log Scale)')

plt.legend()
plt.grid(True)
plt.show()
draw_normalized_q_table_heatmap(agent.q_table)
