"""
**Kwargs(Keyword Arguments)

This Parameter will pass all the arguments in to a dictionary. So that function can accept a varying amount of keyword arguments.....
"""

# Example
def personal_details(**kwargs):
    print("Hi This is {name}, I'm moving to {country} for my masters in {specialization}.".format(name=kwargs['name'],country=kwargs['country'],specialization=kwargs['specialization']))

# personal_details(name="P Mahesh Kumar",country="Germany",specialization="Datascience")