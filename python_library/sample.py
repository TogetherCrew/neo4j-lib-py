import os

import numpy as np
from dotenv import load_dotenv


class Sample:
    def __init__(self) -> None:
        pass

    def sample_compute(self, max_value: int = 50) -> int:
        """
        Do a random sample computations

        Parameters:
        ------------
        max_value : int
            a maximum value for generating randome number
            default is set to 50

        Returns:
        --------
        computation_results : int
            the result of computations
        """
        a = np.random.randint(0, max_value)
        b = np.random.randint(0, max_value)

        computation_results = a + b

        return computation_results

    def sample_get_env(self) -> str | None:
        """
        getting an env for example
        the env name is `SAMPLE_ENV`

        Returns:
        ---------
        env_value : str
            the value that was set to env
        """
        load_dotenv()

        env_value = os.getenv("SAMPLE_ENV")

        return env_value
