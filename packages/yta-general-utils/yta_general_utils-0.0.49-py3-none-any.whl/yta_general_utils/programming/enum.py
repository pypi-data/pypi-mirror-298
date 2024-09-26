from enum import Enum


class YTAEnum(Enum):
    @classmethod
    def is_valid(cls, value):
        """
        This method returns True if the provided 'value' is a valid
        value for the also provided Enum class 'cls', or False if
        not.
        """
        return is_valid(value, cls)
    
    @classmethod
    def get_all(cls):
        """
        This method returns all the existing items in this 'cls' Enum
        class.
        """
        return get_all(cls)
    
    @classmethod
    def get_all_values(cls):
        """
        This method returns all the values of the existing items in 
        this 'cls' Enum class.
        """
        return get_all_values(cls)


def is_valid(value: any, enum: Enum):
    """
    This method returns True if the provided 'value' is a valid value for
    the also provided 'enum' Enum object, or False if not.
    """
    if not value:
        raise Exception('No "value" provided.')
    
    if not issubclass(enum, Enum):
        raise Exception('The "enum" parameter is not an Enum.')

    try:
        enum(type)
        return True
    except Exception:
        return False
    
def get_all(enum: Enum):
    """
    This method returns all the items defined in a Enum subtype that
    is provided as the 'enum' parameter.
    """
    if not enum:
        raise Exception('No "enum" provided.')
    
    if not issubclass(enum, Enum):
        raise Exception('The "enum" parameter provided is not an Enum.')
    
    return [item for item in enum]

@classmethod
def get_all_values(cls):
    """
    Returns a list containing all the registered EnhancementElementMode
    enum values.
    """
    return [item.value for item in get_all(cls)]