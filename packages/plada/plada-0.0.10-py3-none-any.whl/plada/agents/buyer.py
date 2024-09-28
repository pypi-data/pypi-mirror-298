import random

from enum import Enum


class Buyer:
    def __init__(self, strategies, weights, **kwargs) -> None:
        """
        buyer initialization.
        
        Args:
            strategies (list): List of strategy instances.
            weights (list): List of weights for each strategy.
            utility_threshold (float): Utility threshold for waiting state.
            purchase_limit (int): Purchase limit.
        
        Returns:
            None
        """
        self.purchased_data = []
        self.step_purchased_data = None
        self.asset = 200
        self.strategies = strategies
        self.weights = weights
        self.utility = 1
        self.total_vars = set()
        self.state = BuyerState.ACTIVE 
        self.utility_threshold = kwargs.get("utility_threshold", 0)
        self.purchase_limit = kwargs.get("purchase_limit", 10)
        self.waiting_steps = 0
    
    def purchase(self, G, market, isPrice) -> int:
        """
        Purchase data.
        
        Args:
            G (nx.Graph): Data graph.
            market (Market): Market instance.
            isPrice (bool): Whether to consider price.
        
        Returns:
            node (int): Data ID.
        """
        # check state
        self.check_state()
        
        # if the buyer is not active, return None
        if self.state == BuyerState.EXITED:
            return None
        if self.state == BuyerState.WAITING:
            return None
        
        # if the buyer is active, purchase data
        # select strategy
        strategy = random.choices(self.strategies, weights=self.weights, k=1)[0]
        
        # select data
        node = strategy.select_data(G, self.purchased_data)
        
        # check if the buyer can afford the data 
        if isPrice and not self.can_afford(market, node):
            return None
        
        # check if the buyer has already purchased the data
        if node in self.purchased_data:
            return None
        
        # if the buyer can purchase the data, update the purchased data
        self.step_purchased_data = node
        
        # update utility
        self.update_utility(market, node)
        
        # if considering price, update asset
        if isPrice:
            self.update_asset(market, node)
        
        return node
    
    def can_afford(self, market, data_id) -> bool:
        """
        Check if the buyer can afford the data.
        
        Args:
            market (Market): Market instance.
            data_id (int): Data ID.
        
        Returns:
            bool: Whether the buyer can afford the data.
        """
        data_price = market.datasets[data_id].price
        return data_price <= self.asset
    
    def update_asset(self, market, data_id) -> None:
        """
        Update the buyer's asset.
        
        Args:
            market (Market): Market instance.
            data_id (int): Data ID.
        
        Returns:
            None
        """
        data_price = market.datasets[data_id].price
        self.asset -= data_price
    
    def update_utility(self, market, data_id) -> None:
        """
        Update the buyer's utility.
        
        Args:
            market (Market): Market instance.
            data_id (int): Data ID.
        
        Returns:
            None
        """
        current_data_vars = set(market.datasets[data_id].variables.keys())
        # 1st purchase
        if not self.purchased_data:
            self.utility = 0
        # 2nd purchase and later
        else:
            dice_coefficient = self.calc_dice_coefficient(self.total_vars, current_data_vars)
            tag_similarity = self.calc_tag_similarity(market, data_id)
            utility = dice_coefficient + tag_similarity
            self.utility += utility
        
        # update total_vars
        self.total_vars.update(current_data_vars)
    
    def calc_dice_coefficient(self, vars_set1, vars_set2) -> float:
        """
        Calculate the Dice coefficient of variables between two data.
        
        Args:
            vars_set1 (set): Set of variables of data 1.
            vars_set2 (set): Set of variables of data 2.
        
        Returns:
            float: Dice coefficient.
        """
        intersection = vars_set1 & vars_set2
        union = vars_set1 | vars_set2
        if len(union) == 0:
            return 0
        return 2 * len(intersection) / len(union)
    
    def calc_tag_similarity(self, market, data_id) -> float:
        """
        Calculate the similarity of tags between the current data and past purchased data.
        
        Args:
            market (Market): Market instance.
            data_id (int): Data ID.
        
        Returns:
            float: Tag similarity.
        """
        # 1st purchase
        if not self.purchased_data:
            return 0
        
        total_sim = 0
        total_weight = 0
        num_purchased = len(self.purchased_data)
        
        # weighting based on the purchase order (the first purchase has the highest weight)
        for i, purchased_data in enumerate(self.purchased_data):
            current_data = market.datasets[data_id]
            past_data = market.datasets[purchased_data]
            
            weight = (i + 1) / num_purchased
            
            # compare parent and child tags
            if current_data.parent_tag == past_data.parent_tag:
                if current_data.child_tag == past_data.child_tag:
                    total_sim += weight * 1
                else:
                    total_sim += weight * 0.5
            else:
                total_sim += weight * 0
            
            total_weight += weight
            
        return total_sim / total_weight
    
    def check_state(self) -> None:
        """
        Check the buyer's state and update the state.
        
        Args:
            None
        
        Returns:
            None
        """
        # if the buyer's asset is less than 10, change the state to EXITED
        if self.asset <= 10:
            self.state = BuyerState.EXITED
            return
        
        # if the buyer's utility is less than the utility threshold, change the state to WAITING
        if self.utility < self.utility_threshold:
            self.state = BuyerState.WAITING
            self.waiting_steps = 5
            return
        
        # if the buyer has already purchased the maximum number of data, change the state to EXITED
        if len(self.purchased_data) >= self.purchase_limit:
            self.state = BuyerState.EXITED
            return
        
        # if the buyer's state is WAITING, decrease the waiting steps
        if self.state == BuyerState.WAITING:
            if self.waiting_steps > 0:
                self.waiting_steps -= 1
            else:
                self.state = BuyerState.ACTIVE
    
    def end_step(self) -> None:
        """
        End the step.
        
        Args:
            None
        
        Returns:
            None
        """
        if self.step_purchased_data is not None:
            self.purchased_data.append(self.step_purchased_data) # update purchased data at the end of the step
        self.step_purchased_data = None


