import os
import sys
import json
import uuid
import logging
import ipaddress
import traceback
import threading
import subprocess
from time import time
from time import sleep
from typing import List
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from .net_tools import Device
from .decorators import job_tracker
from .ip_parser import parse_ip_input
from .port_manager import PortManager

JOB_DIR = './lanscape-jobs/'
SAVE_FREQUENCY = 1 # seconds



class SubnetScanner:
    def __init__(
            self, 
            subnet: str, 
            port_list: str,
            parallelism: float = 1.0,
            uid: str = None
        ):
        self.subnet = parse_ip_input(subnet)
        self.port_list = port_list
        self.ports: list = PortManager().get_port_list(port_list).keys()
        self.running = False
        self.parallelism: float = float(parallelism)
        self.subnet_str = subnet
        self.job_stats = {'running': {}, 'finished': {}, 'timing': {}}
        self.uid = uid if uid else str(uuid.uuid4())
        self.results = ScannerResults(self)
        self.log: logging.Logger = logging.getLogger('SubnetScanner')
        self.log.debug(f'Instantiated with uid: {self.uid}')
        self.log.debug(f'Port Count: {len(self.ports)} | Device Count: {len(self.subnet)}')

    def scan_subnet_threaded(self) -> threading.Thread:
        """
        Start a new thread to scan the subnet.
        """
        t = threading.Thread(target=self.scan_subnet)
        t.start()
        return t
    
    @staticmethod
    def scan_subnet_standalone(subnet: str, port_list: str, parallelism: float = 1.0):
        """
        Use shell to start a new process for subnet scan.
        """
        scan = SubnetScanner(subnet, port_list, parallelism)
        scan.results.save()

        try:
            scanner_path = Path(__file__).parent.parent / 'scanner.py'
        except:
            scanner_path = 'scanner.py'

        try:
            subprocess.Popen(
                [sys.executable, scanner_path, scan.uid],
                stdout=None, stderr=None, stdin=None, close_fds=True
            )
            sleep(1)
            if not ScannerResults.get_scan(scan.uid)['running']:
                raise Exception('Could not start scanner in new process')

            
        except Exception:
            scan.log.debug(traceback.format_exc())
            scan.log.warning('unable to start standalone scanner')
            scan.scan_subnet_threaded()
        return scan.uid
    
    @staticmethod
    def instantiate_scan(scan_id: str) -> 'SubnetScanner':
        """
        Load a scan by its unique ID.
        """
        scan = SubnetScanner.get_scan(scan_id)
        return SubnetScanner(scan['subnet'], scan['port_list'], scan['parallelism'], scan['uid'])
    

    @staticmethod
    def get_scan(scan_id) -> dict:
        """
        Load a scan by its unique ID.
        """
        return ScannerResults.get_scan(scan_id)
    
    def scan_subnet(self):
        """
        Scan the subnet for devices and open ports.
        """
        self._set_stage('scanning devices')
        self.running = True
        self.results.auto_save()
        with ThreadPoolExecutor(max_workers=self._t_cnt(256)) as executor:
            futures = {executor.submit(self._get_host_details, str(ip)): str(ip) for ip in self.subnet}
            for future in futures:
                ip = futures[future]
                try:
                    future.result()
                except Exception as e:
                    self.log.error(f'[{ip}] scan failed. details below:\n{traceback.format_exc()}')
                    self.results.errors.append({
                        'basic': f"Error scanning IP {ip}: {e}",
                        'traceback': traceback.format_exc(),
                    })
                
        
        self._set_stage('testing ports')
        self._scan_network_ports()

        self._set_stage('complete')
        self.running = False
        self.results.save() # manual save to ensure latest is live
        return self.results
        

    def debug_active_scan(self):
        """
            Run this after running scan_subnet_threaded 
            to see the progress of the scan
        """
        while self.running:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f'{self.uid} - {self.subnet_str}')
            print(f"Scanned: {self.results.devices_scanned}/{self.results.devices_total}")
            print(f"Alive: {len(self.results.devices)}")
            print(f"Running jobs:  {self.job_stats['running']}")
            print(f"Finished jobs: {self.job_stats['finished']}")
            print(f"Job timing:    {self.job_stats['timing']}")
            sleep(1)


    
    def _get_host_details(self, host: str):
        """
        Get the MAC address and open ports of the given host.
        """
        device = Device(host)
        is_alive = self._ping(device)
        self.results.scanned()
        if not is_alive:
            return None
        self.log.debug(f'[{host}] is alive, getting metadata')
        
        device.get_metadata()
        self.results.devices.append(device)
        return True
        
    def _scan_network_ports(self):
        with ThreadPoolExecutor(max_workers=self._t_cnt(10)) as executor:
            futures = {executor.submit(self._scan_ports, device): device for device in self.results.devices}
            for future in futures:
                future.result()

    @job_tracker
    def _scan_ports(self, device: Device):
        self.log.debug(f'[{device.ip}] Initiating port scan')
        device.stage = 'scanning'
        with ThreadPoolExecutor(max_workers=self._t_cnt(128)) as executor:
            futures = {executor.submit(self._test_port, device, int(port)): port for port in self.ports}
            for future in futures:
                future.result()
        self.log.debug(f'[{device.ip}] Completed port scan')
        device.stage = 'complete'
    
    @job_tracker
    def _test_port(self,host: Device, port: int):
        """
        Test if a port is open on a given host.
        Device class handles tracking open ports.
        """
        return host.test_port(port)
    
        

    @job_tracker
    def _ping(self, host: Device):
        """
        Ping the given host and return True if it's reachable, False otherwise.
        """
        return host.is_alive(host.ip)
    
    def _t_cnt(self, base_threads: int) -> int:
        """
        Calculate the number of threads to use based on the base number 
        of threads and the parallelism factor.
        """
        return int(base_threads * self.parallelism)
    
    def _set_stage(self,stage):
        self.log.debug(f'[{self.uid}] Moving to Stage: {stage}')
        self.results.stage = stage
    
