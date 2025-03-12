from torch.optim.optimizer import required


class StringOperations:
    def __init__(self,name,age,profession):
        self.__name=name
        self.__age=age
        self.__profession=profession


    @property
    def name(self):
        """The getter is defined using the @property decorator.
            It retrieves the value of the attribute.
        """
        return self.__name

    @name.setter
    def name(self,value):
        """
        The setter is defined with the @<attribute>.setter decorator,
        which allows you to modify the value of the attribute.
         The setter can include validation checks to ensure proper values
         are assigned (for example, ensuring age is non-negative).
        """
        self.__name=value

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self,value):
        self.__age=value

    @property
    def profession(self):
        return self.__profession

    @profession.setter
    def profession(self,value):
        self.__profession=value

    def json(self):
        pass

    def save_details(self):
        pass

    def list_dicts(self,new_data):
        pass

    def convert_data_df(self):
        pass