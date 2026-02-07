import threading
import time


class WorkBreakTimer:
    """Background timer that cycles between work and break phases."""

    def __init__(self, work_minutes: int, break_minutes: int, on_tick, on_phase_end):
        self.work_seconds = max(1, work_minutes * 60)
        self.break_seconds = max(1, break_minutes * 60)
        self.on_tick = on_tick
        self.on_phase_end = on_phase_end

        self.current_mode = "work"
        self.remaining_seconds = self.work_seconds
        self._stop_event = threading.Event()
        self._thread = None
        self._lock = threading.Lock()
        self._running = False

    def start(self) -> None:
        with self._lock:
            if self._running:
                return
            self._running = True
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._run, daemon=True)
            self._thread.start()
        print(f"[LOG] Timer started in {self.current_mode} mode")

    def stop(self) -> None:
        with self._lock:
            if not self._running:
                return
            self._running = False
            self._stop_event.set()
        print("[LOG] Timer stopped")

    def reset(self) -> None:
        with self._lock:
            self.current_mode = "work"
            self.remaining_seconds = self.work_seconds
        print("[LOG] Timer reset")
        self.on_tick(self.current_mode, self.remaining_seconds)

    def set_mode(self, mode: str) -> None:
        with self._lock:
            self.current_mode = mode
            self.remaining_seconds = self.break_seconds if mode == "break" else self.work_seconds
        print(f"[LOG] Mode switched to {mode}")
        self.on_tick(self.current_mode, self.remaining_seconds)

    def skip_break(self) -> None:
        self.set_mode("work")

    def update_durations(self, work_minutes: int, break_minutes: int) -> None:
        with self._lock:
            self.work_seconds = max(1, work_minutes * 60)
            self.break_seconds = max(1, break_minutes * 60)
            if self.current_mode == "work":
                self.remaining_seconds = self.work_seconds
            else:
                self.remaining_seconds = self.break_seconds
        print("[LOG] Timer durations updated")
        self.on_tick(self.current_mode, self.remaining_seconds)

    def _run(self) -> None:
        while not self._stop_event.is_set():
            time.sleep(1)
            with self._lock:
                if not self._running:
                    continue
                self.remaining_seconds -= 1
                current_mode = self.current_mode
                remaining = self.remaining_seconds

            self.on_tick(current_mode, max(0, remaining))

            if remaining <= 0:
                print(f"[LOG] Timer finished for phase: {current_mode}")
                self.on_phase_end(current_mode)
                with self._lock:
                    if self.current_mode == "work":
                        self.current_mode = "break"
                        self.remaining_seconds = self.break_seconds
                    else:
                        self.current_mode = "work"
                        self.remaining_seconds = self.work_seconds
                self.on_tick(self.current_mode, self.remaining_seconds)
