import os, time, glob
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .generate_gtw import generate_gtw_files

"""
Because Python's standard output is buffered by default. 
This means that the output is temporarily stored in a buffer and not actually written to the console or file until the buffer is full or the program ends. 
Fortunately, there are several ways to globally make all print statements output immediately.

Method 1: Run Python scripts with the -u option

The easiest way is to use the -u option when running the script, which tells the Python interpreter to run in unbuffered mode.
However, this will make the standard output and standard error output of the entire program unbuffered, 
which may have a slight impact on performance, especially in the case of large amounts of output.

Usage:
    $ python -u your_script.py
    
Method 2: Modify sys.stdout in the code

You can make all output flush immediately by setting the buffering mode of sys.stdout in the code.

Usage:
    >>> import sys
    >>> sys.stdout.reconfigure(line_buffering=True)

Method 3: Redefine the print function

You can redefine the print function at the beginning of the code to use flush=True by default.  

Usage:
    >>> import sysimport functools
    >>> print = functools.partial(print, flush=True)  
"""

# Define timeout and polling interval
TIMEOUT = 10 * 60  # 10 minutes
POLLING_INTERVAL = 5  # Check every 5 seconds

def _find_success_file(directory):
    """
    Check if there is a file named 'success' with any extension in the given directory.

    Inputs:
        directory -> [str] The directory to search for the 'success' file.

    Returns:
        [bool] True if a 'success' file is found, otherwise False.
    """
    success_file = glob.glob(os.path.join(directory, 'success.*'))
    return len(success_file) > 0

def check_gtw_completed(ipd_success,gtw_dir,timeout=5):
    """
    Monitor the GTW directory and check if all files have been generated. The function
    continuously checks the modification time of the files in the GTW directory. If there
    are no file modifications within the specified timeout period, it creates a success.fin
    file indicating that all GTW files have been generated.

    Inputs:
        ipd_success -> [bool] If a success.fin file is found in the IPD directory,
                              it indicates that IPD files are complete and can be further processed,
                              then ipd_success is assigned True, otherwise False.
        gtw_dir -> [str] The directory where GTW files are stored.
        timeout -> [int, optional, default=5] The amount of time (in seconds) to wait for file modifications
        before considering the process complete.
    """
    if not ipd_success: return

    last_mod_time = time.time()
    polling_interval = 2  # Check every 2 seconds

    while True:
        current_mod_time = max(os.path.getmtime(os.path.join(gtw_dir, f)) for f in os.listdir(gtw_dir))
        if current_mod_time > last_mod_time:
            last_mod_time = current_mod_time  # Update the last modification time
            print("IPD files are still being modified...")
        else:
            # If no file modifications within the timeout, assume generation is complete
            if time.time() - last_mod_time >= timeout:
                # Create an empty success.fin file
                success_file_path = os.path.join(gtw_dir, 'success.fin')
                open(success_file_path, 'w').close()
                print("All GTW files have been generated successfully.\n")
                break
        time.sleep(polling_interval)

def run_ipd_listfile_monitor(root_dir, eph_path, att_path, output_dir, ipd_list_file='IPD.list'):
    """
    Function to run the file system observer for IPD.list file.

    Usage:
        >>> inputFilePath = 'S12345'
        >>> eph_path = '20240829_IPDGTW/AUX/EPH/9511_P202408281011_012346_L0_GEOGC.eph'
        >>> att_path = '20240829_IPDGTW/AUX/POS/9511_P202408281011_012346_L0_GEOGC.pos'
        >>> run_ipd_listfile_monitor(inputFilePath, eph_path, att_path)

    Inputs:
        root_dir -> [string] Input base directory.
        eph_path -> [string] EPH file path.
        att_path -> [string] ATT file path.
        output_dir -> [string] Output base directory.
        ipd_list_file -> [str,optional,default='IPD.list'] Filename of the IPD list file to monitor,
        where each line records a storage directory of a group of IPD files relative to the base directory.
    """
    # Check if success.fin already exists before starting the observer
    if _find_success_file(root_dir):
        print(f"Detected success.fin in {root_dir} at startup, exiting immediately.")
        return

    ipd_list_path = os.path.join(root_dir, ipd_list_file)
    if not os.path.exists(ipd_list_path):
        print(f"No {ipd_list_file} file detected in {root_dir} at startup, exiting immediately.")
        return

    observer = Observer()
    event_handler = IPDFileHandler(root_dir, ipd_list_file, eph_path, att_path, output_dir, observer)
    observer.schedule(event_handler, root_dir, recursive=False)
    observer.start()

    try:
        # Keep the main loop running until _stop_loop is set to True
        while not getattr(event_handler, '_stop_loop', False):
            time.sleep(1)  # Keep the main thread running
    except KeyboardInterrupt:
        observer.stop()  # Stop the observer on keyboard interrupt
    finally:
        observer.join()  # Ensure observer thread is properly cleaned up

