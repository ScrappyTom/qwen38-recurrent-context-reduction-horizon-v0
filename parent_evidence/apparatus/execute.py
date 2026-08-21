from __future__ import annotations

import argparse
import json
import re
import shutil
import socket
import subprocess
import time
from pathlib import Path
from typing import Any

from apparatus.canonical import write_json
from apparatus.constants import MAXIMUM_MEASURED_CALLS, ROOT
from apparatus.runner import (
    get_json,
    require_authorization,
    require_clean_head,
    run_experiment,
    verify_endpoint,
    verify_runtime_files,
)


def gpu_state() -> dict[str, Any]:
    process = subprocess.run(
        [
            "nvidia-smi",
            "--query-gpu=index,name,memory.used,memory.free,memory.total,utilization.gpu",
            "--format=csv,noheader,nounits",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        text=True,
    )
    return {
        "returncode": process.returncode,
        "stdout": process.stdout.strip(),
        "stderr": process.stderr.strip(),
    }


def llama_processes() -> list[str]:
    process = subprocess.run(
        ["tasklist", "/FI", "IMAGENAME eq llama-server.exe", "/FO", "CSV", "/NH"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        text=True,
    )
    rows = [line.strip() for line in process.stdout.splitlines() if line.strip()]
    return [line for line in rows if "llama-server.exe" in line.lower()]


def port_open(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.25)
        return sock.connect_ex((host, port)) == 0


def wait_ready(base_url: str, process: subprocess.Popen[bytes], timeout_seconds: int = 300) -> None:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"llama-server exited during startup with code {process.returncode}")
        try:
            if get_json(base_url, "/health").get("status") == "ok":
                return
        except Exception:
            pass
        time.sleep(1)
    raise RuntimeError("llama-server did not become healthy before the startup deadline")


def server_arguments(server: Path, model: Path, host: str, port: int, runtime: Path) -> list[str]:
    slots = runtime / "slots"
    slots.mkdir(parents=True, exist_ok=True)
    return [
        str(server),
        "-m", str(model),
        "--alias", "qwen38-ad25q8-world-join",
        "--host", host,
        "--port", str(port),
        "--gpu-layers", "all",
        "--fit", "off",
        "-c", "25000",
        "--flash-attn", "on",
        "-ctk", "q8_0",
        "-ctv", "q8_0",
        "--kv-unified",
        "-b", "512",
        "-ub", "256",
        "--threads", "7",
        "--threads-batch", "8",
        "--parallel", "1",
        "--cache-prompt",
        "--cache-ram", "0",
        "--slot-save-path", str(slots),
        "--no-context-shift",
        "--jinja",
        "--reasoning", "off",
        "--reasoning-format", "deepseek",
        "--reasoning-budget", "0",
        "--no-reasoning-preserve",
        "--temp", "0.7",
        "--top-p", "0.8",
        "--top-k", "20",
        "--min-p", "0.0",
        "--presence-penalty", "1.5",
        "--repeat-penalty", "1.0",
        "--metrics",
        "--slots",
        "--no-webui",
        "--no-mmproj",
        "--verbose",
        "--log-file", str(runtime / "llama-server.log"),
    ]


def execute(*, run_id: str, server: Path, model: Path, host: str, port: int) -> dict[str, Any]:
    require_authorization()
    head = require_clean_head()
    verify_runtime_files(server.resolve(), model.resolve())
    existing = llama_processes()
    if existing:
        raise RuntimeError(f"llama-server isolation check failed; existing processes: {existing}")
    if port_open(host, port):
        raise RuntimeError(f"intended port is already open: {host}:{port}")

    runtime = ROOT / ".cache" / "runtime" / run_id
    if runtime.exists():
        raise RuntimeError(f"runtime staging path already exists: {runtime}")
    runtime.mkdir(parents=True)
    arguments = server_arguments(server.resolve(), model.resolve(), host, port, runtime)
    write_json(runtime / "server-arguments.json", arguments)
    lifecycle: dict[str, Any] = {
        "schema_version": "recurrent-context-reduction-runtime-lifecycle-v0",
        "run_id": run_id,
        "standalone_commit": head,
        "started_at_unix": time.time(),
        "server_arguments": arguments,
        "gpu_before": gpu_state(),
        "existing_llama_processes_before": existing,
        "port_open_before": False,
        "passed": False,
    }
    process: subprocess.Popen[bytes] | None = None
    try:
        with (runtime / "stdout.log").open("wb") as stdout, (runtime / "stderr.log").open("wb") as stderr:
            process = subprocess.Popen(
                arguments,
                stdout=stdout,
                stderr=stderr,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            lifecycle["server_pid"] = process.pid
            base_url = f"http://{host}:{port}"
            wait_ready(base_url, process)
            lifecycle["gpu_after_load"] = gpu_state()
            startup_log = (runtime / "llama-server.log").read_text(encoding="utf-8", errors="replace")
            startup_offloads = [
                (int(used), int(total))
                for used, total in re.findall(r"offloaded\s+(\d+)/(\d+)\s+layers to GPU", startup_log)
            ]
            startup_main = next(
                ((used, total) for used, total in reversed(startup_offloads) if total == 66),
                None,
            )
            lifecycle["main_offloaded_layers_before_calls"] = list(startup_main) if startup_main else None
            if startup_main != (66, 66):
                raise RuntimeError(
                    "the exact CUDA profile did not offload 66/66 main-model layers; no measured call was made"
                )
            props = verify_endpoint(base_url, model.resolve())
            runtime_custody = {
                "schema_version": "recurrent-context-reduction-runtime-custody-v0",
                "server_and_model": verify_runtime_files(server.resolve(), model.resolve()),
                "server_arguments": arguments,
                "endpoint_props": props,
                "gpu_after_load": lifecycle["gpu_after_load"],
                "main_offloaded_layers_before_calls": lifecycle["main_offloaded_layers_before_calls"],
                "model_calls_before_custody": 0,
            }
            result = run_experiment(run_id=run_id, base_url=base_url, runtime_custody=runtime_custody)
            lifecycle["run_result"] = result
            log = (runtime / "llama-server.log").read_text(encoding="utf-8", errors="replace")
            offloads = [(int(used), int(total)) for used, total in re.findall(r"offloaded\s+(\d+)/(\d+)\s+layers to GPU", log)]
            main = next(((used, total) for used, total in reversed(offloads) if total == 66), None)
            lifecycle["main_offloaded_layers"] = list(main) if main else None
            lifecycle["passed"] = main == (66, 66) and result["model_calls"] <= MAXIMUM_MEASURED_CALLS
    except Exception as exc:
        lifecycle["error"] = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        if process is not None and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=30)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=30)
        deadline = time.monotonic() + 30
        while port_open(host, port) and time.monotonic() < deadline:
            time.sleep(0.5)
        lifecycle["port_open_after"] = port_open(host, port)
        lifecycle["llama_processes_after"] = llama_processes()
        lifecycle["gpu_after_stop"] = gpu_state()
        lifecycle["finished_at_unix"] = time.time()
        write_json(runtime / "runtime-lifecycle.json", lifecycle)
        run_model = ROOT / "runs" / run_id / "model"
        if run_model.parent.exists():
            write_json(run_model / "runtime-lifecycle.json", lifecycle)
            write_json(run_model / "server-arguments.json", arguments)
            logs = run_model / "logs"
            logs.mkdir(parents=True, exist_ok=True)
            for name in ("llama-server.log", "stdout.log", "stderr.log"):
                source = runtime / name
                if source.is_file():
                    shutil.copy2(source, logs / name)
    return lifecycle


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--server-executable", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    result = execute(
        run_id=args.run_id,
        server=args.server_executable,
        model=args.model,
        host=args.host,
        port=args.port,
    )
    print(json.dumps(result, sort_keys=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
