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

    # It may be worth adding 12/125 to the human equation. This small term will remove any potential
    # negative results from teh human equation.

    # placeholder function to domonstrait mouse movement
    return human_input + 1
