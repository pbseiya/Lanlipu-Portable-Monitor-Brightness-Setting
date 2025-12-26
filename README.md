# lanlipu_portable_monitor_brightness_setting

A Bash script for adjusting brightness, contrast, and color settings of the RTK (RealTek) 6432 portable monitor using `ddcutil` and `xrandr` to control both hardware and software.

## Prerequisites

- Linux OS supporting `ddcutil` and `xrandr`
- `ddcutil` installed (install with `sudo apt install ddcutil` on Ubuntu/Debian)
- Sudo privileges to run `ddcutil` commands
- RTK 6432 portable monitor connected and detectable

## Installation

1. Clone this repository to your machine:
   ```
   git clone https://github.com/pbseiya/lanlipu_portable_monitor_brightness_setting.git
   cd lanlipu_portable_monitor_brightness_setting
   ```

2. Make the script executable:
   ```
   chmod +x portable_monitor_setting.sh
   ```

## Usage

Run the script with:
```
./portable_monitor_setting.sh
```

The script will:
- Automatically detect the RTK 6432 portable monitor
- Display a menu to select menu type (Simple or Advanced)
- Apply appropriate settings based on the selected mode

### Main Menus

- **Simple Menu**: 3 basic modes for general users
- **Advanced Menu**: 8 modes for specific tasks like coding, entertainment, gaming

### Modes

#### Simple Menu
1. **Standard Mode**: Factory default (Preset 0x05, Contrast 50, RGB 50/50/50, Brightness 100, Software Brightness 1.0)
2. **Boost Mode**: High brightness and clarity (Preset 0x08, Contrast 75, RGB 80/80/80, Brightness 100, Software Brightness 1.0)
3. **Max Mode**: Extreme hardware + software (Preset 0x08, Contrast 100, RGB 80/80/80, Brightness 100, Software Brightness 1.2)

#### Advanced Menu
1. **Standard Mode**: Factory default
2. **Code: Light Mode**: Suitable for coding in bright light (Preset 0x05, Contrast 75, RGB 50/50/50, Brightness 100, Software Brightness 1.0)
3. **Code: Dark Mode**: Suitable for coding in dark environments to reduce eye strain (Preset 0x05, Contrast 60, RGB 50/50/50, Brightness 40, Software Brightness 1.0)
4. **Movie Mode**: Warm and cinematic for watching movies (Preset 0x04, Contrast 80, RGB 50/50/50, Brightness 90, Software Brightness 1.0)
5. **Reading Mode**: For web/e-book reading (Preset 0x04, Contrast 45, RGB 50/50/50, Brightness 35, Software Brightness 0.9)
6. **Game: FPS/Competitive**: Maximum visibility for FPS games (Preset 0x08, Contrast 85, RGB 80/80/80, Brightness 100, Software Brightness 1.0)
7. **Game: RPG/Immersive**: Vivid colors for RPG games (Preset 0x02, Contrast 80, RGB 50/50/50, Brightness 95, Software Brightness 1.0)
8. **Max Mode**: Extreme mode (Preset 0x08, Contrast 100, RGB 80/80/80, Brightness 100, Software Brightness 1.2)

## Utility Scripts

### `extract_edid.py`
This Python script is used for debugging and extracting raw EDID data from `ddcutil` verbose output.
- **Why it's needed**: Some portable monitors (like this RTK model) do not expose EDID correctly via standard i2c tools.
- **What it does**: It parses the output of `ddcutil detect --verbose`, extracts the hex dump of the monitor's EDID, and can be piped to `edid-decode` to view deep hardware specs (like Nits/Luminance).

## Troubleshooting

- **Monitor not found**: Check that the monitor is properly connected and `ddcutil detect` can detect it. If not found, the script will ask to force try on Display 1.
- **Insufficient permissions**: Ensure you have sudo privileges and `ddcutil` is installed correctly.
- **Not working**: Check that xrandr output is DP-1 (can be modified in the script if necessary).

## License

This project is licensed under the MIT License.