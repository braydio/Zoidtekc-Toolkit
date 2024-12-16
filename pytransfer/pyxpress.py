import os
import sys
import json
import argparse
import paramiko
from scp import SCPClient
import getpass

# Modular Configuration
class Config:
    CONFIG_FILE = os.path.expanduser("~/.pyxpress_config.json")

    def __init__(self):
        self.ip_mappings = {}
        self.base_local_dir = os.path.expanduser("~/projects/for-me")
        self.base_remote_dir = os.path.expanduser("~/projects/from-me")
        self.default_user = getpass.getuser()  # Default to the current username
        self.user_mappings = {}  # Optional per-host username mappings
        self.load_config()

    def load_config(self):
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, "r") as file:
                    data = json.load(file)
                    self.ip_mappings = data.get("ip_mappings", {})
                    self.base_local_dir = data.get("base_local_dir", self.base_local_dir)
                    self.base_remote_dir = data.get("base_remote_dir", self.base_remote_dir)
                    self.default_user = data.get("default_user", self.default_user)
                    self.user_mappings = data.get("user_mappings", self.user_mappings)
            except json.JSONDecodeError:
                print("Warning: Config file is corrupted. Using default values.")

    def save_config(self):
        data = {
            "ip_mappings": self.ip_mappings,
            "base_local_dir": self.base_local_dir,
            "base_remote_dir": self.base_remote_dir,
            "default_user": self.default_user,
            "user_mappings": self.user_mappings
        }
        with open(self.CONFIG_FILE, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Configuration saved to {self.CONFIG_FILE}.")

    def get_username(self, host):
        return self.user_mappings.get(host, self.default_user)

# Core Utility Functions
def list_hosts(config):
    """Print the currently known hosts and their IPs."""
    if not config.ip_mappings:
        print("No hosts currently defined.")
        return
    print("\nCurrent Host Mappings:")
    for ip, name in config.ip_mappings.items():
        print(f"  {ip} -> {name}")
    print()

def add_host(config, hostname, ip):
    """Add a new host to the IP_MAPPINGS dictionary."""
    config.ip_mappings[ip] = hostname
    config.save_config()
    print(f"Host '{hostname}' with IP '{ip}' added to mappings and saved.")

def add_user_mapping(config, host, username):
    """Add or update a username for a specific host."""
    config.user_mappings[host] = username
    config.save_config()
    print(f"Username for host '{host}' updated to '{username}' and saved.")

def resolve_host(config, identifier):
    """
    Resolve an identifier which can be an IP or a name from IP_MAPPINGS.
    Returns tuple (ip, name) if found, else None.
    """
    if identifier in config.ip_mappings:
        return identifier, config.ip_mappings[identifier]
    elif identifier in config.ip_mappings.values():
        for saved_ip, name in config.ip_mappings.items():
            if name == identifier:
                return saved_ip, name
    return None

def send_file(local_file, remote_file, hostname, port, username, password, config):
    """
    Transfer a file from the local base directory to the remote base directory.
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    local_path = os.path.join(config.base_local_dir, local_file)
    remote_path = os.path.join(config.base_remote_dir, remote_file)

    if not os.path.exists(local_path):
        print(f"Local file {local_path} does not exist.")
        return

    try:
        ssh.connect(hostname=hostname, port=port, username=username, password=password)
        with SCPClient(ssh.get_transport()) as scp:
            scp.put(local_path, remote_path)
            print(f"Transferred {local_path} to {remote_path}")
    except Exception as e:
        print(f"An error occurred during transfer: {e}")
    finally:
        ssh.close()

def retrieve_file(remote_file, local_file, hostname, port, username, password, config):
    """
    Retrieve a file from the remote base directory to the local base directory.
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    local_path = os.path.join(config.base_local_dir, local_file)
    remote_path = os.path.join(config.base_remote_dir, remote_file)

    try:
        ssh.connect(hostname=hostname, port=port, username=username, password=password)
        with SCPClient(ssh.get_transport()) as scp:
            scp.get(remote_path, local_path)
            print(f"Retrieved {remote_path} to {local_path}")
    except Exception as e:
        print(f"An error occurred during retrieval: {e}")
    finally:
        ssh.close()


# Main Execution Logic
def main():
    parser = argparse.ArgumentParser(description="CLI-based File Transfer Utility with Host Mappings")
    parser.add_argument("-u", "--username", required=True, help="SSH username")
    parser.add_argument("-pw", "--password", help="SSH password")
    parser.add_argument("-ip", "--host", help="Host IP or name from predefined mappings")
    parser.add_argument("-p", "--port", type=int, default=22, help="SSH port (default: 22)")
    parser.add_argument("-ac", "--action", choices=["send", "retrieve"], help="Action to perform: send or retrieve")
    parser.add_argument("-lf", "--local-file", dest="local_file", help="Local file name")
    parser.add_argument("-rf", "--remote-file", dest="remote_file", help="Remote file name")
    parser.add_argument("-ah", "--add-host", nargs=2, metavar=("HOSTNAME","IP"), help="Add a new host to the mappings")
    parser.add_argument("-au", "--add-user", nargs=2, metavar=("HOST","USERNAME"), help="Add or update a username for a specific host")    
    parser.add_argument("-ls", "--list-hosts", action="store_true", help="List all known hosts and exit")

    args = parser.parse_args()
    config = Config()

    if args.add_host:
        add_host(config, *args.add_host)
        sys.exit(0)

    if args.add_user:
        add_user_mapping(config, *args.add_user)
        sys.exit(0)

    if args.list_hosts:
        list_hosts(config)
        sys.exit(0)

    if args.host:
        resolved = resolve_host(config, args.host)
        if not resolved:
            print(f"ERROR: Host '{args.host}' not found in mappings.")
            sys.exit(1)
        hostname, _ = resolved
    else:
        print("No host specified.")
        sys.exit(1)

    username = args.username or config.get_username(args.host)
    password = args.password or input("Enter the password: ").strip()
    action = args.action

    if action == "send":
        send_file(args.local_file, args.remote_file, hostname, args.port, username, password, config)
    elif action == "retrieve":
        retrieve_file(args.remote_file, args.local_file, hostname, args.port, username, password, config)
    else:
        print("Invalid action. Use 'send' or 'retrieve'.")

if __name__ == "__main__":
    main()
