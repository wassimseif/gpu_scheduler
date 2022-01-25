import threading
import subprocess

import os

from typing import List, Dict, Optional
from gpu_scheduler.utils import configure_logger

logger = configure_logger()


class GPUManager:
    """GPU manager, keeps track which GPUs used and which are avaiable."""

    def __init__(self, available_gpus: List[str], max_job_gpu: int):
        self.max_job_gpu = max_job_gpu

        self.available_gpus = list(available_gpus)
        self.available_gpus = [str(i) for i in self.available_gpus]
        self.job_per_gpu: Dict[str:int] = {}
        for i in self.available_gpus:
            self.job_per_gpu[i] = 0

    def get_any_available_gpu(self) -> Optional[str]:
        for id_, n_jobs in self.job_per_gpu.items():
            if n_jobs < self.max_job_gpu:
                return id_
        return None

    def get_gpu_allocations(self) -> Dict:
        return self.job_per_gpu

    def allocate_job(self, command: str, gpu: str) -> bool:
        self.run_command_with_gpu(command, gpu)
        self.job_per_gpu[gpu] += 1
        return True

    def run_command_with_gpu(self, command: str, gpu: str):

        myenv = os.environ.copy()
        myenv["CUDA_VISIBLE_DEVICES"] = str(gpu)

        def run_then_release_GPU(command, gpu):
            myenv = os.environ.copy()
            myenv["CUDA_VISIBLE_DEVICES"] = str(gpu)
            logger.info(f"Command {command} running on GPU {gpu}")
            proc = subprocess.Popen(args=command, shell=True, env=myenv)
            proc.wait()
            logger.info(f"Command {command} is done.")
            self.job_per_gpu[gpu] -= 1
            return

        thread = threading.Thread(target=run_then_release_GPU, args=(command, gpu))
        thread.start()
        # returns immediately after the thread starts
        return thread
