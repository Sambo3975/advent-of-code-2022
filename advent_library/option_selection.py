from timeit import timeit


class OptionSelector:
    """A simple option selector"""
    def __init__(self, timed: bool = False):
        """
        Constructor
        :param timed If true, the time the selected option took to execute will be displayed
        """
        self.timed = timed
        self.options = {}
        self.option_order = []

    def add_option(self, key: str, description: str, call):
        """
        Add an option to the selector. Options will be displayed in the order in which they are added
        :param key: User input that will select the option
        :param description: Description of the option
        :param call: Function to call when the option is selected
        :return: None
        """
        if key == 'q':
            raise KeyError("Cannot set a call to 'q'. It is reserved for quitting.")
        self.options[key] = {'description': description, 'call': call}
        self.option_order.append(key)

    def run(self):
        """Run the selector repeatedly until it is exited with an input of 'q'"""
        while True:
            print('Choose an option from below (q to quit)')
            for k in self.option_order:
                print(f'  {k:2s} : {self.options[k]["description"]}')
            print('-----------------------------------------------')
            if (key := input('>> ')) in self.options:
                if self.timed:
                    time = timeit(self.options[key]['call'], number=1)
                    print(f'Completed after {time:.4f} s')
                else:
                    self.options[key]['call']()
            elif key == 'q':
                break
            else:
                print('Invalid input')
            print()