class BuyerState(Enum):
    ACTIVE = 1
    WAITING = 2
    EXITED = 3


class RandomStrategy:
    def select_data(self, G, _) -> int:
        """
        Select data randomly.
        
        Args:
            G (nx.Graph): Data graph.
            
        Returns:
            node (int): Data ID.
        """
        return random.choice(list(G.nodes()))


class RelatedStrategy:
    def __init__(self, market) -> None:
        """
        related strategy initialization.
        
        Args:
            market (Market): Market instance.
        
        Returns:
            None
        """
        self.market = market
    
    def select_data(self, G, purchased_data) -> int:
        """
        Select data based on the related strategy.
        
        Args:
            G (nx.Graph): Data graph.
            purchased_data (list): List of purchased data.
        
        Returns:
            node (int): Data ID.
        """
        # 1st purchase
        if not purchased_data:
            return random.choice(list(G.nodes()))
        
        # 2nd purchase and later
        else:
            last_purchased_data = purchased_data[-1] # the last purchased data
            neighbors = list(G.neighbors(last_purchased_data))
            # if neighbors exist
            if neighbors:
                probabilities = self.calc_probabilities(G, neighbors)
                return random.choices(neighbors, weights=[probabilities[node] for node in neighbors])[0]
            # if neighbors do not exist
            else:
                return random.choice(list(G.nodes()))
    
    def calc_probabilities(self, G, target_nodes):
        # calculate the purchase count of the target nodes
        total_purchase_count = sum(self.market.datasets[node].purchase_count for node in target_nodes)
        if total_purchase_count == 0:
            return {node: 1 / len(target_nodes) for node in target_nodes}
        probabilities = {node: (self.market.datasets[node].purchase_count + 1) / (total_purchase_count + len(target_nodes)) for node in target_nodes}
        
        # normalize the probabilities
        total_prob = sum(probabilities.values())
        return {node: prob / total_prob for node, prob in probabilities.items()}


class RankingStrategy:
    def __init__(self, market) -> None:
        """
        ranking strategy initialization.
        
        Args:
            market (Market): Market instance.
        
        Returns:
            None
        """
        self.market = market
    
    def select_data(self, G, _) -> int:
        """
        Select data based on the ranking strategy.
        
        Args:
            G (nx.Graph): Data graph.
            
        Returns:
            node (int): Data ID.
        """
        # calculate the probabilities of each data
        probabilities = self.calc_probabilities(G)
        
        # select data based on the probabilities
        weights = [probabilities[node] for node in list(G.nodes())]
        return random.choices(list(G.nodes()), weights=weights, k=1)[0]
    
    def calc_probabilities(self, G) -> dict:
        """
        Calculate the probabilities of each data.
        
        Args:
            G (nx.Graph): Data graph.
        
        Returns:
            probabilities (dict): Probabilities of each data.
        """
        total_purchase_count = sum(self.market.datasets[node].purchase_count for node in G.nodes())
        if total_purchase_count == 0:
            return {node: 1 / len(G.nodes()) for node in G.nodes()}
        probabilities = {node: (self.market.datasets[node].purchase_count + 1) / (total_purchase_count + len(G.nodes())) for node in G.nodes()}
        
        # normalize the probabilities
        total_prob = sum(probabilities.values())
        return {node: prob / total_prob for node, prob in probabilities.items()}


def create_buyer(strategy_weights, market) -> Buyer:
    """
    Create a buyer instance.
    
    Args:
        strategy_weights (dict): Dictionary of strategy names and weights.
        market (Market): Market instance.
    
    Returns:
        buyer (Buyer): Buyer instance.
    """
    # create strategy instances
    random_strategy = RandomStrategy()
    related_strategy = RelatedStrategy(market)
    ranking_strategy = RankingStrategy(market)
    
    # create a dictionary of strategies
    strategies = {
        "random": random_strategy,
        "related": related_strategy,
        "ranking": ranking_strategy
    }
    
    strategy_list = []
    weight_list = []
    
    for strategy, weight in strategy_weights.items():
        strategy_list.append(strategies[strategy])
        weight_list.append(weight)
    
    return Buyer(strategy_list, weight_list)