class ScannerResults:
    def __init__(self,scan: SubnetScanner):
        self.scan = scan
        self.port_list: str = scan.port_list
        self.subnet: str = scan.subnet_str
        self.parallelism: float = scan.parallelism
        self.uid = scan.uid

        self.devices_total: int = len(list(scan.subnet))
        self.devices_alive: int = 0
        self.devices_scanned: int = 0
        self.devices: List[Device] = []

        self.errors: List[str] = []        
        self.running: bool = False
        self.start_time: float = time()
        self.run_time: int = 0
        self.stage = 'instantiated'

        self.log = logging.getLogger('ScannerResults')
        self.log.debug(f'Instantiated Logger For Scan: {self.scan.uid}')

    @staticmethod
    def get_scan(scan_id: str):
        """
        load scan by scan id
        """

        for i in range(5):
            try:
                with open(f'{JOB_DIR}{scan_id}.json', 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                sleep(1)

        raise json.JSONDecodeError('Could not load scan data')

    def scanned(self):
        self.devices_scanned += 1
        
    def auto_save(self):
        threading.Thread(target=self._save_thread).start()
    
    def save(self):
        Path(JOB_DIR).mkdir(parents=True, exist_ok=True)
        self.log.debug(f"Saving Results. Threads: {self.scan.job_stats.get('running')}")

        self.running = self.scan.running
        self.run_time = int(round(time() - self.start_time,0))
        self.devices_alive = len(self.devices)

        out = vars(self).copy()
        out.pop('scan')
        out.pop('log')
        
        devices: Device = out.pop('devices')
        sortedDevices = sorted(devices, key=lambda obj: ipaddress.IPv4Address(obj.ip))
        out['devices'] = [vars(device).copy() for device in sortedDevices]
        for device in out['devices']: device.pop('log') 

        with open(f'{JOB_DIR}{self.uid}.json', 'w') as f:
            json.dump(out, f,indent=2)
    def _save_thread(self):
        while self.scan.running:
            self.save()
            sleep(SAVE_FREQUENCY)
        self.save()

            
def cleanup_old_jobs(older_than=0):
    """
    Removes removes jobs (scans) from the execution directory.
    Optional param to filter jobs older than (seconds).
    """
    for file in os.listdir(JOB_DIR):
        if file.endswith('.json'):
            file_path = f'{JOB_DIR}{file}'
            if time() - os.path.getmtime(file_path) > older_than:
                os.remove(file_path)