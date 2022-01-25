# Python stdlib
from copy import copy
import threading
import time
from typing import Dict
import argparse

# Project Dependencies
from flask import Flask, request, jsonify
import schedule

# Project Imports
from gpu_scheduler.models.command import Command
from gpu_scheduler.models.commandqueue import CommandQueue
from gpu_scheduler.utils import configure_logger
from gpu_scheduler.scheduler.gpu_manager import GPUManager

logger = configure_logger()
app = Flask(__name__)
queue = None
gpu_manager = None


def mk_error_object(msg: str) -> Dict:
    return {"status": "error", "msg": msg}


def run_continuously(interval=1):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


def check_job_allocations():
    logger.info(gpu_manager.get_gpu_allocations())
    if queue.is_empty():
        logger.info(f"No Jobs to run")
        return
    logger.info(f"{queue.size()} Jobs to queue")
    if not (gpu := gpu_manager.get_any_available_gpu()):
        logger.info(f"No GPUs available now")
        return
    command_to_run = queue.front()
    gpu_manager.allocate_job(command_to_run.command, gpu)
    queue.dequeue()


schedule.every(5).seconds.do(check_job_allocations)
stop_run_continuously = run_continuously()


@app.get("/")
def root():
    return {"status": "Up"}


@app.post("/commands")
def add_command():
    params = ["command"]
    for p in params:
        if p not in request.form:
            return jsonify(mk_error_object(f"Missing parameter {p}"))

    com = request.form["command"]

    obj = Command(com)

    bs = queue.size()

    queue.enqueue(obj)
    logger.info(
        f"Added Command {str(obj)} - Before size {bs} - After size "
        f"{queue.size()} "
    )
    return obj.to_json()


@app.get("/commands/")
def get_all_commands():
    logger.info(queue.size())
    tq = copy(queue)
    resp = []
    index = 0
    while not tq.is_empty():
        a = tq.dequeue().to_json()
        a["index"] = index
        resp.append(a)
        index += 1
    return jsonify(resp)


@app.delete("/commands")
def delete_command():
    params = ["uid"]
    for p in params:
        if p not in request.form:
            return jsonify(mk_error_object(f"Missing parameter {p}"), 400)

    uid = request.form["uid"]
    logger.info(f"Should Remove Command with uid {uid}")
    if queue.remove_elm_uid(uid):
        return {"success": True}
    return jsonify(mk_error_object(f"Element could not be found "), 400)


if __name__ == "__main__":
    """Read command line arguments and start reading from stdin."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--gpus", nargs="+", type=str, required=True)
    parser.add_argument("--jobs_per_gpu", type=int, required=True)
    args = parser.parse_args()
    # Support both comma separated and individually passed GPU ids
    gpus = args.gpus if len(args.gpus) > 1 else args.gpus[0].split(",")
    gpu_manager = GPUManager(gpus, args.jobs_per_gpu)
    queue = CommandQueue()

    app.run(port=8000)
