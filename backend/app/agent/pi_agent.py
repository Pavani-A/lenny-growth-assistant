import json
import os
import subprocess
from collections.abc import Iterator


class PiAgent:
    """Bridge between the Python backend and Pi Coding Agent."""

    def __init__(
        self,
        provider: str = "ollama",
        model: str = "llama3.2:3b",
    ):
        self.provider = provider
        self.model = model
        self.pi_path = os.getenv(
            "PI_EXECUTABLE",
            r"C:\Users\dell\AppData\Roaming\npm\pi.cmd",
        )

    def _start_process(self) -> subprocess.Popen:
        """Start Pi in RPC mode."""

        return subprocess.Popen(
            [
                self.pi_path,
                "--mode",
                "rpc",
                "--provider",
                self.provider,
                "--model",
                self.model,
                "--no-session",
                "--no-tools",
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

    def _send_prompt(self, process: subprocess.Popen, prompt: str) -> None:
        """Send a prompt to Pi's RPC process."""

        command = {
            "id": "lenny-request",
            "type": "prompt",
            "message": prompt,
        }

        process.stdin.write(json.dumps(command) + "\n")
        process.stdin.flush()

    def generate(self, prompt: str) -> str:
        """Generate a complete response through Pi."""

        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        process = self._start_process()

        try:
            self._send_prompt(process, prompt)

            response_parts: list[str] = []

            while True:
                line = process.stdout.readline()

                if not line:
                    break

                event = json.loads(line)

                if event.get("type") != "message_update":
                    if event.get("type") == "agent_end":
                        break
                    continue

                assistant_event = event.get("assistantMessageEvent", {})

                if assistant_event.get("type") == "text_delta":
                    delta = assistant_event.get("delta", "")
                    if delta:
                        response_parts.append(delta)

            response = "".join(response_parts).strip()

            if not response:
                raise RuntimeError("Pi returned an empty response.")

            return response

        finally:
            process.kill()

    def generate_stream(self, prompt: str) -> Iterator[str]:
        """Stream response text through Pi."""

        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        process = self._start_process()

        try:
            self._send_prompt(process, prompt)

            while True:
                line = process.stdout.readline()

                if not line:
                    break

                event = json.loads(line)

                if event.get("type") == "agent_end":
                    break

                if event.get("type") != "message_update":
                    continue

                assistant_event = event.get("assistantMessageEvent", {})

                if assistant_event.get("type") == "text_delta":
                    delta = assistant_event.get("delta", "")

                    if delta:
                        yield delta

        finally:
            process.kill()