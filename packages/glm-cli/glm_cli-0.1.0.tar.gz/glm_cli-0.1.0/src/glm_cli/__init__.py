from typing import Optional

import click
import mido  # type: ignore


class GLMControl:
    # Define the MIDI control change (CC) numbers for various functions
    # NOTE: These are default values from GLM-5 on Mac , going to Settings -> MIDI Settings
    CC_MAP = {
        "volume_up": 21,
        "volume_down": 22,
        "mute": 23,
        "dim": 24,
        "preset_level1": 25,
        "preset_level2": 26,
        "bm_bypass": 27,
        "system_power": 28,
        "group1": 31,
        "group2": 32,
        "group3": 33,
        "group4": 34,
        "group5": 35,
        "group6": 36,
        "group7": 37,
        "group8": 38,
        "group9": 39,
        "group10": 40,
        "group_plus": 41,
        "group_minus": 42,
    }

    VOLUME_CC = 20  # Special case for volume
    GROUPX_CC = 30  # Special case for groupx
    SOLO_DEV_CC = 43  # Special case for solo dev
    MUTE_DEV_CC = 44  # Special case for mute dev

    def __init__(self, device_name: str):
        self.device_name = device_name
        self.port_name = self.find_virtual_midi_device(device_name)

    def find_virtual_midi_device(self, name: str) -> Optional[str]:
        """Find the virtual MIDI device by name."""
        for port in mido.get_input_names():  # type: ignore
            if name in port:
                return port  # type: ignore
        return None

    def send_midi_message(self, control: int, value: int):
        """Send a MIDI control change message."""
        if not self.port_name:
            print(f"Virtual MIDI device '{self.device_name}' not found.")
            return

        with mido.open_output(self.port_name) as outport:  # type: ignore
            msg = mido.Message("control_change", control=control, value=value)
            outport.send(msg)  # type: ignore
            print(f"Sent control change: control={control}, value={value}")

    def activate(self, function_name: str):
        """Activate a function by name (momentary)."""
        if function_name in self.CC_MAP:
            self.send_midi_message(self.CC_MAP[function_name], 127)
        else:
            print(f"Function '{function_name}' not found.")

    def set_volume(self, value: int):
        """Set the volume to a specific value (0-127)."""
        if 0 <= value <= 127:
            self.send_midi_message(self.VOLUME_CC, value)
        else:
            print("Volume value must be between 0 and 127.")

    def set_groupx(self, value: int):
        """Set group x to a specific value (1-10)."""
        if 1 <= value <= 10:
            self.send_midi_message(self.GROUPX_CC, value)
        else:
            print("Group x value must be between 1 and 10.")

    def set_solo_dev(self, value: int):
        """Set solo dev to a specific value (0-127)."""
        if 0 <= value <= 127:
            self.send_midi_message(self.SOLO_DEV_CC, value)
        else:
            print("Solo dev value must be between 0 and 127.")

    def set_mute_dev(self, value: int):
        """Set mute dev to a specific value (0-127)."""
        if 0 <= value <= 127:
            self.send_midi_message(self.MUTE_DEV_CC, value)
        else:
            print("Mute dev value must be between 0 and 127.")


@click.group()
@click.option(
    "--device",
    default="IAC Driver Bus 1",
    required=True,
    help="Name of the virtual MIDI device",
)
@click.pass_context
def cli(ctx: click.Context, device: str):
    """CLI for controlling GLM via MIDI."""
    ctx.ensure_object(dict)
    ctx.obj["controller"] = GLMControl(device)


@cli.command()
@click.pass_context
def list_functions(ctx: click.Context):
    """List all available functions."""
    controller = ctx.obj["controller"]
    for function in controller.CC_MAP.keys():
        click.echo(function)


@cli.command()
@click.argument("function_name")
@click.pass_context
def activate(ctx: click.Context, function_name: str):
    """Activate a function by name."""
    controller = ctx.obj["controller"]
    controller.activate(function_name)


@cli.command()
@click.argument("value", type=int)
@click.pass_context
def set_volume(ctx: click.Context, value: int):
    """Set the volume to a specific value (0-127)."""
    controller = ctx.obj["controller"]
    controller.set_volume(value)


@cli.command()
@click.argument("value", type=int)
@click.pass_context
def set_groupx(ctx: click.Context, value: int):
    """Set group x to a specific value (1-10)."""
    controller = ctx.obj["controller"]
    controller.set_groupx(value)


@cli.command()
@click.argument("value", type=int)
@click.pass_context
def set_solo_dev(ctx: click.Context, value: int):
    """Set solo dev to a specific value (0-127)."""
    controller = ctx.obj["controller"]
    controller.set_solo_dev(value)


@cli.command()
@click.argument("value", type=int)
@click.pass_context
def set_mute_dev(ctx: click.Context, value: int):
    """Set mute dev to a specific value (0-127)."""
    controller = ctx.obj["controller"]
    controller.set_mute_dev(value)


if __name__ == "__main__":
    cli()
