from tqdm import tqdm

from .market import Market
from .agents.buyer import create_buyer
from .simulator import run_sim
from .logger import Saver


class Runner:
    def __init__(self, settings, logger) -> None:
        """
        Runner initialization.
        
        Args:
            settings (dict): Settings
            logger (Saver): Saver instance
        
        Returns:
            None
        """
        self.settings = settings
        self.logger = logger
    
    def main(self) -> None:
        """
        Main function to run the simulation.
        
        Args:
            None
        
        Returns:
            None
        """
        # default settings
        default_settings = {
            "Simulation": {
                "num_iterations": 1,
                "num_steps": 5,
                "isPrice": False
            },
            "Market": {
                "model": None
            },
            "Agent": {
                "num_buyers": 10,
                "strategy_weights": {
                    "random": 0.4,
                    "related": 0.3,
                    "ranking": 0.3
                },
                "new_buyer_probability": 0
            }
        }
        
        # merge default settings and user settings
        settings = {**default_settings, **self.settings}
        num_iterations = settings["Simulation"]["num_iterations"]
        num_steps = settings["Simulation"]["num_steps"]
        isPrice = settings["Simulation"]["isPrice"]
        num_buyers = settings["Agent"]["num_buyers"]
        strategy_weights = settings["Agent"]["strategy_weights"]
        probability = settings["Agent"]["new_buyer_probability"]
        
        # market model
        if settings["Market"]["model"] is None:
            raise ValueError("Market model must be provided in settings.")
        G = settings["Market"]["model"]
        
        
        for i in tqdm(range(num_iterations)):
            # create Market instance
            market = Market(G)
        
            # create buyers list
            buyers = [create_buyer(strategy_weights, market) for _ in range(num_buyers)]
            
            # create Saver instance
            saver = Saver()
            
            # run simulation
            results = run_sim(buyers, market, num_steps, isPrice, strategy_weights, probability)
            
            # save results
            for step, data in results.items():
                self.logger.save(i, step, data["data_info"], data["var_info"], data["agent_info"])
        
        self.logger.write_results()