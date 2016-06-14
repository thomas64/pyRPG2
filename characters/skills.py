
"""
class: Skill
class: etc
"""


PATH = 'resources/sprites/icons/skills/'

# todo, description aanpassen van skills. wanneer skills meer of anders kunnen, zoals pick locks voor thief.
# todo, docstrings


class Skill(object):
    """
    Skill baseclass voor skills.
    """
    TRAININGSCOSTS = (200, 80, 120, 160, 200, 240, 280, 320, 360, 400, "Max")

    def __init__(self, name, raw, upgrade, quantity):
        self.NAM = name
        self.RAW = raw
        self.ICON = PATH+name.lower()+'.png'
        self.MAX = 10                   # maximum mogelijk, is voor alle skills 10
        self.UPG = upgrade              # upgrade formule constante
        self.qty = quantity             # standaard hoeveelheid op te waarderen stat (tot bijv 30)
        self.ext = 0                    # extra: wat geeft equipment item voor pos/neg extra

    @property
    def tot(self):
        """
        Ext en qty vormen samen totaal.
        self.tot = self.qty + self.ext
        total: quantity + extra
        """
        total = self.qty + self.ext
        if total < 0 or self.qty <= 0:
            total = 0
        return total

    def positive_quantity(self):
        """
        ...
        """
        if self.qty >= 1:
            return True
        return False


class Alchemist(Skill):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Alchemist", "alc", 1200, quantity)
        self.DESC = "Allows the character to manufacture various potions out of Herbs, Spices and Gemstones. " \
                    "A higher Alchemist rank means a higher chance to successfully create a potion."


class Diplomat(Skill):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Diplomat", "dip", 400, quantity)
        self.DESC = "The higher the Diplomat rank, the lower are the conditions of new heroes who wants to join " \
                    "the party. For every 1 Diplomat rank gained, 1% lower conditions. Cumulative for all characters."


class Healer(Skill):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Healer", "hlr", 800, quantity)
        self.DESC = "Allows the character to heal another character in combat. " \
                    "Character may use herbs to double the amount of damage restored. " \
                    "A higher Healer rank means more restoration of damage."


class Loremaster(Skill):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Loremaster", "lor", 600, quantity)
        self.DESC = "Lowers the XP needed for training Stats(?), Skills and Spells. " \
                    "For every 1 Loremaster rank gained, 1% less XP is needed."


class Mechanic(Skill):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Mechanic", "mec", 400, quantity)
        self.DESC = "Allows the character to upgrade inventory with metals. The process also costs gold. " \
                    "A higher Mechanic rank means a higher chance to successfully upgrade an item. " \
                    "The item is destroyed when upgrade is unsuccessful."


class Merchant(Skill):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Merchant", "mer", 600, quantity)
        self.DESC = "The higher the Merchant rank, the lower the prices when buying (and the higher the " \
                    "prices when selling) in shops. For every 1 Merchant rank gained, 1% extra gold in your " \
                    "favor. Cumulative for all characters."


class Ranger(Skill):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Ranger", "ran", 800, quantity)
        self.DESC = "Helps to increase the amount of Herbs, Spices, Gemstones and Metals " \
                    "when searching for materials. More characters " \
                    "with this skill will help to find even more materials."


class Stealth(Skill):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Stealth", "stl", 400, quantity)
        self.DESC = "Makes it easier to flee from combat. For every 1 Stealth rank gained, 1% more chance " \
                    "to flee. Cumulative for all characters. Also when in combat, for every 2 Stealth ranks " \
                    "gained, the enemy thinks the character is 1 position further away."


class Thief(Skill):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Thief", "thf", 800, quantity)
        self.DESC = "Improves character's chance to hit and increases damage " \
                    "inflicted FROM BEHIND in combat. For every 1 Thief rank gained, " \
                    "2% more chance to hit and 3% more damage."


class Troubadour(Skill):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Troubadour", "trb", 800, quantity)
        self.DESC = "Allows character to play and sing inspirationally, improving your party's chance " \
                    "to hit in combat and reducing the enemy's chance to hit. For every 1 Troubadour " \
                    "rank gained, 2% more chance to hit."


class Warrior(Skill):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Warrior", "war", 800, quantity)
        self.DESC = "Improves base hit of character's weapon. Especially weapons with a low base hit. " \
                    "It also allows the possibility of scoring critical hits in combat. For every 1 " \
                    "Warrior rank gained, 2% extra chance for a critical hit. And overall, it improves " \
                    "combat damage and defenses."

    def bonus(self, wpn):
        """
        Berekent de warrior bonus.
        :param wpn: EquipmentItem object van weapon
        :return: de formule of anders 0
        """
        if self.positive_quantity() and wpn.is_not_empty():
            return round((47 - ((wpn.HIT / 10) * 5)) * (self.tot / 10))
        return 0


class Wizard(Skill):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Wizard", "wiz", 1200, quantity)
        self.DESC = "At the moment, Wizard does nothing."


class Hafted(Skill):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Hafted", "haf", 320, quantity)
        self.DESC = "Improves character's chance to hit and increseas damage inflicted with Hafted weapons in " \
                    "combat. For every 1 Hafted rank gained, 2% more chance to hit and 1% more damage."


class Missile(Skill):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Missile", "mis", 480, quantity)
        self.DESC = "Improves character's chance to hit and increseas damage inflicted with Missile weapons in " \
                    "combat. For every 1 Missile rank gained, 2% more chance to hit and 1% more damage."


class Pole(Skill):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Pole", "pol", 320, quantity)
        self.DESC = "Improves character's chance to hit and increseas damage inflicted with Pole weapons in combat. " \
                    "For every 1 Pole rank gained, 2% more chance to hit and 1% more damage."


class Shield(Skill):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Shield", "shd", 400, quantity)
        self.DESC = "Improves character's defenses when wearing a shield in combat. A shield doesn't defend " \
                    "character's back."


class Sword(Skill):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Sword", "swd", 480, quantity)
        self.DESC = "Improves character's chance to hit and increseas damage inflicted with all types of swords " \
                    "and daggers in combat. For every 1 Sword rank gained, 2% more chance to hit and 1% more damage."


class Thrown(Skill):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Thrown", "thr", 320, quantity)
        self.DESC = "Improves character's chance to hit and increseas damage inflicted with Thrown weapons in " \
                    "combat. For every 1 Thrown rank gained, 2% more chance to hit and 1% more damage."
