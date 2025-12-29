#!/bin/bash

# Target Monitor Identification (RTK - RealTek)
TARGET_MFG="RTK"
TARGET_MODEL="6432" 

# Check for ddcutil dependency
if ! command -v ddcutil &> /dev/null; then
    echo "Error: ddcutil is not installed."
    read -p "Do you want to install it now? (y/n): " install_choice
    if [ "$install_choice" == "y" ]; then
        if [ -x "$(command -v apt-get)" ]; then
            sudo apt-get update && sudo apt-get install -y ddcutil
        else
            echo "Package manager not found. Please install ddcutil manually."
            exit 1
        fi
    else
        echo "Please install ddcutil manually and run the script again."
        exit 1
    fi
fi 

# Function to detect the display number for the portable monitor
get_monitor_display() {
    DISP_NUM=$(sudo ddcutil detect | grep -B 10 "$TARGET_MFG" | grep "Display" | head -n 1 | awk '{print $2}')
    
    if [ -z "$DISP_NUM" ]; then
        DISP_NUM=$(sudo ddcutil detect | grep -B 10 "$TARGET_MODEL" | grep "Display" | head -n 1 | awk '{print $2}')
    fi
    
    echo "$DISP_NUM"
}

DISP_ID=$(get_monitor_display)

# Helper function to apply settings
# $1=Preset, $2=Contrast, $3=Red, $4=Green, $5=Blue, $6=Brightness, $7=SoftwareBrightness
apply_settings() {
    echo "Applying settings to Display $DISP_ID..."
    sudo ddcutil setvcp 14 $1 12 $2 16 $3 18 $4 1A $5 10 $6 --display $DISP_ID
    xrandr --output DP-1 --brightness $7 2>/dev/null
    echo "Done!"
}

# Clear screen and check monitor
clear
echo "=========================================="
echo "   Portable Monitor Settings Control"
if [ ! -z "$DISP_ID" ]; then
    echo "   [Detected RTK Monitor at Display $DISP_ID]"
else
    echo "   [WARNING: Portable Monitor Not Found via DDC]"
fi
echo "=========================================="

# Safety check
if [ -z "$DISP_ID" ]; then
    read -p "Monitor not auto-detected. Force try on Display 1? (y/n): " force
    if [ "$force" == "y" ]; then
        DISP_ID="1"
    else
        echo "Aborted."
        exit 1
    fi
fi

# Main Menu Selection
echo "Select Menu Layout:"
echo "1. Simple (Classic 3 Modes)"
echo "2. Advanced (All 8 Modes)"
read -p "Choose (1/2): " menu_type

echo ""

if [ "$menu_type" == "1" ]; then
    # --- SIMPLE MENU ---
    echo "--- SIMPLE MODES ---"
    echo "1. Standard Mode (Factory Default)"
    echo "2. Boost Mode (High Brightness & Clarity)"
    echo "3. Max Mode (Extreme Hardware + Software)"
    echo "=========================================="
    read -p "Select Mode (1-3): " choice

    case $choice in
        1) # Standard
            apply_settings 0x05 50 50 50 50 100 1
            ;;
        2) # Boost (Classic)
            apply_settings 0x08 75 80 80 80 100 1
            ;;
        3) # Max (Classic)
            apply_settings 0x08 100 80 80 80 100 1.2
            ;;
        *)
            echo "Invalid choice."
            ;;
    esac

elif [ "$menu_type" == "2" ]; then
    # --- ADVANCED MENU ---
    echo "--- GENERAL ---"
    echo "1. Standard Mode (Factory Default)"
    echo ""
    echo "--- CODING ---"
    echo "2. Code: Light Mode (Sharp & Bright)"
    echo "3. Code: Dark Mode (Eye Comfort)"
    echo ""
    echo "--- ENTERTAINMENT ---"
    echo "4. Movie Mode (Warm & Cinematic)"
    echo "5. Reading Mode (Web/E-book)"
    echo ""
    echo "--- GAMING ---"
    echo "6. Game: FPS/Competitive (Max Visibility)"
    echo "7. Game: RPG/Immersive (Vivid Color)"
    echo ""
    echo "--- EXTREME ---"
    echo "8. Max Mode (Overdrive 120%)"
    echo "=========================================="
    read -p "Select Mode (1-8): " choice

    case $choice in
        1) # Standard
            apply_settings 0x05 50 50 50 50 100 1
            ;;
        2) # Code Light
            apply_settings 0x05 75 50 50 50 100 1
            ;;
        3) # Code Dark
            apply_settings 0x05 60 50 50 50 40 1
            ;;
        4) # Movie
            apply_settings 0x04 80 50 50 50 90 1
            ;;
        5) # Reading
            apply_settings 0x04 45 50 50 50 35 0.9
            ;;
        6) # Game FPS
            apply_settings 0x08 85 80 80 80 100 1
            ;;
        7) # Game RPG
            apply_settings 0x02 80 50 50 50 95 1
            ;;
        8) # Max
            apply_settings 0x08 100 80 80 80 100 1.2
            ;;
        *)
            echo "Invalid choice."
            ;;
    esac
else
    echo "Invalid Menu Selection."
fi
