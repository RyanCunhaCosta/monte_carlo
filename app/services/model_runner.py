class ModelRunner:
    """
    A class to manage cost functions and constraints for a model.

    Attributes:
        inputs (dict): A dictionary containing input parameters for each cost function.
        pd (float): The power demand parameter.
        cost_functions (dict): A dictionary mapping keys to cost functions generated based on input parameters.
    """

    def __init__(self, inputs, pd):
        """
        Initializes the ModelRunner with inputs and power demand.

        Args:
            inputs (dict): A dictionary containing parameters for each cost function.
            pd (float): The power demand.

        """
        self.inputs = inputs
        self.pd = pd
        self.cost_functions = self._generate_cost_functions()

    def _generate_cost_functions(self):
        """
        Generates cost functions based on input parameters.

        Returns:
            dict: A dictionary mapping keys to generated cost functions.
        """

        def cost_function_generator(c_base, c_lin, c_quad):
            """
            Generates a cost function based on quadratic parameters.

            Args:
                c_base (float): Base cost coefficient.
                c_lin (float): Linear cost coefficient.
                c_quad (float): Quadratic cost coefficient.

            Returns:
                function: Cost function that calculates cost based on input power.

            """

            def cost(P):
                return c_base + c_lin * P + c_quad * P**2

            return cost

        return {
            key: cost_function_generator(
                params["c_base"], params["c_lin"], params["c_quad"]
            )
            for key, params in self.inputs.items()
        }

    def C_total(self, x):
        """
        Calculates the total cost based on the input vector x.

        Args:
            x (list): List of power values.

        Returns:
            float: Total cost based on the input power values.

        """
        return sum(
            self.cost_functions[key](x[i]) for i, key in enumerate(self.cost_functions)
        )

    def constraint(self, x):
        """
        Evaluates the constraint based on the input vector x.

        Args:
            x (list): List of power values.

        Returns:
            float: The difference between total generation and losses minus power demand.

        """
        total_generation = sum(x)
        losses = sum(
            self.inputs[key]["p_l_quad"] * x[i] ** 2
            for i, key in enumerate(self.inputs)
        )
        return total_generation - losses - self.pd

    def limits(self):
        """
        Retrieves the limits for power generation based on input parameters.

        Returns:
            list: A list of tuples containing minimum and maximum power generation limits.

        """
        return [
            (params["p_g_min"], params["p_g_max"]) for params in self.inputs.values()
        ]
