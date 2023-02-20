"""Alchemy."""

class AlchemicalElement:
    """
    AlchemicalElement class.

    Every element must have a name.
    """

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"<AE: {self.name}>"


class AlchemicalStorage:
    """AlchemicalStorage class."""

    def __init__(self):
        """
        Initialize the AlchemicalStorage class.

        You will likely need to add something here, maybe a list?
        """
        self.elements = []

    def add(self, element: AlchemicalElement):
        """
        Add element to storage.

        Check that the element is an instance of AlchemicalElement, if it is not, raise the built-in TypeError exception.

        :param element: Input object to add to storage.
        """

    def pop(self, element_name: str) -> AlchemicalElement | None:
        """
        Remove and return previously added element from storage by its name.

        If there are multiple elements with the same name, remove only the one that was added most recently to the
        storage. If there are no elements with the given name, do not remove anything and return None.

        :param element_name: Name of the element to remove.
        :return: The removed AlchemicalElement object or None.
        """
        return None

    def extract(self) -> list[AlchemicalElement]:
        """
        Return a list of all of the elements from storage and empty the storage itself.

        Order of the list must be the same as the order in which the elements were added.

        Example:
            storage = AlchemicalStorage()
            storage.add(AlchemicalElement('Water'))
            storage.add(AlchemicalElement('Fire'))
            storage.extract() # -> [<AE: Water>, <AE: Fire>]
            storage.extract() # -> []

        In this example, the second time we use .extract() the output list is empty because we already extracted everything.

        :return: A list of all of the elements that were previously in the storage.
        """
        return []

    def get_content(self) -> str:
        """
        Return a string that gives an overview of the contents of the storage.

        Example:
            storage = AlchemicalStorage()
            storage.add(AlchemicalElement('Water'))
            storage.add(AlchemicalElement('Fire'))
            print(storage.get_content())

        Output in console:
            Content:
             * Fire x 1
             * Water x 1

        The elements must be sorted alphabetically by name.

        :return: Content as a string.
        """
        return ''


if __name__ == '__main__':
    element_one = AlchemicalElement('Fire')
    element_two = AlchemicalElement('Water')
    element_three = AlchemicalElement('Water')
    storage = AlchemicalStorage()

    print(element_one)  # <AE: Fire>
    print(element_two)  # <AE: Water>

    storage.add(element_one)
    storage.add(element_two)

    print(storage.get_content())
    # Content:
    #  * Fire x 1
    #  * Water x 1

    print(storage.extract())  # [<AE: Fire>, <AE: Water>]
    print(storage.get_content())
    # Content:
    #  Empty

    storage.add(element_one)
    storage.add(element_two)
    storage.add(element_three)

    print(storage.pop('Water') == element_three)  # True
    print(storage.pop('Water') == element_two)  # True
