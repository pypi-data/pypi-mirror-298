import os
import paramiko
import sys
import time
import logging
import atexit
import signal


########################################################################
class WatchDogWorker:
    """"""

    hostname = os.environ['hostname']
    username = os.environ['username']
    password = os.environ['password']
    command = os.environ['command']

    # ----------------------------------------------------------------------
    def __init__(self):
        """"""
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the server
        self.client.connect(
            self.hostname, username=self.username, password=self.password
        )

        # Execute the command in the background and get the PID
        # The 'nohup' and '& echo $!' are used to run the command in the background and get its PID
        background_command = (
            f"nohup {self.command} > /dev/null 2>&1 & echo $!"
        )
        stdin, stdout, stderr = self.client.exec_command(background_command)

        # Read the output which should contain the PID
        output = stdout.read().decode('utf-8').strip()
        self.pid = int(output)
        logging.warning(f"Process started with PID: {self.pid}")

        # Registrar la función de limpieza
        atexit.register(self.kill_remote_process)

        # Registrar las señales para capturar interrupciones (Ctrl+C y SIGTERM)
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        logging.warning('Pre loop')
        self.monitor_remote_process()

    # ----------------------------------------------------------------------
    def monitor_remote_process(self):
        while True:
            logging.warning('Looping...')

            stdin, stdout, stderr = self.client.exec_command(
                f"ps -p {self.pid}"
            )

            output = stdout.read().decode('utf-8')

            logging.warning(f'XxX: stdout: {output}')
            logging.warning(f'XxX: stderr: {stderr.read().decode('utf-8')}')

            if len(output.splitlines()) > 1:
                logging.warning(
                    f"Process with PID {self.pid} is still running."
                )
            else:
                logging.warning(f"Process with PID {self.pid} has finished.")
                self.client.close()
                sys.exit(0)

            time.sleep(1)

    # ----------------------------------------------------------------------
    def kill_remote_process(self):
        try:
            kill_command = f"kill -9 {self.pid}"
            self.client.exec_command(kill_command)
        except Exception as e:
            pass

    # ----------------------------------------------------------------------
    def signal_handler(self, signum, frame):
        logging.warning(f"Signal {signum} received. Cleaning up...")
        self.kill_remote_process()
        sys.exit(0)


if __name__ == '__main__':
    WatchDogWorker()


if __name__ == '__main__':
    WatchDogWorker()
