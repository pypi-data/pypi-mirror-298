import random
import math
import hashlib
import argparse
from abc import ABC, abstractmethod

# from ... import logger
import logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger('MyLogger')

SCALAR=1/(2*math.sqrt(2.0))

class MCTSState(ABC):
    MOVES=[]
    num_moves=len(MOVES)
    def __init__(self):
        ...

    def next_state(self):
        ...

    def terminal(self):
        ...

    def reward(self):
        ...

    def __hash__(self):
        ...

    def __eq__(self,other):
        ...

    def __repr__(self):
        ...

class MCTSNode:
	def __init__(self, state, parent=None):
		self.visits=1
		self.reward=0.0	
		self.state=state
		self.children=[]
		self.parent=parent	
	def add_child(self,child_state):
		child=MCTSNode(child_state,self)
		self.children.append(child)
	def update(self,reward):
		self.reward+=reward
		self.visits+=1
	def fully_expanded(self, num_moves_lambda):
		num_moves = self.state.num_moves
		if num_moves_lambda is not None:
			num_moves = num_moves_lambda(self)
		if len(self.children)==num_moves:
			return True
		return False
	def __repr__(self):
		s="Node; children: %d; visits: %d; reward: %f"%(len(self.children),self.visits,self.reward)
		return s

class MCTS:
    @classmethod
    def UCTSearch(cls, budget, root, num_moves_lambda = None):
        for iter in range(int(budget)):
            if iter%10000==9999:
                logger.info("simulation: %d"%iter)
                logger.info(root)
            front=cls.tree_policy(root, num_moves_lambda)
            reward=cls.default_policy(front.state)
            cls.backup(front,reward)
        return cls.best_child(root,0)

    @classmethod
    def tree_policy(cls, node, num_moves_lambda):
        #a hack to force 'exploitation' in a game where there are many options, and you may never/not want to fully expand first
        while not node.state.terminal():
            if len(node.children)==0:
                return cls.expand(node)
            elif random.uniform(0,1)<.5:
                node=cls.best_child(node,SCALAR)
            else:
                if not node.fully_expanded(num_moves_lambda):	
                    return cls.expand(node)
                else:
                    node=cls.best_child(node,SCALAR)
        return node

    @staticmethod
    def expand(node):
        tried_children=[c.state for c in node.children]
        new_state=node.state.next_state()
        while new_state in tried_children and not new_state.terminal():
            new_state=node.state.next_state()
        node.add_child(new_state)
        return node.children[-1]

    #current this uses the most vanilla MCTS formula it is worth experimenting with THRESHOLD ASCENT (TAGS)
    @staticmethod
    def best_child(node,scalar):
        bestscore=0.0
        bestchildren=[]
        for c in node.children:
            exploit=c.reward/c.visits
            explore=math.sqrt(2.0*math.log(node.visits)/float(c.visits))	
            score=exploit+scalar*explore
            if score==bestscore:
                bestchildren.append(c)
            if score>bestscore:
                bestchildren=[c]
                bestscore=score
        if len(bestchildren)==0:
            logger.warn("OOPS: no best child found, probably fatal")
        return random.choice(bestchildren) if bestchildren != [] else None

    @staticmethod
    def default_policy(state):
        while state.terminal()==False:
            state=state.next_state()
        return state.reward()

    @staticmethod
    def backup(node,reward):
        while node!=None:
            node.visits+=1
            node.reward+=reward
            node=node.parent
        return None

if __name__=="__main__":
    class TESTState(MCTSState):
        NUM_TURNS = 10	
        GOAL = 0
        MOVES=[2,-2,3,-3]
        MAX_VALUE= (5.0*(NUM_TURNS-1)*NUM_TURNS)/2
        num_moves=len(MOVES)
        def __init__(self, value=0, moves=[], turn=NUM_TURNS):
            self.value=value
            self.turn=turn
            self.moves=moves
        def next_state(self):
            nextmove=random.choice([x*self.turn for x  in self.MOVES])
            next=TESTState(self.value+nextmove, self.moves+[nextmove],self.turn-1)
            return next
        def terminal(self):
            if self.turn == 0:
                return True
            return False
        def reward(self):
            r = 1.0-(abs(self.value-self.GOAL)/self.MAX_VALUE)
            return r
        def __hash__(self):
            return int(hashlib.md5(str(self.moves).encode('utf-8')).hexdigest(),16)
        def __eq__(self,other):
            if hash(self)==hash(other):
                return True
            return False
        def __repr__(self):
            s="Value: %d; Moves: %s"%(self.value,self.moves)
            return s

    parser = argparse.ArgumentParser(description='MCTS research code')
    parser.add_argument('--num_sims', action="store", required=True, type=int)
    parser.add_argument('--levels', action="store", required=True, type=int, choices=range(TESTState.NUM_TURNS+1))
    args=parser.parse_args()

    current_node=MCTSNode(TESTState())
    for l in range(args.levels):
        current_node=MCTS.UCTSearch(args.num_sims/(l+1),current_node)
        print("level %d"%l)
        print("Num Children: %d"%len(current_node.children))
        for i,c in enumerate(current_node.children):
            print(i,c)
        print("Best Child: %s"%current_node.state)
		# while current_node is not None:
		# 	print("Best Child: %s"%current_node.state)
		# 	current_node = MCTS.best_child(current_node, 0)
        print("--------------------------------")
    # Command: python src/fastmindapi/algo/tree/mcts.py --num_sims 10000 --levels 8 