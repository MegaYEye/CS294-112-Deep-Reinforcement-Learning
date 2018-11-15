import numpy as np
from gym import spaces
from gym import Env


class PointEnv(Env):
    """
    point mass on a 2-D plane
    goals are sampled randomly from a square
    """

    def __init__(self, num_tasks=1):
        self.reset_task()
        self.reset()
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(2,))
        self.action_space = spaces.Box(low=-0.1, high=0.1, shape=(2,))


    def reset_task(self, generalized=False, granularity=1, is_evaluation=False):
        '''
        sample a new task randomly

        Problem 3: make training and evaluation goals disjoint sets
        if `is_evaluation` is true, sample from the evaluation set,
        otherwise sample from the training set
        '''
        #====================================================================================#
        #                           ----------PROBLEM 3----------
        #====================================================================================#
        # YOUR CODE HERE
        # Construct the chessboard space with 20 x 20
        # The granularity is the size of squares, the value can be chosen from [1, 2, 4, 5, 10]
        if generalized:  
            print("Problem 3...")  
            print("The size of square is ", granularity)       
            size = int(20 / granularity)
            space = np.zeros((size, size))
            space[1::2,::2] = 1
            space[::2,1::2] = 1
            if is_evaluation:
                dataset = np.where(space == 1)
            else:
                dataset = np.where(space == 0)

            dataset = np.asarray(dataset).T
            nums = dataset.shape[0]
            idx = np.random.randint(0, nums)
            if is_evaluation:
                print("Evaluation")
            else:
                print("training")

            goal = dataset[idx]
            goal[0] = goal[0] * granularity
            goal[1] = goal[1] * granularity

            x = np.random.uniform(goal[0], goal[0] + granularity) - 10
            y = np.random.uniform(goal[1], goal[1] + granularity) - 10
            print((x, y))
        else:
            #print("Problem 2...")
            x = np.random.uniform(-10, 10)
            y = np.random.uniform(-10, 10)

        self._goal = np.array([x, y])

        #x = np.random.uniform(-10, 10)
        #y = np.random.uniform(-10, 10)
        #self._goal = np.array([x, y])

    def reset(self):
        self._state = np.array([0, 0], dtype=np.float32)
        return self._get_obs()

    def _get_obs(self):
        return np.copy(self._state)

    def reward_function(self, x, y):
        return - (x ** 2 + y ** 2) ** 0.5

    def step(self, action):
        x, y = self._state
        # compute reward, add penalty for large actions instead of clipping them
        x -= self._goal[0]
        y -= self._goal[1]
        # check if task is complete
        done = abs(x) < .01 and abs(y) < .01
        reward = self.reward_function(x, y)
        # move to next state
        self._state = self._state + action
        ob = self._get_obs()
        return ob, reward, done, dict()

    def viewer_setup(self):
        print('no viewer')
        pass

    def render(self):
        print('current state:', self._state)

    def seed(self, seed):
        np.random.seed = seed
