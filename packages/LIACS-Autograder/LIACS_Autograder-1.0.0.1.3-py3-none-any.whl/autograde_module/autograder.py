from pathlib import Path
import time
import re
from yaml import safe_load
import os

# tmp solution, search for the overall autograding directory and add it to path.
# try:
#     import sys
#     main_folder_name = "autograding"  # This could be in the overall .yml file
#     sys.path.append(re.search(f".*/{main_folder_name}(?=/)", Path(__file__).as_posix()).group(0))
# except AttributeError:
#     pass

# These two lines make it possible to use relative imports, when working in the autograde module
# import relative_import
# relative_import.enable_relative()

from .multiproccessing_extended import UnittestProcess
from . import subprocess_controller

class ProcessManager():
    def __init__(self, dir_, config):
        self.processes = []
        self.dir = dir_
        self.config = config
        self.init_test_configs()

    def init_test_configs(self):
        """Loads test config yaml file."""

        # Get relative path of assignment config folder
        config_folder = self.dir / "config"
        crt_folder = Path.cwd()
        config_folder = config_folder.relative_to(crt_folder)

        # Read and store assignment config
        with open(config_folder / "test_config.yaml") as config_file:
            self.test_config = safe_load(config_file)

    def start(self):
        # if exclude string exists add to regex otherwise leave it out
        if self.config["exclude_strings"]:
            incorrect_regex = f'(?<={self.config["filename_format"]})_?\\d*_?{self.config["student_n_format"]}((?!{self.config["exclude_strings"]}).)*$'
        else:
            incorrect_regex = f'(?<={self.config["filename_format"]})_?\\d*_?{self.config["student_n_format"]}.*$'

        # Go through all the student files.
        for file in self.dir.rglob("*.py"):
            file = file.resolve()  # create absolute file path

            # incorrect file format
            if not re.search(incorrect_regex, str(file), flags=re.IGNORECASE):
                continue

            # skip files not in the student folder
            elif not re.search(str(self.dir), str(file.as_posix()), flags=re.IGNORECASE):
                continue

            # skip files that are actually a notebook but disguised themselves as python files
            with open(file) as f:
                if f.read()[0] == "{":
                    continue

            self.start_process(file)

            # delay the start of the next process
            self.control_number_of_current_processes()

    def control_number_of_current_processes(self):
        # Manage the amount of processes
        open_processes = sum(1 for p in self.processes if p.is_alive())
        if open_processes > self.config["max_concurrent_process"]:
            time.sleep(0.05)  # Give the process some time to finish.
            for p in self.processes[:-self.config["max_concurrent_process"]]:  # Only terminate old processes
                self.terminate_process_after_n_seconds(p)

    def close_all(self):
        # close all processes, thus unittests
        for p in self.processes:
            # check if tests for a student is done
            self.terminate_process_after_n_seconds(p)

    def start_process(self, file):
        for file_num in range(self.test_config["n_files"]):
            # Start a new process for each students such that the unittest file can import a different student "module/script".
            p = UnittestProcess(name=str(file),
                                target=subprocess_controller.run_student_code,
                                kwargs={"dir_": self.dir, "file": file, "suite": self.test_config["files"][file_num]["name"], "n_unittests": self.test_config["files"][file_num]["n_tests"], "max_unittest_code_lines_4_report": self.config["max_unittest_code_lines_4_report"]},
                                config=self.config,
                                suite_config=self.test_config["files"][file_num])
            self.processes.append(p)
            p.start()
            if not self.config["run_parallel"]:
                self.terminate_process_after_n_seconds(p, self.test_config["files"][file_num]["max_runtime"])

    def terminate_process_after_n_seconds(self, p):
        # check if tests for a student is done
        if p.is_alive():
            # Give the test MAX_RUNTIME seconds to finish running
            p.join(p.suite_config["max_runtime"])

            # force the tests to stop running, if still running
            if p.is_alive():
                print(f"TERMINATE PROCESS {p}")  # Can be helpful to see which student codes have a timeout error
                p.terminate()
                p.join()  # make sure the process is terminate this can take a while but terminate itself is not blocking

            # release resources and remove from self.processes
            p.close()
            self.processes.remove(p)

def main():
    """
    The main flow of the autograder script.
    """
    global_config_path = next(Path(os.getcwd()).rglob("global_config.yaml"))
    global_config_path = global_config_path.resolve()
    with open(global_config_path) as config_file:
        config = safe_load(config_file)

    # Test if at least one folder matches the student_folder regex
    if len(list(Path(os.getcwd()).rglob(config["student_folder"]))) == 0:
        raise ValueError(f'{config["student_folder"]}, this directory/sub-path can not be found in the assignment folder!')

    # Search for exercise folder (in parent directory) giving in global config
    for dir_ in Path(os.getcwd()).rglob(config["student_folder"]):
        # check if it is a folder
        if not dir_.is_dir():
            continue

        dir_ = dir_.resolve()
        # check if it is a folder that contains a config.yaml
        try:
            process_manager = ProcessManager(dir_, config)
        except (NotADirectoryError, FileNotFoundError):
            continue

        process_manager.start()
        process_manager.close_all()

        # brightspace_grades = BrightspaceHandlerADS(dir_, BRIGHTSPACE_GRADE_FILE)
        # brightspace_grades.read_eligible(BRIGHTSPACE_ELIGIBLE_FILE)
        # process_manager.update_grades(brightspace_grades)

if __name__ == "__main__":
    main()
