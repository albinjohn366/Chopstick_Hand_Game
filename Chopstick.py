import random


class Chopstick:
    def __init__(self, states):
        self.states = states
        self.player = True
        self.over = False

    def move(self, action):
        # Make the move and make changes
        (row_0, column_0), (row_1, column_1) = action
        temp = list(self.states).copy()
        sum = self.states[row_0][column_0] + self.states[row_1][column_1]
        if sum > 4:
            sum = 0
        self.states = []
        for i in range(2):
            set_list = []
            for j in range(2):
                if (i, j) == (row_1, column_1):
                    set_list.append(sum)
                else:
                    set_list.append(temp[i][j])
            self.states.append(tuple(set_list))

        self.change_player()

    def change_player(self):
        # To change the player after each move
        self.player = not self.player

    @classmethod
    def actions(cls, states, player):
        # Find the available actions for that particular state
        actionss = []
        if player:
            set_1 = [(1, i) for i in range(2) if states[1][i] != 0]
            set_2 = [(0, i) for i in range(2) if states[0][i] != 0]
        else:
            set_1 = [(0, i) for i in range(2) if states[0][i] != 0]
            set_2 = [(1, i) for i in range(2) if states[1][i] != 0]
        for i in set_1:
            for j in set_2:
                actionss.append((i, j))
        return actionss


class Chopstick_AI:
    def __init__(self):
        self.q = dict()
        self.alpha = 0.5

    def get_q_value(self, state, action):
        # Returns the q value for a particular action and state
        if (tuple(state), action) in self.q:
            return self.q[(tuple(state), action)]
        else:
            return 0

    def update_q_value(self, old_q, reward, future_rewards, state, action):
        """Q(s, a) <- old value estimate
        + alpha * (new value estimate - old value estimate)"""
        self.q[(tuple(state), action)] = old_q + self.alpha * (future_rewards +
                                                               reward - old_q)

    def find_future_rewards(self, state, player):
        # Find the best future reward
        actions = Chopstick.actions(state, player)
        if not actions:
            return 0
        ordered_actions = []
        for action in actions:
            ordered_actions.append((self.get_q_value(state, action), action))
        ordered_actions = sorted(ordered_actions, reverse=True)
        return ordered_actions[0][0]

    def update(self, state, action, new_state, reward, player):
        # Updates the q value on the basis of rewards for state and action
        old = self.get_q_value(state, action)
        future_rewards = self.find_future_rewards(new_state, player)
        self.update_q_value(old, reward, future_rewards, state, action)

    def best_action(self, state, player):
        # Returns the best action depending on the q value
        actions = Chopstick.actions(state, player)
        ordered_actions = []
        for action in actions:
            q_value = self.get_q_value(state, action)
            ordered_actions.append((q_value, action))
        ordered_actions = sorted(ordered_actions, reverse=True)
        if not ordered_actions:
            return 0
        return ordered_actions[0][1]

    def train(self, limit):
        # Training the AI for the given limit
        for i in range(limit):
            game = Chopstick(((1, 1), (1, 1)))
            last = dict()
            last['player'] = {'state': None, 'action': None}
            last['ai'] = {'state': None, 'action': None}

            while True:
                # making move using the best action
                state = game.states
                action_set_1 = game.actions(game.states, game.player)
                action_1 = random.choice(action_set_1)
                action_2 = self.best_action(game.states, game.player)
                action = random.choices([action_1, action_2], weights=[0.1,
                                                                       0.9])[0]
                last['player' if game.player else 'ai'] = {'state': state,
                                                           'action': action}
                game.move(action)
                new_state = game.states.copy()

                # Condition for game over
                for item in game.states:
                    if item == (0, 0):
                        game.over = True

                if game.over:
                    self.update(state, action, new_state, 1, game.player)
                    if game.player:
                        self.update(last['player']['state'], last['player'][
                            'action'], new_state, -1, game.player)
                    else:
                        self.update(last['ai']['state'], last['ai'][
                            'action'], new_state, -1, game.player)
                    break
                else:
                    if game.player and last['player']['state']:
                        self.update(last['player']['state'], last['player'][
                            'action'], new_state, 0, game.player)
                    if not game.player and last['ai']['state']:
                        self.update(last['ai']['state'], last['ai'][
                            'action'], new_state, 0, game.player)
            print('Training done {}th time'.format(i + 1))
        self.training = True

    def play(self, states, player):
        action = self.best_action(states, player)
        return action
