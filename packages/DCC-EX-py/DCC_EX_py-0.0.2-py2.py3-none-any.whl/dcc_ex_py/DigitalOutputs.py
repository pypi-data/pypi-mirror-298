from typing import Any

from .Helpers import ActiveState, DecodedCommand, IFlag


class DigitalOutput:
    """Represents a single digital output that can be monitored.
    """

    def __init__(self, id: int, pin: int, iflag: IFlag) -> None:
        """Instantiates a digital output when we first learn about it either because we created it or the command station told us about it.
        If we don't know this information at creation time, temporary values will be used and they will be filled in later.

        :param id: The internal id of this output.
        :param pin: The digital output pin on the arduino used by this output.
        :param iflag: The flags defining the behavior of this output.
        """
        #: The internal id of this output.
        self.id: int = id
        #: The pin on the arduino used by this output.
        self.pin: int = pin
        #: The iflag defining special behavior of this output.
        self.iflag: IFlag = iflag
        #: Whether this output is active or not.
        self.state: ActiveState = ActiveState.OFF

    # Happens when we first learn about this output because of a state change instead of a full definition
    def _pin_and_flag_later(self, pin: int, iflag: IFlag) -> None:
        """An internal initialization function triggered when we don't know all of the information about this pin on instantiation.

        :param pin: The digital output pin on the Arduino used by this output.
        :param iflag: The flags defining the behavior of this output.
        """
        self.pin = pin
        self.iflag = iflag

    def _set_state(self, state: ActiveState) -> None:
        """An internal notification when we recieve notice the pin state has changed from the command station.

        :param state: The updated state of this digital pin.
        """
        self.state = state


class DigitalOutputs:
    """Wraps control of DCC-EX digital output pins for easy control and monitoring.
    """

    def __init__(self, controller: Any) -> None:
        """Instantiated by the DCCEX Instance.

        :param controller: The DCCEX object that this instance controls.
        """
        from .DCCEX import DCCEX
        self.controller: DCCEX = controller

        self.outputs: dict[int, DigitalOutput] = {}

        self.controller.add_command_listener(self._command_received)

    def create_output_pin(self, id: int, pin: int, flags: IFlag) -> DigitalOutput:
        """Defines an output pin on the DCC-EX board if it hasn't already been with the given inputs.

        :param id: The id assigned tot he pin. These ids are shared with sensors.
        :param pin: The digital output pin on the Arduino this output uses.
        :param flags: A set of flags to define the output pin behaviors.

        :returns: A local representation of the digital output created.
        """
        self.controller.send_command(f"<Z {id} {pin} {str(flags)}>")

        self.outputs[id] = DigitalOutput(id, pin, flags)
        return self.outputs[id]

    def delete_output_pin(self, id: int) -> None:
        """Deletes the output pin at the given id. (id is based on the DCC-EX board not the arduino pin.) Also deletes the local isntance of the pin.

        :param id: The id of the digital output to delete.
        """
        self.controller.send_command(f"<Z {id}>")
        self.outputs.pop(id, None)

    def set_output_pin(self, id: int, state: ActiveState) -> None:
        """Turns the output pin on or off.

        :param id: The id of the output pin to change.
        :param state: Whether to turn the pin on or off."""
        self.controller.send_command(f"<Z {id} {state}>")
        # this causes DCC-EX to broadcast the state change, we update our local cache using that instead.

    def refresh_output_pins(self) -> None:
        """Asks the command station to tell us about each of it's digital output pins and their state.
        """
        self.controller.send_command("<Z>")

    def _command_received(self, command: DecodedCommand) -> None:
        """Internal listener to catch changes on the command station both caused by this program and other connections.

        :param command: The command we received after parsing it into a helper class.
        """
        if command.command == 'Y':
            if command.args == 4:  # Full definition
                id: int = int(command.args[0])
                if id not in self.outputs:
                    self.outputs[id] = DigitalOutput(id, int(command.args[1]), IFlag(int(command.args[2])))
                else:
                    self.outputs[id]._pin_and_flag_later(int(command.args[1]), IFlag(int(command.args[2])))

                self.outputs[id]._set_state(ActiveState(command.args[3]))

            elif command.args == 2:  # State update successful
                id: int = int(command.args[0])
                if id not in self.outputs:
                    self.outputs[id] = DigitalOutput(id, 0, IFlag.DEFAULT_ACTIVE)
                self.outputs[id]._set_state(ActiveState(command.args[1]))
