

class ObjectAsDictProxy:
    """
    A class that proxies a Python object and behaves like a dictionary.
    Allows access, modification, and deletion of object attributes through dictionary-like syntax.
    """

    def __init__(self, obj):
        """
        Initializes the ObjectProxy.

        Args:
            obj (object): The object to be proxied.
        """
        self._obj = obj

    def __getitem__(self, key):
        """
        Get the value of an object's attribute using dictionary-style syntax.

        Args:
            key (str): The name of the attribute to access.

        Returns:
            object: The value of the attribute.
        
        Raises:
            KeyError: If the attribute does not exist.
        """
        try:
            return getattr(self._obj, key)
        except AttributeError:
            raise KeyError(key)

    def __setitem__(self, key, value):
        """
        Set the value of an object's attribute using dictionary-style syntax.

        Args:
            key (str): The name of the attribute to set.
            value (object): The value to assign to the attribute.
        
        Raises:
            KeyError: If the attribute does not exist.
        """
        try:
            setattr(self._obj, key, value)
        except AttributeError:
            raise KeyError(key)

    def __delitem__(self, key):
        """
        Delete an object's attribute using dictionary-style syntax.

        Args:
            key (str): The name of the attribute to delete.
        
        Raises:
            KeyError: If the attribute does not exist.
        """
        try:
            delattr(self._obj, key)
        except AttributeError:
            raise KeyError(key)
        
    def __contains__(self, key):
        try:
            return getattr(self._obj, key)
        except:
            raise KeyError(key)

    def keys(self, exclude_special=True):
        """
        Get a list of object attributes as dictionary keys.

        Args:
            exclude_special (bool, optional): Exclude special attributes if True. Defaults to False.

        Returns:
            list: A list of attribute names.
        """
        result = []
        for attr in dir(self._obj):
            if not (exclude_special and self.is_attribute_special(attr)):
                result.append(attr)
        return result

    def items(self, exclude_special=True):
        """
        Get a generator of key-value pairs (attribute-value) for the object.

        Args:
            exclude_special (bool, optional): Exclude special attributes if True. Defaults to False.

        Yields:
            tuple: A tuple containing attribute name and its corresponding value.
        """
        for key in self.keys(exclude_special=exclude_special):
            yield (key, self[key])

    def update(self, dictionary:dict, overwrite=True):
        """
        Update object's attributes with key-value pairs from a dictionary.

        Args:
            dictionary (dict): A dictionary containing attribute-value pairs.
        """
        for key, value in dictionary.items():
            if overwrite:
                self[key] = value
            elif key not in self:
                self[key] = value

    def is_attribute_special(self, attr):
        """
        Check if an object's attribute is special.

        Args:
            attr (str): The name of the attribute to check.

        Returns:
            bool: True if the attribute is special, False otherwise.
        """
        return attr in {'__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__'}

    def __len__(self):
        """
        Get the number of object attributes.

        Returns:
            int: The number of attributes.
        """
        return len(self.keys())

    def __repr__(self):
        """
        Get a string representation of the proxy object.

        Returns:
            str: A string representation of the proxied object.
        """
        return repr(self._obj)


"""
# Example usage:
class MyClass:
    def __init__(self):
        self.name = "John"
        self.age = 30

my_object = MyClass()
proxy = ObjectProxy(my_object)

# Access object's attributes as if accessing dictionary keys
print(proxy['name'])  # Output: John
print(proxy['age'])   # Output: 30

# Set object's attributes using dictionary keys
proxy['name'] = "Alice"
print(proxy['name'])  # Output: Alice

# Delete object's attributes using dictionary keys
del proxy['age']
print(proxy.keys())   # Output: ['name']
"""

