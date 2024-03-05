import subprocess

# ANSI color codes
class Color:
    HEADER = '\033[95m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# Cyberbuddy Logo ASCII art
logo = r"""
////////////////////////////////////////////////////////////////////////////////////////////
//                                                                                        //
//                                                                                        //
//   ▄████▄  ▓██   ██▓ ▄▄▄▄   ▓█████  ██▀███   ▄▄▄▄    █    ██ ▓█████▄ ▓█████▄ ▓██   ██▓  //
//  ▒██▀ ▀█   ▒██  ██▒▓█████▄ ▓█   ▀ ▓██ ▒ ██▒▓█████▄  ██  ▓██▒▒██▀ ██▌▒██▀ ██▌ ▒██  ██▒  //
//  ▒▓█    ▄   ▒██ ██░▒██▒ ▄██▒███   ▓██ ░▄█ ▒▒██▒ ▄██▓██  ▒██░░██   █▌░██   █▌  ▒██ ██░  //
//  ▒▓▓▄ ▄██▒  ░ ▐██▓░▒██░█▀  ▒▓█  ▄ ▒██▀▀█▄  ▒██░█▀  ▓▓█  ░██░░▓█▄   ▌░▓█▄   ▌  ░ ▐██▓░  //
//  ▒ ▓███▀ ░  ░ ██▒▓░░▓█  ▀█▓░▒████▒░██▓ ▒██▒░▓█  ▀█▓▒▒█████▓ ░▒████▓ ░▒████▓   ░ ██▒▓░  //
//  ░ ░▒ ▒  ░   ██▒▒▒ ░▒▓███▀▒░░ ▒░ ░░ ▒▓ ░▒▓░░▒▓███▀▒░▒▓▒ ▒ ▒  ▒▒▓  ▒  ▒▒▓  ▒    ██▒▒▒   //
//    ░  ▒    ▓██ ░▒░ ▒░▒   ░  ░ ░  ░  ░▒ ░ ▒░▒░▒   ░ ░░▒░ ░ ░  ░ ▒  ▒  ░ ▒  ▒  ▓██ ░▒░   //
//  ░         ▒ ▒ ░░   ░    ░    ░     ░░   ░  ░    ░  ░░░ ░ ░  ░ ░  ░  ░ ░  ░  ▒ ▒ ░░    //
//  ░ ░       ░ ░      ░         ░  ░   ░      ░         ░        ░       ░     ░ ░       //
//  ░         ░ ░           ░                       ░           ░       ░       ░ ░       //
//                                                                                        //
//                                                                                        //
////////////////////////////////////////////////////////////////////////////////////////////
"""

# Function to start Frida server
def start_frida_server():
    # Start Frida server using adb shell command
    adb_command = "adb shell \"/data/local/tmp/frida-server &\""
    try:
        subprocess.run(adb_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"{Color.RED}Error starting Frida server: {e}{Color.END}")

# Function to get package names using frida-ps
def get_package_names():
    frida_ps_command = ["frida-ps", "-Uai"]
    try:
        output = subprocess.check_output(frida_ps_command).decode()
        # Split the output by lines and extract package identifiers
        lines = output.strip().split('\n')
        package_data = [(i, line.split()[2]) for i, line in enumerate(lines[2:], start=1)]  # Skip the header lines
        return package_data
    except subprocess.CalledProcessError as e:
        print(f"{Color.RED}Error retrieving package identifiers: {e}{Color.END}")
        return []

# Function to run Frida command with specified package identifier
def run_frida(package_identifier):
    # Frida command
    frida_command = [
        "frida",
        "-U",
        "-f",
        package_identifier,
        "-l",
        "antiroot.js",
        "-l",
        "emulator.js",
        "-l",
        "sslbypass.js"
    ]
    try:
        subprocess.run(frida_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"{Color.RED}Error running Frida command for package identifier {package_identifier}: {e}{Color.END}")

# Main function
def main():
    # Start Frida server
    start_frida_server()

    # Print logo
    print(f"{Color.CYAN}{logo}{Color.END}")

    # Get package identifiers along with serial numbers
    package_data = get_package_names()

    # Print package identifiers with serial numbers
    print(f"{Color.YELLOW}Available packages:{Color.END}")
    for serial_number, package_identifier in package_data:
        print(f"{Color.GREEN}{serial_number}: {package_identifier}{Color.END}")

    # Prompt user to choose a serial number
    chosen_serial = input(f"{Color.BOLD}Choose the serial number of the package to run Frida command:=> {Color.END}")

    try:
        chosen_serial = int(chosen_serial)
        if chosen_serial < 1 or chosen_serial > len(package_data):
            print(f"{Color.RED}Invalid serial number.{Color.END}")
            return
    except ValueError:
        print(f"{Color.RED}Invalid input.{Color.END}")
        return

    chosen_package = package_data[chosen_serial - 1][1]
    print(f"{Color.YELLOW}Running Frida for package identifier: {chosen_package}{Color.END}")
    run_frida(chosen_package)

if __name__ == "__main__":
    main()
