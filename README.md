# EntomoloGUI
GUI for interfacing with the Pi-Eyes and Canons for the NHMD Pinned Insect Digitization Station

![plot](./media/gui.png)

# Installation Instructions
It is assumed this will be install on a Mac computer. Otherwise the instructions might need adjustment
1. Install homebrew (https://brew.sh/)
2. Install anaconda/python (https://docs.anaconda.com/anaconda/install/mac-os/)
3. Install git (run `brew install git`)
4. Clone git repository (`git clone https://github.com/NHMDenmark/EntomoloGUI.git`)
5. Install python packages from environment.yml
6. Make storage folder for images and update STORAGE_PATH in guis/settings/settings.py to said folder.
7. On the two canon cameras - ensure one has its owner (on the camera itself) set to 'Top' and the other set to 'Side'. This allows the GUI to figure out which is the 'top'/dorsal camera, and which is the side camera.
8. Ensure both the canon cameras are also set to never auto turn off (can be set in the settings)
9. Both canon cameras also require a sd card in them for temporary storage.


# TODO
1. Package everything into a portable app - Qsound does not seem to work in Automator.
2. We don't have enough usb ports for the keyboard, mouse and all the pi-eyes, so we need to get a different keyboard/mouse or buy another usb hub - for testing I am taking pieye-earwig out. 
