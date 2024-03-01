"""

Test Manager

This is the flow controller of the unit tests.

Only the tests imported in this file will be executed, in the order of importation.

"""

from base import TestApp # basic tests of the aplication function and configuration
from database import TestDatabase # preparation and testing of the database
from homepage import TestHomepage # testing the basic homepage 
from registration import TestRegisterUser # testing all the user registration functions and validations