def run_ipd_dir_monitor(root_dir, eph_path, att_path, output_dir):
    """
    Function to run the file system observer for directory of IPD file.

    Usage:
        >>> inputFilePath = 'S12345'
        >>> eph_path = '20240829_IPDGTW/AUX/EPH/9511_P202408281011_012346_L0_GEOGC.eph'
        >>> att_path = '20240829_IPDGTW/AUX/POS/9511_P202408281011_012346_L0_GEOGC.pos'
        >>> run_ipd_dir_monitor(inputFilePath, eph_path, att_path)

    Inputs:
        root_dir -> [string] Input base directory.
        eph_path -> [string] EPH file path.
        att_path -> [string] ATT file path.
        output_dir -> [string] Output base directory.
    """
    # Check if success.fin already exists before starting the observer
    if _find_success_file(root_dir):
        print(f"Detected success.fin in {root_dir} at startup, exiting immediately.")
        return

    observer = Observer()
    event_handler = IPDDirHandler(root_dir, eph_path, att_path, output_dir, observer)
    observer.schedule(event_handler, root_dir, recursive=True)  # Recursive monitoring
    observer.start()  # Start the observer

    try:
        # Keep the main loop running until _stop_loop is set to True
        while not getattr(event_handler, '_stop_loop', False):
            time.sleep(1)  # Keep the main thread running
    except KeyboardInterrupt:
        observer.stop()  # Stop the observer on keyboard interrupt
    finally:
        observer.join()  # Ensure observer thread is properly cleaned up

class IPDFileHandler(FileSystemEventHandler):
    """
    Event handler class for monitoring the change of the IPD list file.
    """
    def __init__(self, root_dir, ipd_list_file, eph_path, att_path, output_dir, observer):
        """
        Initialize the IPDFileHandler with the base directory, filename of the IPD list file, path to the EPH file and ATT file.

        Inputs:
            root_dir -> [string] Input base directory.
            ipd_list_file -> [string] Filename of the IPD list file to monitor.
            eph_path -> [string] The path to the EPH file.
            att_path -> [string] The path to the ATT file.
            output_dir -> [string] Output base directory.
            observer -> [Observer] The observer instance used to stop monitoring.
        """
        # Path to the IPD list file to monitor
        ipd_list_path = os.path.join(root_dir, ipd_list_file)
        self.root_dir = root_dir  # Input base directory
        self.ipd_list_path = ipd_list_path # Path to the IPD list file to monitor
        self.eph_path = eph_path  # Path to the EPH file
        self.att_path = att_path  # Path to the ATT file
        self.output_dir = output_dir  # Output base directory
        self.observer = observer  # Observer instance
        self.processed_dirs = set()  # Keep track of processed directories

        # On startup, process any existing entries
        self.process_new_entries(first_run=True)

    def on_modified(self, event):
        """
        Event handler called when the IPD list file is modified.

        Inputs:
            event -> [FileSystemEvent] The event object containing information about the modification.
        """
        if event.src_path == self.ipd_list_path:
            print(f"{event.src_path} has been modified.")
            self.process_new_entries()

        # Check for success.fin in the root directory and stop the observer if found
        if _find_success_file(self.root_dir):
            print(f"Detected success.fin in {self.root_dir}, stopping observer.")
            self.observer.stop()
            self._stop_loop = True  # Set a flag to stop the main loop

    def process_new_entries(self, first_run=False):
        """
        Read the IPD list file and process new directory entries.

        Inputs:
            first_run -> [bool, optional, default=False] Indicates if this is the initial processing on startup.
        """
        with open(self.ipd_list_path, 'r') as f:
            lines = [line.strip() for line in f]

        if first_run:
            # On first run, process all entries
            new_entries = lines
        else:
            # Identify new entries that haven't been processed yet
            new_entries = [line for line in lines if line not in self.processed_dirs]

        if new_entries:
            for entry in new_entries:
                self.process_directory(entry)
                self.processed_dirs.add(entry)
                self.check_gtw_completed()
        else:
            if not first_run:
                print("No new entries to process.")

        # Check for success.fin in the root directory and stop the observer if found
        if _find_success_file(self.root_dir):
            print(f"Detected success.fin in {self.root_dir}, stopping observer.")
            self.observer.stop()
            self._stop_loop = True  # Set a flag to stop the main loop

    def process_directory(self, directory):
        """
        Process the directory specified in the entry.

        Inputs:
            directory -> [str] The directory relative to the base directory.
        """

        # Set up directories
        self.ipd_dir = os.path.join(self.root_dir, directory)
        self.gtw_dir = os.path.join(self.output_dir, 'L2/GTW')
        self.res_dir = os.path.join(self.output_dir, 'L2/RES')
        self.ipd_success = False

        start_time = time.time()

        # Check if the directory exists
        if os.path.exists(self.ipd_dir):
            print(f"Processing entry: {self.ipd_dir}")

            while True:
                if _find_success_file(self.ipd_dir):
                    print(f"Found success.fin in {self.ipd_dir}, proceeding to process IPD files.")
                    # Call the generate_gtw_files function to process the IPD files
                    generate_gtw_files(self.ipd_dir, self.gtw_dir, self.res_dir, self.eph_path, self.att_path)
                    self.ipd_success = True
                    break
                elif time.time() - start_time > TIMEOUT:
                    print(f"Timeout while waiting for success.fin in {self.ipd_dir}.")
                    break
                else:
                    print(f"Waiting for success.fin in {self.ipd_dir}...")
                    time.sleep(POLLING_INTERVAL)  # Wait for a few seconds before checking again
        else:
            print(f"Directory does not exist: {self.ipd_dir}")

    def check_gtw_completed(self, timeout=5):
        """
        Monitor the GTW directory and check if all files have been generated. The function
        continuously checks the modification time of the files in the GTW directory. If there
        are no file modifications within the specified timeout period, it creates a success.fin
        file indicating that all GTW files have been generated.

        Inputs:
            timeout -> [int, optional, default=5] The amount of time (in seconds) to wait for file modifications
            before considering the process complete.
        """
        check_gtw_completed(self.ipd_success,self.gtw_dir,timeout)

