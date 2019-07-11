# Control a UM3561 ic
# See https://www.instructables.com/id/Siren-Generation-using-IC-UM3561/ for pinout
#
# 1. sel1
# 2. gnd
# 3. out -> 1k ohm -> transistor that drives speaker gnd line
# 4. not connected (testing)
# 5. active (3-5vin)
# 6. sel2
# 7. osc1
# 8. osc2 -> bridge osc1 -> osc2 with a 220 ohm resistor
#
# S1   S2   Sound
# --------------------
# NC   NC   Police (default)
# 5v   NC   Fire brigade
# Gnd  NC   Ambulance
# Any  5v   Machine gun


from .device import Device


class AlarmProfile(object):

    POLICE = "police"
    FIRE = "fire"
    AMBULANCE = "ambulance"
    MACHINE_GUN = "machine gun"


class SirenIC(Device):

    id = 0

    def __init__(self, pin_active, pin_sel1, pin_sel2, name=None, interval=0.1, *args, **kwargs):
        if not name:
            name = "srn{}".format(SirenIC.id)
            SirenIC.id += 1
        Device.__init__(self, name=name, interval=interval, *args, **kwargs)

        import digitalio

        self.pin_active = digitalio.DigitalInOut(pin_active)
        self.pin_active.direction = digitalio.Direction.OUTPUT

        self.pin_sel1 = digitalio.DigitalInOut(pin_sel1)
        self.pin_sel1.direction = digitalio.Direction.OUTPUT

        self.pin_sel2 = digitalio.DigitalInOut(pin_sel2)
        self.pin_sel2.direction = digitalio.Direction.OUTPUT

        self.data["active"] = False
        self.data["profile"] = AlarmProfile.POLICE

    def write(self):

        if self.data["profile"] == AlarmProfile.POLICE:
            self.pin_sel1.value = False
            self.pin_sel2.value = False
        elif self.data["profile"] == AlarmProfile.FIRE:
            self.pin_sel1.value = True
            self.pin_sel2.value = False
        elif self.data["profile"] == AlarmProfile.AMBULANCE:
            self.pin_sel1.value = False
            self.pin_sel2.value = True
        elif self.data["profile"] == AlarmProfile.MACHINE_GUN:
            self.pin_sel1.value = True
            self.pin_sel2.value = True
        else:
            raise ValueError("Unknown alarm profile {}".format(self.data["profile"]))

        self.pin_active.value = self.data["active"]

        # print("Siren is {}".format(self.pin_active.value))
