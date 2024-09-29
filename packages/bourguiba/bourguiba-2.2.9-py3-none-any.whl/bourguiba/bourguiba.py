import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from difflib import get_close_matches

class CommandGenerator:
    def __init__(self, model_name: str = 'gpt2'):
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name, clean_up_tokenization_spaces=True)
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        self.model.eval()
        self.common_commands = {
            'create folder': 'mkdir [folder_name]',
            'create directory': 'mkdir [directory_name]',
            'remove file': 'rm [file_name]',
            'delete file': 'rm [file_name]',
            'list files': 'ls [directory]',
            'change directory': 'cd [directory]',
            'move file': 'mv [source] [destination]',
            'copy file': 'cp [source] [destination]',
            'rename file': 'mv [old_name] [new_name]',
            'show file contents': 'cat [file_name]',
            'find file': 'find [directory] -name [file_name]',
            'search file content': 'grep [pattern] [file_name]',
            'create empty file': 'touch [file_name]',
            'move to folder': 'cd [folder_name]',
            'go to folder': 'cd [folder_name]',
            'print working directory': 'pwd',
            'clear terminal': 'clear',
            'display disk usage': 'df -h',
            'display memory usage': 'free -h',
            'change file permissions': 'chmod [permissions] [file_name]',
            'change file owner': 'chown [owner]:[group] [file_name]',
            'compress files': 'tar -czvf [archive_name].tar.gz [directory]',
            'extract files': 'tar -xzvf [archive_name].tar.gz',
            'download file': 'curl -O [url]',
            'upload file': 'curl -T [file_name] [url]',
            'display network information': 'ifconfig',
            'search for a process': 'ps aux | grep [process_name]',
            'kill a process': 'kill [process_id]',
            'create symbolic link': 'ln -s [target] [link_name]',
            'open file with editor': 'nano [file_name]',
            'display current date': 'date',
            'display file permissions': 'ls -l [file_name]',
            'find text in files': 'grep -r [text] [directory]',
            'show active network connections': 'netstat',
            'display system information': 'uname -a',
            'check disk space usage': 'du -sh [directory]',
            'view log files': 'tail -f [log_file]',
            'stop a service': 'systemctl stop [service_name]',
            'start a service': 'systemctl start [service_name]',
            'restart a service': 'systemctl restart [service_name]',
            'check service status': 'systemctl status [service_name]',
            'get environment variable': 'echo $[VARIABLE]',
            'set environment variable': 'export [VARIABLE]=[value]',
            'create a new user': 'sudo adduser [username]',
            'delete a user': 'sudo deluser [username]',
            'list users': 'cat /etc/passwd',
            'change user password': 'passwd [username]',
            'show running processes': 'top',
            'suspend a process': 'kill -STOP [process_id]',
            'resume a process': 'kill -CONT [process_id]',
            'check for system updates': 'sudo apt update',
            'upgrade installed packages': 'sudo apt upgrade',
            'install package': 'sudo apt install [package_name]',
            'remove package': 'sudo apt remove [package_name]',
            'search for a package': 'apt search [package_name]',
            'show disk partitions': 'lsblk',
            'mount a filesystem': 'mount [device] [mount_point]',
            'unmount a filesystem': 'umount [mount_point]',
            'display CPU information': 'lscpu',
            'display memory information': 'cat /proc/meminfo',
            'create a cron job': 'crontab -e',
            'list scheduled cron jobs': 'crontab -l',
            'scheduling a one-time job': 'at [time]',
            'view active cron jobs': 'systemctl list-timers',
            'get help on command': 'man [command]',
            'check internet connectivity': 'ping [hostname]',
            'download file using wget': 'wget [url]',
            'create a zip file': 'zip [zip_file_name] [file1] [file2]',
            'extract zip file': 'unzip [zip_file_name]',
            'display file type': 'file [file_name]',
            'show current working directory': 'pwd',
            'set file attributes': 'chattr [attributes] [file_name]',
            'list network interfaces': 'ip a',
            'get public IP address': 'curl ifconfig.me',
            'check listening ports': 'netstat -tuln',
            'list all installed packages': 'dpkg --get-selections',
            'check for broken packages': 'dpkg --check-broken',
            'clean up package cache': 'sudo apt clean',
            'view disk usage by directory': 'du -h --max-depth=1',
            'export file to a different format': 'convert [input_file] [output_file]',
            'view the first lines of a file': 'head [file_name]',
            'view the last lines of a file': 'tail [file_name]',
            'search in command history': 'history | grep [command]',
            'backup a directory': 'cp -r [source_directory] [backup_directory]',
            'restore a backup': 'cp -r [backup_directory] [source_directory]',
            'list hidden files': 'ls -a',
            'view system logs': 'journalctl',
            'shutdown the system': 'shutdown now',
            'restart the system': 'reboot',
            'power off the system': 'poweroff',
            'create a temporary file': 'mktemp',
            'show the current user': 'whoami',
            'check active user sessions': 'w',
            'show user login history': 'last',
            'display file checksum': 'md5sum [file_name]',
            'check running Docker containers': 'docker ps',
            'pull a Docker image': 'docker pull [image_name]',
            'run a Docker container': 'docker run [options] [image_name]',
            'list all Docker images': 'docker images',
            'stop a Docker container': 'docker stop [container_id]',
            'remove a Docker container': 'docker rm [container_id]',
            'remove a Docker image': 'docker rmi [image_name]',
            'check Git status': 'git status',
            'commit changes in Git': 'git commit -m "[message]"',
            'push changes to remote Git repository': 'git push',
            'clone a Git repository': 'git clone [repository_url]',
            'pull changes from remote Git repository': 'git pull',
            'create a new Git branch': 'git checkout -b [branch_name]',
            'switch to a different Git branch': 'git checkout [branch_name]',
            'merge branches in Git': 'git merge [branch_name]',
            'delete a Git branch': 'git branch -d [branch_name]',
            'view Git commit history': 'git log',
            'show differences between commits': 'git diff',
            'set Git user email': 'git config --global user.email "[email]"',
            'set Git user name': 'git config --global user.name "[name]"',
            'initialize a new Git repository': 'git init',
            'check memory usage by process': 'pmap [process_id]',
            'show network routes': 'ip route',
            'enable a service on boot': 'systemctl enable [service_name]',
            'disable a service on boot': 'systemctl disable [service_name]',
            'get current shell': 'echo $SHELL',
            'view shell environment variables': 'env',
            'set a temporary shell variable': 'export [VARIABLE]=[value]',
            'display all available shell built-in commands': 'help',
            'get the current terminal size': 'stty size',
            'show the current shell history': 'history',
            'execute a command as another user': 'sudo -u [user] [command]',
            'create a directory and move into it': 'mkdir [folder_name] && cd $_',
            'remove a directory recursively': 'rm -r [directory_name]',
            'search for files by name': 'find / -name "[file_name]"',
            'search for files by type': 'find . -type [file_type]',
            'list files with detailed information': 'ls -lh',
            'count lines in a file': 'wc -l [file_name]',
            'compress files into a zip archive': 'zip -r [archive_name].zip [directory]',
            'decompress zip archive': 'unzip [archive_name].zip',
            'compress files using tar': 'tar -czf [archive_name].tar.gz [directory]',
            'decompress tar.gz archive': 'tar -xzf [archive_name].tar.gz',
            'view running services': 'service --status-all',
            'check system uptime': 'uptime',
            'list current environment variables': 'printenv',
            'get help on a specific command': 'man [command]',
            'check the size of a directory': 'du -sh [directory]',
            'display the last N lines of a file': 'tail -n [number] [file_name]',
            'show the first N lines of a file': 'head -n [number] [file_name]',
            'download file using curl': 'curl -O [url]',
            'upload file using curl': 'curl -T [file_name] [url]',
            'create a new file and open it': 'nano [file_name]',
            'display disk usage summary': 'df -h',
            'check installed software versions': 'apt list --installed',
            'check the logs of a specific service': 'journalctl -u [service_name]',
        }

    def generate_command(self, prompt: str) -> str:
        # Check if the prompt matches any common commands with fuzzy matching
        lower_prompt = prompt.lower()
        command_keys = self.common_commands.keys()
        
        # Get the closest match if no direct match is found
        closest_match = get_close_matches(lower_prompt, command_keys, n=1)
        if closest_match:
            return self.common_commands[closest_match[0]]

        # If no match found, use the AI model
        input_text = f"Generate a shell command to {prompt}. Make sure the command is practical and commonly used:\n$ "
        input_ids = self.tokenizer.encode(input_text, return_tensors='pt')
        attention_mask = torch.ones_like(input_ids)

        with torch.no_grad():
            output = self.model.generate(
                input_ids,
                attention_mask=attention_mask,
                max_length=50,
                num_return_sequences=1,
                do_sample=True,
                temperature=0.7,
                top_k=50,
                top_p=0.95,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        generated_command = self.extract_command(self.tokenizer.decode(output[0], skip_special_tokens=True))
        
        return generated_command if self.is_valid_command(generated_command) else "No valid command generated."

    def extract_command(self, generated_text: str) -> str:
        lines = generated_text.splitlines()
        for line in lines:
            if line.startswith('$'):
                return line.strip('$ ').strip()
        return ""

    @staticmethod
    def is_valid_command(command: str) -> bool:
        common_prefixes = [
            'mkdir', 'cd', 'ls', 'cp', 'mv', 'rm', 'touch', 'echo', 'cat',
            'grep', 'sed', 'awk', 'find', 'pwd', 'clear', 'df', 'free',
            'chmod', 'chown', 'tar', 'curl', 'ifconfig', 'ps', 'kill', 'ln', 'nano',
            'zip', 'unzip', 'wget', 'date', 'man', 'apt', 'docker', 'git', 'systemctl',
            'journalctl', 'crontab', 'ping', 'at', 'tail', 'head', 'whoami', 'history',
            'printenv', 'env', 'stty', 'service', 'ifconfig', 'lscpu', 'du', 'df',
            'netstat', 'ip', 'shutdown', 'reboot', 'poweroff', 'pmap', 'last',
            'echo', 'mktemp', 'kill', 'bg', 'fg', 'jobs', 'ps', 'sudo', 'chattr',
            'killall', 'uname', 'free', 'uptime', 'hostname', 'arch', 'lsblk', 'mount',
            'umount', 'chmod', 'lsusb', 'lsmod', 'dmesg', 'df', 'du', 'echo',
            'clear', 'cat', 'less', 'more', 'tail', 'head', 'cut', 'paste', 'sort',
            'uniq', 'join', 'split', 'wc', 'tac', 'tee', 'grep', 'sed', 'awk',
            'xargs', 'find', 'locate', 'updatedb', 'history', 'cut', 'paste', 'tr',
            'printf', 'read', 'select', 'eval', 'export', 'let', 'declare', 'readonly',
            'alias', 'unalias', 'set', 'unset', 'shopt', 'pushd', 'popd', 'dirs',
            'push', 'pop', 'basename', 'dirname', 'dirname', 'dirname', 'basename',
            'nl', 'diff', 'patch', 'cmp', 'join', 'tee', 'bg', 'fg', 'jobs', 'kill',
            'exec', 'logout', 'exit', 'sudo', 'chown', 'chgrp', 'chmod', 'df',
            'du', 'du', 'df', 'mount', 'umount', 'fsck', 'blkid', 'mkfs', 'fdisk',
            'parted', 'df', 'du', 'mount', 'umount', 'fsck', 'mkfs', 'chroot', 'resize2fs',
            'tune2fs', 'cryptsetup', 'lvm', 'btrfs', 'zfs', 'dmsetup', 'luks',
            'lsmod', 'modprobe', 'rmmod', 'insmod', 'lsmod', 'modinfo', 'modprobe',
            'rmmod', 'lsmod', 'cat', 'tail', 'head', 'diff', 'cmp', 'sort', 'uniq'
        ]
        return any(command.startswith(prefix) for prefix in common_prefixes)

def main():
    generator = CommandGenerator()
    print("Welcome to the Hybrid Command Generator!")
    print("Type 'quit' to exit.\n")

    while True:
        user_input = input("Enter command description (or 'quit' to exit): ").strip()
        if user_input.lower() == 'quit':
            break
        command = generator.generate_command(user_input)
        # Display only the command without extra phrases
        print(f"Generated command: {command}")

    print("Thank you for using the Hybrid Command Generator. Goodbye!")

if __name__ == '__main__':
    main()