class IPDDirHandler(FileSystemEventHandler):
    """
    Event handler class for monitoring the creation of IPD directories.
    """
    def __init__(self, root_dir, eph_path, att_path, output_dir, observer):
        """
        Initialize the IPDDirHandler class with the root directory, EPH file path, and ATT file path.

        Inputs:
            root_dir -> [string] The root directory to monitor.
            eph_path -> [string] The path to the EPH file.
            att_path -> [string] The path to the ATT file.
            observer -> [Observer] The observer instance used to stop monitoring.
        """
        self.root_dir = root_dir  # Input base directory to monitor
        self.eph_path = eph_path  # Path to the EPH file
        self.att_path = att_path  # Path to the ATT file
        self.output_dir = output_dir # Output base directory
        self.observer = observer  # Observer instance

    def on_created(self, event):
        """
        Event handler triggered when a new directory is created. If the directory ends with 'IPD',
        it sets up the corresponding GTW and RES directories and checks for the success.fin file.

        Inputs:
            event -> [watchdog.Event] The event object containing information about the created directory.
        """
        if event.is_directory and event.src_path.endswith('IPD'):
            print(f"New dir created: {event.src_path}")

            # Set up directories
            self.ipd_dir = event.src_path
            self.gtw_dir = os.path.join(self.output_dir, 'L2/GTW')
            self.res_dir = os.path.join(self.output_dir, 'L2/RES')
            self.ipd_success = False

            # Check for success.fin in IPD and GTW file generation completion
            self.check_success_fin()
            self.check_gtw_completed()

        # Check for success.fin in the root directory and stop the observer if found
        if _find_success_file(self.root_dir):
            print(f"Detected success.fin in {self.root_dir}, stopping observer.")
            self.observer.stop()
            self._stop_loop = True  # Set a flag to stop the main loop

    def check_success_fin(self):
        """
        Continuously check for the existence of the success.fin file in the IPD directory.
        If the success.fin file is found, the generate_gtw_files function is called to process
        the files. This function will time out after 10 minutes if the file is not found.
        """
        start_time = time.time()

        while True:
            if _find_success_file(self.ipd_dir):
                print(f"Found success.fin in {self.ipd_dir}, proceeding to process IPD files.")
                # Call the generate_gtw_files function to process the IPD files
                generate_gtw_files(self.ipd_dir, self.gtw_dir, self.res_dir, self.eph_path, self.att_path)
                self.ipd_success = True
                break
            elif time.time() - start_time > TIMEOUT:
                print(f"Timeout while waiting for success.fin in {self.ipd_dir}.")
                break
            else:
                print(f"Waiting for success.fin in {self.ipd_dir}...")
                time.sleep(POLLING_INTERVAL)  # Wait for a few seconds before checking again

    def check_gtw_completed(self, timeout=5):
        """
        Monitor the GTW directory and check if all files have been generated. The function
        continuously checks the modification time of the files in the GTW directory. If there
        are no file modifications within the specified timeout period, it creates a success.fin
        file indicating that all GTW files have been generated.

        Inputs:
            timeout -> [int, optional, default=5] The amount of time (in seconds) to wait for file modifications
            before considering the process complete.
        """
        check_gtw_completed(self.ipd_success,self.gtw_dir,timeout)

