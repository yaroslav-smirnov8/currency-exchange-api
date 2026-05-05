"""Test runner with green OK per test and 100 % summary."""

import ctypes
import os
import re
import subprocess
import sys


def _enable_ansi() -> None:
    """Enable ANSI escape sequences on Windows console."""
    if sys.platform != "win32":
        return
    kernel32 = ctypes.windll.kernel32
    mode = ctypes.c_ulong()
    for handle_id in (-11, -12):  # STD_OUTPUT_HANDLE, STD_ERROR_HANDLE
        handle = kernel32.GetStdHandle(handle_id)
        if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            kernel32.SetConsoleMode(handle, mode.value | 0x0004)


def main() -> None:
    _enable_ansi()
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short", "--no-header", "--color=no"],
        capture_output=True,
        text=True,
    )

    sys.stdout.write(result.stderr)

    passed = 0
    failed = 0

    for line in result.stdout.splitlines():
        m = re.match(r"^(.*?)\s+(PASSED|FAILED)\s+.*$", line)
        if m:
            name, status = m.group(1).strip(), m.group(2)
            if status == "PASSED":
                passed += 1
                print(f"\033[92m{name}  OK\033[0m")
            else:
                failed += 1
                print(f"\033[91m{name}  FAIL\033[0m")
        else:
            print(line)

    total = passed + failed
    print()
    if failed == 0 and total > 0:
        print(f"\033[1m\033[92mAll {total} tests passed — 100% OK\033[0m")
    elif total > 0:
        pct = passed * 100 // total
        print(f"\033[1m\033[91m{failed} test(s) failed! {passed}/{total} — {pct}%\033[0m")
    else:
        print("\033[91mNo tests collected.\033[0m")

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
