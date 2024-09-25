from unittest.mock import patch

import pytest

from glm_cli import GLMControl


@pytest.fixture
def glm_control():
    with patch("mido.get_input_names", return_value=["IAC Driver Bus 1"]):
        return GLMControl("IAC Driver Bus 1")


def test_find_virtual_midi_device(glm_control: GLMControl):
    with patch("mido.get_input_names", return_value=["IAC Driver Bus 1"]):
        assert (
            glm_control.find_virtual_midi_device("IAC Driver Bus 1")
            == "IAC Driver Bus 1"
        )


def test_activate_function(glm_control: GLMControl):
    with patch.object(glm_control, "send_midi_message") as mock_send_midi_message:
        glm_control.activate("volume_up")
        mock_send_midi_message.assert_called_once_with(21, 127)


def test_set_volume(glm_control: GLMControl):
    with patch.object(glm_control, "send_midi_message") as mock_send_midi_message:
        glm_control.set_volume(100)
        mock_send_midi_message.assert_called_once_with(20, 100)


def test_set_groupx(glm_control: GLMControl):
    with patch.object(glm_control, "send_midi_message") as mock_send_midi_message:
        glm_control.set_groupx(5)
        mock_send_midi_message.assert_called_once_with(30, 5)


def test_set_solo_dev(glm_control: GLMControl):
    with patch.object(glm_control, "send_midi_message") as mock_send_midi_message:
        glm_control.set_solo_dev(50)
        mock_send_midi_message.assert_called_once_with(43, 50)


def test_set_mute_dev(glm_control: GLMControl):
    with patch.object(glm_control, "send_midi_message") as mock_send_midi_message:
        glm_control.set_mute_dev(75)
        mock_send_midi_message.assert_called_once_with(44, 75)
