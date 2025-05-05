from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models here after they are created
from .victim import VictimSurvivor
from .missing_person import MissingPersonReport
from .relief_camp import ReliefCamp
from .inventory import Inventory
from .donor import Donor
from .donation import Donation
from .supply import Supply
from .volunteer import Volunteer
from .volunteer_assignment import VolunteerAssignment
# For example:
# from .user_model import User
# from .disaster_model import Disaster 