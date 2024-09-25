# glm cli

Genelec GLM cli (works over virtual midi, expects app to be open)

## Requirements

This assumes you have [direnv](https://direnv.net/) and [uv](https://github.com/astral-sh/uv) installed

Simply run `direnv allow` to setup the environment, you can read the contents of [.envrc](.envrc) to see what it does behind the scenes.

## Usage

1. Open the Genelec GLM app

2. Open Audio Midi Setup -> Window show Midi Studio -> Make sure IAC Driver is online, you can look at image below to verify

![iac-driver](./docs/iac-driver.png)

3. Open Settings -> Midi Settings on GLM app, make sure Enable GLM Midi interface is checkend, and the virtual midi device from the previous step is selected.

![glm-midi-settings](./docs/glm-midi-settings.png)

4. Run `glm-cli --help` to see the available commands
