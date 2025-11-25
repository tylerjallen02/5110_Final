def get_human_cost(human_input, machine_input):
    """
    Calculates human cost from 3D quadratic equation

    Args:
      humans_input: input from the human agent in the range [-1, 1]
      machine_input: input from the machine agent in the range [-1, 1]
    Returns:
      returns the cost of the human player. Output is in the range [0, 596 / 375]
    """

    # TODO fully implement. Note that the actual values could be slightly negative. It may
    # dummy function should be replaced with actual equation

    # It may be worth adding 12/125 
    return (1 / 2) * human_input ** 2 \
        + (7 / 30)  * machine_input ** 2 \
        - (1/3) * human_input * machine_input \
        + (2 / 15) * human_input  \
        - (22/ 75) * machine_input

def get_machine_cost(human_input, machine_input):
    """
    Calculates macine cost from 3D quadratic equation

    Args:
      humans_input: input from the human agent in the range [-1, 1]
      machine_input: input from the machine agent in the range [-1, 1]
    Returns:
      returns the cost of the human player. Output has minium of 0
    """
    return (1 / 2) * machine_input ** 2 \
        + human_input ** 2 \
        - human_input * machine_input