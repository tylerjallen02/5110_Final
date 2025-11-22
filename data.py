import numpy as np
import os
import uuid

class DataBase:
    """
    Stores the data for a **single round** of the game. 
    """
    def __init__(self, n_frames):
        """
        Initializes of database. For speed specifieds initial array size

        Args:
          n_frames: the number of frames intented to be stored
        """
        self.human_scores = np.zeros(n_frames, dtype=np.float64)
        self.machine_scores = np.zeros(n_frames, dtype=np.float64)
        self.human_inputs = np.zeros(n_frames, dtype=np.float64)
        self.machine_inputs = np.zeros(n_frames, dtype=np.float64)
        self.current_frame = 0
        self.warned = False
        
    def append(self, human_input, machine_input, human_score, machine_score):
        """
        Appends data for a single frame of the game.

        The term append is used somewhat loosely here, data should not exceed the allocated
        `n_fames` from the initializer

        Args:
          human_input: numeric human input value for the frame
          machine_input: numeric machine input value for the frame
          human_score: human score for the frame
          machine_score: machine score for the frame
        """
        if self.current_frame >= len(self.human_inputs):
            if not self.warned:
                print("Warning: frames exceed allocated array size. No more data is being stored")
                self.warned = True
            return
        self.human_inputs[self.current_frame] = human_input
        self.machine_inputs[self.current_frame] = machine_input
        self.human_scores[self.current_frame] = human_score
        self.machine_scores[self.current_frame] = machine_score

        self.current_frame += 1

    def _file_hash(self):
        """
        Returns a randomly generated, unique file hash
        """
        LENGTH = 10
        hash = str(uuid.uuid4()).replace('-', '')[:LENGTH]
        return hash
    
    def write(self, round_num):
        """
        Writes the data to a new file under `data/round_{round_num}`.

        Each round will have a unique hash to avoid duplicates
        """
        DATA_DIRECTORY = "data"
        directory = os.path.join(DATA_DIRECTORY, f"round_{round_num}")
        # generate random filename to avoid duplicates
        file_path = os.path.join(directory, f"{self._file_hash()}.npz")

        os.makedirs(directory, exist_ok=True)

        data_to_save: dict[str, np.ndarray] = {
            "human_inputs": self.human_inputs,
            "machine_inputs": self.machine_inputs,
            "human_scores": self.human_scores,
            "machine_scores": self.machine_scores
        }
        
        np.savez_compressed(file_path, **data_to_save, allow_pickle=True)
        
