
"""
Databases Package
"""

from .accessory import AccessoryDatabase        # Enum data, maak objecten mee
from .amulet import AmuletDatabase              #
from .armor import ArmorDatabase                #
from .belt import BeltDatabase                  #
from .boots import BootsDatabase                #
from .bracelet import BraceletDatabase          #
from .cloak import CloakDatabase                #
from .gloves import GlovesDatabase              #
from .helmet import HelmetDatabase              #
from .ring import RingDatabase                  #
from .shield import ShieldDatabase              #
from .weapon import WeaponDatabase              #

from .pouchitem import PouchItemDatabase        # Enum data, maak objecten mee
from .hero import HeroDatabase                  # Enum data, maak aan het begin alle objecten mee, gebruik sommige data
from .inn import InnDatabase                    # Enum data, gebruik de data
from .people import PeopleDatabase              # Enum data, gebruik de data
from .quest import QuestDatabase                # Enum data, maak objecten mee
from .school import SchoolDatabase              # Enum data, gebruik de data
from .shop import ShopDatabase                  # Enum data, gebruik de data
from .trainer import TrainerDatabase            # Enum data, gebruik de data
from .note import NoteDatabase                  # Enum data, gebruik de data
from .sign import SignDatabase                  # Enum data, gebruik de data
from .sparkly import SparklyDatabase            # Dict class, maak aan het begin 1 object van
from .treasurechest import TreasureChestDatabase    # Dict class, maak aan het begin 1 object van
