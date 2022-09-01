import random
import warnings
import numpy as np


class Animal(object):
    """A general animal class"""

    def __init__(self, name='A', gender=None, strength=None):
        """Define the animal's gender ('M', 'F' are accepted) and strength (int)"""
        if isinstance(name, str):
            self._name = name
        else:
            raise TypeError("Animal name expected to be a string")

        if gender is not None and gender.lower().strip() in ['m', 'f']:
            self._gender = gender
        else:
            self._gender = random.choice(['M', 'F'])

        if isinstance(strength, int) and 0 <= strength <= 9:
            self._strength = strength
        else:
            self._strength = random.randint(0, 9)

    @property
    def name(self):
        return self._name

    @property
    def gender(self):
        return self._gender

    @property
    def strength(self):
        return self._strength

    def __repr__(self):
        return f'{self.name}{self.gender}{self.strength}'

    def __eq__(self, other):
        return type(self) == type(other) and self.gender == other.gender and self.strength == other.strength

    def is_same_type(self, other):
        return type(self) == type(other)

    def is_same_gender(self, other):
        return self.is_same_type(other) and self.gender == other.gender

    def is_same_strength(self, other):
        return self.is_same_type(other) and self.strength == other.strength

    def is_stronger(self, other):
        return self.is_same_type(other) and self.strength > other.strength



class Bear(Animal):
    """A Bear which is the subclass of an animal"""

    def __init__(self, name='B', gender=None, strength=None):
        super().__init__(name=name, gender=gender, strength=strength)


class Fish(Animal):
    """A fish which is a subclass of an animal"""

    def __init__(self, name='F', gender=None, strength=None):
        super().__init__(name=name, gender=gender, strength=strength)

class River(object):
    """Simulation of a river ecosystem with bears and fish interacting"""

    def __init__(self, river_length, bias=[1/3, 1/3, 1/3]):
        """Initialize a river as a list of specified length"""
        self._length = river_length
        self._contents = []
        for i in range(self._length):
            animals = [Bear(), Fish(), None]
            self._contents.append(np.random.choice(a=animals, p=bias))

    def __len__(self):
        """Length of the river's contents; len(self._contents)"""
        return len(self._contents)

    def __getitem__(self, i):
        """Retrieve item at index i"""
        return self._contents[i]

    def __setitem__(self, i, value):
        """Set item at index i"""
        self._contents[i] = value

    def __str__(self):
        """String representation of the river"""
        result = []
        for val in self._contents:
            if val is None:
                result.append('_')
            else:
                result.append(str(val))
        return ' '.join(result)

    @property
    def contents(self):
        return self._contents

    @property
    def length(self):
        return len(self)

    def count(self, val):
        """Return occurences of val in river's contents"""
        if val is None:
            return self._contents.count(None)
        return sum(isinstance(x, val) for x in self._contents)

    def get_positions(self, val):
        """Return a list of indices of val in river's contents"""
        result = []
        for i in range(len(self)):
            if val is None:
                if self._contents[i] is None:
                    result.append(i)
            else:
                if isinstance(self._contents[i], val):
                    result.append(i)
        return result

    def replace(self, add_val, remove_val=None):
        """Replace a 'None' position with an animal instance as represented by add_val"""
        remove_indices = self.get_positions(remove_val)
        if remove_indices:
            remove_index = random.choice(remove_indices)
            self._contents[remove_index] = add_val
        else:
            warnings.warn("No positions left to replace")

    def update_cell(self, i):
        """Update cell as per rules; cell index to update = i"""
        update_success, skip_next_instance, move = True, False, None

        if self._contents[i] is None:  # do nothing if position has None
            pass
        else:
            move = random.randint(-1, 1)  # animal can move backward(-1), stay(0), forward(1)
            if move == 0:  # do nothing if move is zero
                pass
            else:
                curr_pos, curr_ani = i, self._contents[i]

                if i+move < 0:
                    clash_pos, clash_ani = -1, self._contents[-1]
                elif i+move >= len(self):
                    clash_pos, clash_ani = 0, self._contents[0]
                else:
                    clash_pos, clash_ani = i + move, self._contents[i + move]

                if clash_ani is None:  # animal moves without conflict
                    self._contents[curr_pos], self._contents[clash_pos] = None, curr_ani
                    if move == 1:
                        skip_next_instance = True
                else:
                    if curr_ani.is_same_type(clash_ani):
                        if curr_ani.is_same_gender(clash_ani):
                            if curr_ani.is_same_strength(clash_ani):
                                pass  # do nothing since all is equal
                            else:
                                if curr_ani.is_stronger(clash_ani):
                                    self._contents[curr_pos], self._contents[clash_pos] = None, curr_ani
                                    if move == 1:
                                        skip_next_instance = True
                                else:
                                    self._contents[curr_pos], self._contents[clash_pos] = None, clash_ani
                        else:
                            # different genders so make a new instance and leave curr & clash as is
                            self.replace(curr_ani.__class__())
                    else:  # different animals clash
                        if isinstance(curr_ani, Bear) and isinstance(clash_ani, Fish):  # bear moving into fish-- fish dies and bear takes the spot
                            self._contents[curr_pos], self._contents[clash_pos] = None, curr_ani
                            if move == 1:
                                skip_next_instance = True

                        # fish moving into bear-- fish dies and bear stays
                        elif isinstance(curr_ani, Fish) and isinstance(clash_ani, Bear):
                            self._contents[curr_pos] = None

        return update_success, skip_next_instance, move

    def update_river(self):
        """Iteratively update each cell in the river"""
        i = 0
        while i < len(self._contents):
            print(i, '---'*12, i)
            print(self._contents[i], 'Current State', self, sep=' || ')
            update_success, skip_next_instance, move = self.update_cell(i)
            print(self._contents[i], 'After move {}'.format(str(move)), self, sep=' || ')
            if skip_next_instance:
                i += 1
            i += 1
            print()
            print()