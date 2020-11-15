# Audient EVO Linux tools
Python scripts for changing settings on Audent EVO 4 USB audio interfaces. Should also work with EVO 8, possibly with some simple modification (change product id?).

# How I made this
First I reverse engineered the USB interface by running the official EVO Control app on Windows, and listening to messages occuring over USB using Wireshark, and carefully examining outgoing data using a filter. Once I figured out the required USB messages that set the volume etc on the device, I used a simple python script (using pyusb library) to play back those USB messages to the device in Linux.  Used `lsusb` to figure out vendor and product ids.


# Installation & Usage
1. Ensure you have Python 3+ installed and then install pyusb

    ```pip install pyusb```

2. Optional: Add a udev rule so you dont need to run the python script with `sudo`

    ```sudo echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="2708", ATTR{idProduct}=="0006", MODE="0666"' | sudo tee /etc/udev/rules.d/70-audient.evo.rules```

3. Optional: Edit settings in the python script to your liking.

4. Run script, it will modify the settings on your Audient EVO 4 device (may require `sudo` if you skipped step 2)

    ```python evo4-settings.py```


# TODO
Suggestions/PRs welcome.
* Allow adjust settings without having to detach from kernel and re-attach
* Run in the background and save/restore any changes made using physical controls
* GUI for adjusting settings (e.g. Official Evo Control Windows/Mac app)
