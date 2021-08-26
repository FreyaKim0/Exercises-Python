import random
import time

class DataGenerator:
    # Generate radom values
    def __init__(self, curr_val=0, frequency=20, min=0, max=1, size=400):
        self.__value = {
            'curr_val': curr_val,
            'frequency': frequency,  
            'val_to_mult': 1}  # Value to multiply to the random value which will be added
        self.__max = max 
        self.__min = min 
        self.__size = size 

    # Private method that generates data
    def __generate_values(self):
        if self.__value['frequency'] > 0:  # If the frequency is greater than 0
            self.__value['frequency'] -= 1  # Decrease frequency by 1

            # Add a random number which is multiplied by 'val_to_mult'
            # When 'val_to_mult' is positive y value increases
            self.__value['curr_val'] += (random.randint(0, 1)) * self.__value['val_to_mult']
            # If current value is less than min value, set the current value to min value
            # and flip the incrementer
            if self.__value['curr_val'] < self.__min:
                self.__value['val_to_mult'] = 1
                self.__value['curr_val'] = self.__min
            # If current value is greater than max value, set the current value to max value
            # and flip the incrementer
            elif self.__value['curr_val'] > self.__max:
                self.__value['val_to_mult'] = -1
                self.__value['curr_val'] = self.__max
        else:
            # Reset the frequency
            self.__value['frequency'] = round(random.gauss(30, 20))
            # Multiply -1 to 'val_to_mult'
            self.__value['val_to_mult'] *= -1
        # Return the current value adding the small random number to make some squiggles
        return self.__value['curr_val'] + random.randint(-1, 1)

    # Property that returns a list of values
    @property
    def values(self):
        return [self.__generate_values() for _ in range(self.__size)]

curr_val = DataGenerator(min=15, max=40, size=1).values[0]

# Create data
def create_data(date, location):
    global curr_val
    # randomly choose a generated value
    value = DataGenerator(min=15, max=40, curr_val=curr_val, size=1).values[0]
    # update the current value
    curr_val = value
    datadict = {
        "num_students": value,
        "date": date,
        "location": location,
        "time_created": time.asctime()
    }
    return datadict