import re
import sys


def extract_hex():
    try:
        with open("/tmp/ddc_verbose.txt", "r", errors="ignore") as f:
            content = f.read()
    except FileNotFoundError:
        print("File /tmp/ddc_verbose.txt not found")
        sys.exit(1)

    # Split by "Display " to find "Display 1"
    # Note: The output format is "Display 1" at start of line
    blocks = re.split(r"\nDisplay ", "\n" + content)

    target_block = None
    for block in blocks:
        if block.startswith("1"):
            target_block = block
            break

    if not target_block:
        target_block = content  # Fallback if split fails or single display
        if "Display 1" not in target_block:
            sys.exit(1)

    hex_lines = []
    capture = False

    for line in target_block.splitlines():
        if "EDID hex dump:" in line:
            capture = True
            continue

        if capture:
            ls = line.strip()
            if ls.startswith("+"):
                # Extract hex parts
                # ddcutil detected output: +0000   00 ff ...  text
                parts = ls.split()
                # parts[0] is address
                # hex bytes follow
                current_hex = []
                for p in parts[1:]:
                    if re.match(r"^[0-9a-fA-F]{2}$", p):
                        current_hex.append(p)
                hex_lines.append(" ".join(current_hex))
            elif not ls:
                continue
            else:
                # End of hex block
                break

    print("\n".join(hex_lines))


if __name__ == "__main__":
    extract_hex()
