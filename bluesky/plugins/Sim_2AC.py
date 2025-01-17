"""
Plugin for simulating 2-aircraft conflict episodes, to train a conflict-resolution DQN
Author : Shiraz Khan
"""

from numpy import random, cos, sin, deg2rad
from bluesky import stack, traf
from bluesky.tools.geo import qdrdist

# Radius (in "Latitudes")
RADIUS = 0.4

# Radius (in nautical miles)
_, RADIUS_NM = qdrdist(-RADIUS, 0, 0, 0)


def init_plugin():
    reset()

    # Configuration parameters
    config = {
        'plugin_name':     'Sim_2AC',
        'plugin_type':     'sim',
        'preupdate':       preupdate,
        'reset':           reset
        }
    stackfunctions = {}

    return config, stackfunctions


def reset():
    # Sets area of interest, flights exiting this area are deleted
    stack.stack(f"CIRCLE SimCirc 0 0 {RADIUS_NM}")
    # stack.stack("AREA SimCirc")  ~~ This is now being done explicitly in plugins.CR_2AC.preupdate()
    reset_aircrafts()


def preupdate():
    pass


def create_self_ac():
    """
    Create aircraft going from South to North
    """
    pos_lat = -RADIUS
    pos_lon = 0
    hdg = 0
    stack.stack(f"CRE SELF B744 {pos_lat} {pos_lon} {hdg} FL200 400")


def create_enemy_ac():
    """
    Create aircraft coming inwards from a random point on circumference
    """
    hdg = random.uniform(0, 360.0)
    hdg_r = deg2rad(hdg)
    pos_lon = -1 * RADIUS * sin(hdg_r)
    pos_lat = -1 * RADIUS * cos(hdg_r)
    stack.stack(f"CRE ENEMY B744 {pos_lat} {pos_lon} {hdg} FL200 400")


def reset_aircrafts():
    """
    Creates both aircrafts.
    Note : CR_2AC relies on the order of creation
    """
    delete_aircrafts()
    create_self_ac()
    create_enemy_ac()


def delete_aircrafts():
    stack.stack(f"DEL SELF")
    stack.stack(f"DEL ENEMY")
