# EntomoloGUI
GUI for interfacing with the Pi-Eyes and Canons for the NHMD Pinned Insect Digitization Station

# Installation Instructions
It is assumed this will be install on a Mac computer. Otherwise the instructions might need adjustment
1. Install homebrew (https://brew.sh/)
2. Install anaconda/python (https://docs.anaconda.com/anaconda/install/mac-os/)
3. Install git (run `brew install git`)
4. Clone git repository (`git clone https://github.com/NHMDenmark/EntomoloGUI.git`)
5. Install python packages from environment.yml
5. TODO : Make a link to a run file.
6. Make storage folder for images and update STORAGE_PATH in guis/settings/settings.py to this folder.
7. On the two canon cameras - ensure one has its owner (on the camera itself) set to 'Top' and the other set to 'Side'. This allows the GUI to figure out which is the 'top'/dorsal camera, and which is the side camera.
8. Ensure both the canon cameras are also set to never auto turn off (can be set in the settings)
9. Both canon cameras also require a sd card in them for temporary storage.


# TODO
1. Add Image of GUI to this README
2. Finalize installation instructions to this README - Will probably need to be done while everything is being installed
3. Package everything into a portable app
4. Update environment.yml for mac packages
5. Add timeout to utils.py/try_url
6. Check if plugins necessary in main.py
7. In savePhoto of CanonGUI - check if as_posix can be replaced by str(), and check if taking_photo = True required to download the image
8. In getPreview of CanonGUI - check if need to mutex around taking_photo thing there.