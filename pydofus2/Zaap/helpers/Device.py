import hashlib
import math
import os
import platform
import re
import subprocess

import psutil
import pythoncom  # Ensure pythoncom is imported


class Device:
    __uuid = None

    @staticmethod
    def get_os_name():
        os_name_map = {
            "Windows": "WINDOWS",
            "Darwin": "MACOS",
            "Linux": "LINUX"
        }
        return os_name_map.get(platform.system())

    @staticmethod
    def get_uuid():
        if Device.__uuid:
            return Device.__uuid

        id = Device.machine_id()
        print(f"Machine id : {id}")
        cpu_count, cpu_model = Device.get_cpu_info()
        print(f"cpu_count : {cpu_count}, cpu_model : {cpu_model}")
        plt, arch = Device.get_platform_and_architecture()
        Device.__uuid = ",".join([plt, arch, id, str(cpu_count), cpu_model])
        return Device.__uuid

    @staticmethod
    def get_platform_and_architecture():
        # Map Python's platform.system() to JavaScript's os.platform() style
        system_map = {
            'Windows': 'win32',
            'Darwin': 'darwin',
            'Linux': 'linux'
        }
        plt = system_map.get(platform.system(), platform.system().lower())

        # Map Python's platform.machine() to JavaScript's os.arch() style
        arch_map = {
            'AMD64': 'x64',
            'x86_64': 'x64',
            'i386': 'x86',
            'i686': 'x86'
        }
        arch = arch_map.get(platform.machine(), platform.machine())

        return plt, arch
    
    @staticmethod
    def get_cpu_info():
        cpu_count = psutil.cpu_count(logical=True)  # Number of physical cores
        cpu_model = None
        
        # For Windows
        if psutil.WINDOWS:
            try:
                pythoncom.CoInitialize()
                import wmi
                w = wmi.WMI()
            except Exception as e:
                print(f"Error while getting wmi : {e}")
            cpu_info = w.Win32_Processor()[0]
            cpu_model = cpu_info.Name
            print(f"cpu_model : {cpu_model}")
            
        # For Unix/Linux
        elif psutil.LINUX or psutil.MACOS or psutil.UNIX:
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if "model name" in line:
                        cpu_model = line.split(":")[1].strip()
                        break

        return cpu_count, cpu_model
    
    @staticmethod
    def get_computer_ram():
        ram_mb = int(psutil.virtual_memory().total / (1024 ** 2))
        return int(2 ** round(math.log(ram_mb, 2)))

    @staticmethod
    def get_os_version():
        return int('.'.join(platform.release().split(".")[:2]))

    @staticmethod
    def get_uuid_cmd_per_platform():
        plt = platform.system().lower()
        arch = platform.machine().lower()

        if plt == "darwin":
            return "ioreg -rd1 -c IOPlatformExpertDevice"
        elif plt == "linux":
            return "( cat /var/lib/dbus/machine-id /etc/machine-id 2> /dev/null || hostname ) | head -n 1 || :"
        elif plt == "freebsd":
            return "kenv -q smbios.system.uuid || sysctl -n kern.hostuuid"
        elif plt == "windows":
            if arch == "ia32" and "PROCESSOR_ARCHITEW6432" in os.environ:
                return "%windir%\\sysnative\\cmd.exe /c %windir%\\System32\\REG.exe QUERY HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Cryptography /v MachineGuid"
            else:
                return "%windir%\\System32\\REG.exe QUERY HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Cryptography /v MachineGuid"
        else:
            raise Exception("Unsupported platform: " + plt)

    @staticmethod
    def hash_with_sha256(string):
        hash_obj = hashlib.sha256(string.encode())
        return hash_obj.hexdigest()

    @staticmethod
    def parse_machine_guuid(std_out):
        plt = platform.system().lower()

        if plt == "darwin":
            return re.search("IOPlatformUUID.*?=\s*\"(.*?)\"", std_out, re.IGNORECASE).group(1).lower()
        elif plt in ["linux", "freebsd"]:
            return std_out.strip().lower()
        elif plt == "windows":
            return re.search("REG_SZ\s+(.*?)\s*$", std_out, re.IGNORECASE).group(1).lower()
        else:
            raise Exception("Unsupported platform: " + plt)

    def get_machine_guid_windows():
        import winreg

        # Define the registry path and key
        registry_path = r"SOFTWARE\Microsoft\Cryptography"
        key_name = "MachineGuid"
        try:
            # Connect to the registry
            with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as hkey:
                # Open the key
                with winreg.OpenKey(hkey, registry_path) as reg_key:
                    # Read the value
                    value, _ = winreg.QueryValueEx(reg_key, key_name)
                    return value
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    @staticmethod
    def machine_id(with_sha256_hash=True):
        try:
            plt = platform.system().lower()
            if plt == "windows":
                machine_uuid = Device.get_machine_guid_windows()
            else:
                cmd = Device.get_uuid_cmd_per_platform()
                output = subprocess.check_output(cmd, shell=True, text=True)
                machine_uuid = Device.parse_machine_guuid(output)
            return Device.hash_with_sha256(machine_uuid) if with_sha256_hash else machine_uuid
        except subprocess.CalledProcessError as e:
            raise Exception("Error while obtaining machine id: " + str(e))
