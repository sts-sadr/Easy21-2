from dealer import dealer
from state import State
from random import randint, random
import logging

__author__ = 'sudhanshu mittal'


class Env(object):

    HIT = 0
    STICK = 1

    def draw_card(self):
        def draw_black_card():
            return randint(1, 10)
    
        def draw_red_card():
            return -randint(1, 10)
        
        probability = random()
        card = None
        if probability <= float(2) / 3:
            card = draw_black_card()
        else:
            card = draw_red_card()
        logging.info("card drawn: "+str(card))
        return card

    def is_bust(self, score):
        return score < 1 or score > 21

    def get_reward(self, player, dealer):
        reward = 0
        if self.is_bust(player):
            reward = -1
        elif self.is_bust(dealer):
            reward = 1
        else:
            if player > dealer:
                # player wins
                reward = 1
            elif player < dealer:
                # player loses
                reward = -1
            else:
                # draw match
                reward = 0
        return reward
    def step(self, state, action):
        """
        :param state: State
        :param action: 0 (self.hit) or 1 (self.stick)
        :rtype : State next_state, int reward, boolean done
        """
        # check arguments' type
        assert isinstance(state, State), 'First argument should be State!'
        assert action in [self.HIT, self.STICK], action

        player = state.player
        dealer = state.dealer
        done = False
        
        if action == self.HIT:
            logging.info("player chose to hit")
            player += self.draw_card()
            if self.is_bust(player):
                done = True
                logging.info("player went bust")

        elif action == self.STICK:
            logging.info("player chose to stick. Dealer will play now...")
            next_dealer_action = self.HIT
            while not self.is_bust(dealer) and next_dealer_action == self.HIT:
                dealer += self.draw_card()
                next_dealer_action = self.dealer.get_action(dealer);
            if self.is_bust(dealer):
                logging.info("dealer went bust")
            done = True

        reward = self.get_reward(player, dealer)
        return State(dealer, player), reward, done

    def __init__(self):
        self.dealer = dealer();
