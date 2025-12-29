import sys
import subprocess
import re
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                             QWidget, QSlider, QHBoxLayout, QMessageBox, 
                             QPushButton, QTabWidget, QGridLayout)
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lanlipu Portable Monitor Settings")
        self.setGeometry(100, 100, 500, 650)
        
        # Data: Presets from shell script
        # Format: [Preset(VCP 14), Contrast(12), Red(16), Green(18), Blue(1A), Brightness(10), Gamma(SW)]
        self.PRESETS = {
            # Simple / General
            "Standard Mode (Default)": [0x05, 50, 50, 50, 50, 100, 1.0],
            "Boost Mode":              [0x08, 75, 80, 80, 80, 100, 1.0],
            "Max Mode":                [0x08, 100, 80, 80, 80, 100, 1.2],
            
            # Advanced - Coding
            "Code: Light Mode":        [0x05, 75, 50, 50, 50, 100, 1.0],
            "Code: Dark Mode":         [0x05, 60, 50, 50, 50, 40, 1.0],
            
            # Advanced - Entertainment
            "Movie Mode":              [0x04, 80, 50, 50, 50, 90, 1.0],
            "Reading Mode":            [0x04, 45, 50, 50, 50, 35, 0.9],
            
            # Advanced - Gaming
            "Game: FPS/Competitive":   [0x08, 85, 80, 80, 80, 100, 1.0],
            "Game: RPG/Immersive":     [0x02, 80, 50, 50, 50, 95, 1.0],
        }

        # 1. Detect Monitor ID (DDC)
        self.display_id = self.get_monitor_id()
        # 2. Detect Display Output (xrandr)
        self.xrandr_output = self.get_xrandr_output()
        
        # Main Layout
        main_layout = QVBoxLayout()
        
        # Header
        header_text = f"DDC Monitor ID: {self.display_id} | Output: {self.xrandr_output}"
        self.info_label = QLabel(header_text)
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 5px;")
        main_layout.addWidget(self.info_label)

        # --- Preset Tabs ---
        tabs = QTabWidget()
        tabs.addTab(self.create_simple_tab(), "Simple Menu")
        tabs.addTab(self.create_advanced_tab(), "Advanced Menu")
        main_layout.addWidget(tabs)
        
        main_layout.addWidget(QLabel("--- Fine Tuning Controls ---"))

        # Sliders storage to update them programmatically
        self.sliders = {}

        # --- Hardware Controls (DDC) ---
        # Brightness (VCP 10)
        main_layout.addLayout(self.create_slider("HW Brightness", 0x10, 0, 100, 100, "brightness"))
        
        # Contrast (VCP 12)
        main_layout.addLayout(self.create_slider("Contrast", 0x12, 0, 100, 50, "contrast"))
        
        # Red (VCP 16)
        main_layout.addLayout(self.create_slider("Red Gain", 0x16, 0, 100, 50, "red"))
        
        # Green (VCP 18)
        main_layout.addLayout(self.create_slider("Green Gain", 0x18, 0, 100, 50, "green"))
        
        # Blue (VCP 1A)
        main_layout.addLayout(self.create_slider("Blue Gain", 0x1A, 0, 100, 50, "blue"))

        # --- Software Controls (xrandr) ---
        # Gamma / SW Brightness
        main_layout.addLayout(self.create_gamma_slider("SW Brightness (Gamma)", 10, 200, 100, "gamma"))

        # Container
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def create_simple_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(self.create_btn("Standard Mode (Default)"))
        layout.addWidget(self.create_btn("Boost Mode"))
        layout.addWidget(self.create_btn("Max Mode"))
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab

    def create_advanced_tab(self):
        tab = QWidget()
        layout = QGridLayout()
        
        # General
        layout.addWidget(QLabel("General:"), 0, 0)
        layout.addWidget(self.create_btn("Standard Mode (Default)"), 0, 1)
        
        # Coding
        layout.addWidget(QLabel("Coding:"), 1, 0)
        layout.addWidget(self.create_btn("Code: Light Mode"), 1, 1)
        layout.addWidget(self.create_btn("Code: Dark Mode"), 2, 1)
        
        # Entertainment
        layout.addWidget(QLabel("Entertainment:"), 3, 0)
        layout.addWidget(self.create_btn("Movie Mode"), 3, 1)
        layout.addWidget(self.create_btn("Reading Mode"), 4, 1)
        
        # Gaming
        layout.addWidget(QLabel("Gaming:"), 5, 0)
        layout.addWidget(self.create_btn("Game: FPS/Competitive"), 5, 1)
        layout.addWidget(self.create_btn("Game: RPG/Immersive"), 6, 1)
        
        # Extreme
        layout.addWidget(QLabel("Extreme:"), 7, 0)
        layout.addWidget(self.create_btn("Max Mode"), 7, 1)

        tab.setLayout(layout)
        return tab

    def create_btn(self, name):
        btn = QPushButton(name)
        btn.clicked.connect(lambda: self.apply_preset(name))
        return btn

    def apply_preset(self, preset_name):
        print(f"Applying Preset: {preset_name}")
        values = self.PRESETS.get(preset_name)
        if not values:
            return

        # Unpack values
        # [Preset(0), Contrast(1), Red(2), Green(3), Blue(4), Brightness(5), Gamma(6)]
        preset_vcp, contrast, red, green, blue, brightness, gamma = values
        
        # 1. Update Sliders (This determines visual state + triggers single updates)
        # Note: Ideally we should block signals if we want to batch send, 
        # but to keep simple consistent logic with valid 'sliderReleased', we can just set them.
        # However, setPreset uses 'setvcp' directly usually. 
        # But 'sliderReleased' only fires on user interaction. setValue() does NOT trigger sliderReleased.
        # So we must call set_vcp manually or relying on valueChanged (which is spammy).
        # We used sliderReleased in create_slider. So setValue() simply updates UI.
        
        self.sliders["brightness"].setValue(brightness)
        self.sliders["contrast"].setValue(contrast)
        self.sliders["red"].setValue(red)
        self.sliders["green"].setValue(green)
        self.sliders["blue"].setValue(blue)
        self.sliders["gamma"].setValue(int(gamma * 100))
        
        # 2. Send Actual Commands (Batch / Sequential)
        # We also need to send the 'Preset VCP 14' command which has no slider
        self.set_vcp(0x14, preset_vcp) 
        self.set_vcp(0x12, contrast)
        self.set_vcp(0x16, red)
        self.set_vcp(0x18, green)
        self.set_vcp(0x1A, blue)
        self.set_vcp(0x10, brightness)
        self.set_gamma(int(gamma * 100))
        
        print("Preset Applied!")

    def get_monitor_id(self):
        try:
            cmd = "sudo ddcutil detect"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            output = result.stdout
            if "RTK" in output or "6432" in output:
                match = re.search(r"Display\s+(\d+)", output)
                if match: return match.group(1)
            return "1" 
        except: return "1"

    def get_xrandr_output(self):
        try:
            cmd = "xrandr | grep ' connected'"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            outputs = [line.split()[0] for line in result.stdout.strip().split('\n') if line]
            if "DP-1" in outputs: return "DP-1"
            if len(outputs) > 1: return outputs[1]
            if len(outputs) == 1: return outputs[0]
            return "DP-1"
        except: return "DP-1"

    def create_slider(self, label_text, vcp_code, min_val, max_val, default_val, key):
        layout = QVBoxLayout()
        header_layout = QHBoxLayout()
        label = QLabel(label_text)
        value_label = QLabel(str(default_val))
        header_layout.addWidget(label)
        header_layout.addStretch()
        header_layout.addWidget(value_label)
        layout.addLayout(header_layout)

        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(default_val)
        
        slider.valueChanged.connect(lambda val: value_label.setText(str(val)))
        slider.sliderReleased.connect(lambda: self.set_vcp(vcp_code, slider.value()))
        
        layout.addWidget(slider)
        
        # Store ref
        self.sliders[key] = slider
        return layout

    def create_gamma_slider(self, label_text, min_val, max_val, default_val, key):
        layout = QVBoxLayout()
        header_layout = QHBoxLayout()
        label = QLabel(label_text)
        value_label = QLabel(f"{default_val/100:.2f}") 
        header_layout.addWidget(label)
        header_layout.addStretch()
        header_layout.addWidget(value_label)
        layout.addLayout(header_layout)

        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(default_val)
        
        slider.valueChanged.connect(lambda val: value_label.setText(f"{val/100:.2f}"))
        slider.sliderReleased.connect(lambda: self.set_gamma(slider.value()))
        
        layout.addWidget(slider)
        self.sliders[key] = slider
        return layout

    def set_vcp(self, vcp_code, value):
        print(f"DDC: Setting VCP {hex(vcp_code)} to {value}...")
        try:
            subprocess.run(f"sudo ddcutil setvcp {hex(vcp_code)} {value} --display {self.display_id}", shell=True)
        except Exception as e: print(e)

    def set_gamma(self, int_value):
        float_val = int_value / 100.0
        print(f"xrandr: Setting brightness to {float_val}...")
        try:
            subprocess.run(f"xrandr --output {self.xrandr_output} --brightness {float_val}", shell=True)
        except Exception as e: print(e)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
