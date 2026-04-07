#!/usr/bin/env python3
"""Collect read-only Android device facts over adb and classify the SukiSU path."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


PROP_KEYS = [
    "ro.product.manufacturer",
    "ro.product.brand",
    "ro.product.model",
    "ro.product.device",
    "ro.build.version.release_or_codename",
    "ro.build.version.sdk",
    "ro.boot.slot_suffix",
    "ro.boot.vbmeta.device_state",
    "ro.boot.flash.locked",
    "ro.boot.verifiedbootstate",
    "ro.product.cpu.abi",
    "ro.product.cpu.abilist",
]


@dataclass
class AdbDevice:
    serial: str
    state: str
    details: str


def run(cmd: List[str]) -> str:
    proc = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        stderr = proc.stderr.strip()
        stdout = proc.stdout.strip()
        raise RuntimeError(stderr or stdout or f"command failed: {' '.join(cmd)}")
    return proc.stdout.strip()


def list_adb_devices() -> List[AdbDevice]:
    output = run(["adb", "devices", "-l"])
    devices: List[AdbDevice] = []
    for line in output.splitlines()[1:]:
        line = line.strip()
        if not line:
            continue
        parts = line.split(maxsplit=2)
        serial = parts[0]
        state = parts[1] if len(parts) > 1 else "unknown"
        details = parts[2] if len(parts) > 2 else ""
        devices.append(AdbDevice(serial=serial, state=state, details=details))
    return devices


def adb_cmd(serial: str, *args: str) -> str:
    return run(["adb", "-s", serial, *args])


def parse_kernel_version(kernel: str) -> Optional[Tuple[int, int]]:
    match = re.search(r"(\d+)\.(\d+)", kernel)
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


def parse_android_release(value: str) -> Optional[int]:
    match = re.search(r"\d+", value)
    if not match:
        return None
    return int(match.group(0))


def classify(data: Dict[str, object]) -> Dict[str, object]:
    manufacturer = str(data.get("manufacturer", "")).lower()
    brand = str(data.get("brand", "")).lower()
    model = str(data.get("model", "")).lower()
    kernel = str(data.get("kernel_release", ""))
    android_release = str(data.get("android_release", ""))
    bootloader_locked = str(data.get("flash_locked", "")) in {"1", "true"}
    kernel_version = parse_kernel_version(kernel)
    android_major = parse_android_release(android_release)

    haystack = " ".join([manufacturer, brand, model])
    reasons: List[str] = []
    notes: List[str] = []

    if bootloader_locked:
        return {
            "route": "blocked-bootloader",
            "bucket": "blocked",
            "reasons": ["bootloader appears locked"],
            "notes": ["do not recommend flashing steps until the bootloader issue is resolved"],
        }

    if any(name in haystack for name in ("oneplus", "oppo", "realme")):
        reasons.append("vendor belongs to the OnePlus/OPPO/realme family that upstream routes away from generic GKI")
        return {
            "route": "oneplus-special-workflow",
            "bucket": "special-workflow",
            "reasons": reasons,
            "notes": ["prefer the dedicated OnePlus workflow repo when the model has an explicit entry"],
        }

    if "meizu" in haystack:
        reasons.append("Meizu is called out upstream as needing manual kernel modification/compilation")
        return {
            "route": "source-integration-required",
            "bucket": "manual-integration",
            "reasons": reasons,
            "notes": ["use the core SukiSU-Ultra integration docs rather than generic GKI assumptions"],
        }

    if kernel_version and android_major and kernel_version >= (5, 10) and android_major >= 12:
        reasons.append("device matches the documented Android 12+ and kernel 5.10+ GKI/LKM range")
        if "pixel" in haystack:
            notes.append("Pixel-family devices should prefer the less-patched GKI build according to the upstream Japanese README")
        return {
            "route": "generic-gki-candidate",
            "bucket": "documented-range",
            "reasons": reasons,
            "notes": notes,
        }

    reasons.append("device falls outside the documented generic GKI range or lacks clear upstream evidence")
    return {
        "route": "source-integration-required",
        "bucket": "manual-integration",
        "reasons": reasons,
        "notes": ["expect kernel-source work instead of a generic prebuilt flow"],
    }


def collect(serial: Optional[str]) -> Dict[str, object]:
    if shutil.which("adb") is None:
        raise RuntimeError("adb not found in PATH")

    devices = [device for device in list_adb_devices() if device.state == "device"]
    if not devices:
        raise RuntimeError("no adb device in 'device' state is connected")

    if serial is None:
        if len(devices) != 1:
            serials = ", ".join(device.serial for device in devices)
            raise RuntimeError(f"multiple devices connected, use --serial: {serials}")
        serial = devices[0].serial

    prop_values: Dict[str, str] = {}
    for key in PROP_KEYS:
        prop_values[key] = adb_cmd(serial, "shell", "getprop", key)

    result: Dict[str, object] = {
        "serial": serial,
        "manufacturer": prop_values["ro.product.manufacturer"],
        "brand": prop_values["ro.product.brand"],
        "model": prop_values["ro.product.model"],
        "device_codename": prop_values["ro.product.device"],
        "android_release": prop_values["ro.build.version.release_or_codename"],
        "sdk_int": prop_values["ro.build.version.sdk"],
        "slot_suffix": prop_values["ro.boot.slot_suffix"],
        "vbmeta_device_state": prop_values["ro.boot.vbmeta.device_state"],
        "flash_locked": prop_values["ro.boot.flash.locked"],
        "verified_boot_state": prop_values["ro.boot.verifiedbootstate"],
        "primary_abi": prop_values["ro.product.cpu.abi"],
        "abi_list": prop_values["ro.product.cpu.abilist"],
        "kernel_release": adb_cmd(serial, "shell", "uname", "-r"),
    }
    result["classification"] = classify(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Collect read-only adb device facts and classify the SukiSU root path."
    )
    parser.add_argument("--serial", help="adb serial to inspect")
    parser.add_argument(
        "--json",
        action="store_true",
        help="print JSON output (default when no other format is requested)",
    )
    args = parser.parse_args()

    try:
        payload = collect(args.serial)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
