from guis.basicGUI import basicGUI
import subprocess
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import os
import signal
import paramiko

class ShutdownPiGUI(basicGUI):

    def __init__(self, **kwargs):
        super(ShutdownPiGUI, self).__init__(**kwargs)
        
        self.initUI()

    def initUI(self):
        
        self.shutdownPisButton = QtWidgets.QPushButton("Shutdown Pieyes")
        self.shutdownPisButton.clicked.connect(self.shutdown_pi)
        self.shutdownPisButton.setStyleSheet("background-color: #d6e6ff;")
        self.grid.addWidget(self.shutdownPisButton, 0, 0, 9, 9)

        self.setLayout(self.grid)

    def shutdown_pieyes(self):

        path_to_shutdown_script = "./shutdown.sh"

        try:
            # Execute the shell script using subprocess
            subprocess.run(['sh', path_to_shutdown_script], check=True)
        except subprocess.CalledProcessError as e:
            QtWidgets.QMessageBox.critical(self, 'Error', f'Shell script failed with error: {str(e)}')

    def shutdown_pi(self):
        
        # Define your Raspberry Pi's SSH username and an array of hostnames
        USERNAME = "pi"
        PI_HOSTNAMES = ["pieye-ant.local", "pieye-beetle.local", "pieye-cicada.local", "pieye-dragonfly.local", "pieye-earwig.local"]

        # Set a timeout value for the SSH connection attempt (adjust as needed)
        SSH_TIMEOUT = 3    
        # Loop through the hostnames and shut down each Raspberry Pi
        for hostname in PI_HOSTNAMES:
            try:
                # Create an SSH client instance
                ssh_client = paramiko.SSHClient()

                # Automatically load keys from the SSH agent
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                # Connect to the Raspberry Pi
                ssh_client.connect(hostname, username=USERNAME, timeout=SSH_TIMEOUT)

                # Run the shutdown command
                stdin, stdout, stderr = ssh_client.exec_command("sudo shutdown -h now")

                # Wait for the command to complete
                stdout.channel.recv_exit_status()

                # Close the SSH connection
                ssh_client.close()

                print(f"Shut down {hostname} successfully.")
            except Exception as e:
                print(f"Failed to shut down {hostname}: {str(e)}")

class ShutdownGuiGUI(basicGUI):

    def __init__(self, **kwargs):
        super(ShutdownGuiGUI, self).__init__(**kwargs)
        
        self.initUI()

    def initUI(self):
        
        self.shutdownGuiButton = QtWidgets.QPushButton("Shutdown program")
        self.shutdownGuiButton.clicked.connect(self.shutdown_gui)
        self.shutdownGuiButton.setStyleSheet("background-color: #d6e6ff;")
        self.grid.addWidget(self.shutdownGuiButton, 0, 0, 9, 9)

        self.setLayout(self.grid)

    def shutdown_gui(self):
        # Get the PID of the current process
        pid = os.getpid()

        # Send a termination signal to the process
        os.kill(pid, signal.SIGTERM)