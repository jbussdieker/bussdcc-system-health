import platform
import shutil
import subprocess

from bussdcc import ContextProtocol, Process, Event, Message

from .. import message


class NotificationInterface(Process):
    name = "notification"

    def _notify(self, title: str, message: str) -> None:
        system = platform.system()

        try:
            if system == "Darwin":
                subprocess.run(
                    [
                        "osascript",
                        "-e",
                        f'display notification "{message}" with title "{title}"',
                    ],
                    check=False,
                )
                return

            if system == "Linux" and shutil.which("notify-send"):
                subprocess.run(["notify-send", title, message], check=False)
                return

            if system == "Windows":
                subprocess.run(
                    [
                        "powershell",
                        "-Command",
                        (
                            "Add-Type -AssemblyName PresentationFramework; "
                            f'[System.Windows.MessageBox]::Show("{message}", "{title}")'
                        ),
                    ],
                    check=False,
                )
                return

        except Exception:
            pass

        print(f"[{title}] {message}")

    def handle_event(self, ctx: ContextProtocol, evt: Event[Message]) -> None:
        payload = evt.payload

        if isinstance(payload, message.Notify):
            self._notify(payload.title, payload.message)
