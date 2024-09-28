import json

class Saver:
    def __init__(self, file_path="result.json") -> None:
        """
        Saver initialization.
        
        Args:
            file_path (str): File path to save the results
        
        Returns:
            None
        """
        self.file_path = file_path
        self.results = {}
    
    def save(self, iteration, step, data_info, var_info, agent_info) -> None:
        """
        Save the results.
        
        Args:
            iteration (int): Iteration number
            step (int): Step number
            data_info (dict): Data information
            var_info (dict): Variable information
            agent_info (dict): Agent information
            
        Returns:
            None
        """
        if iteration not in self.results:
            self.results[iteration] = {}
        self.results[iteration][step] = {
            "data_info": data_info,
            "var_info": var_info,
            "agent_info": agent_info
        }
    
    def write_results(self) -> None:
        """"
        Write the results to a file.
        
        Args:
            None
        Returns:
            None
        """
        with open(self.file_path, 'w') as file:
            json.dump(self.results, file, indent=4)

