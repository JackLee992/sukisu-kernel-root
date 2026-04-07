# Bootloader Unlock Reference

This reference is intentionally conservative. It explains only what is supported by current official or primary-source evidence.

## Core Rule

Do not equate these statements:
- "This device family is in SukiSU's documented compatibility range"
- "This device can be officially bootloader-unlocked"

Those are different questions.

## Official Android / Pixel-Style Fastboot Unlock

Primary source:
- <https://source.android.com/docs/core/architecture/bootloader/locking_unlocking>
- <https://developers.google.com/android/images>

What the Android official docs say:
- The user must first enable `OEM unlocking` in `Settings > System > Developer options` if `get_unlock_ability` is still `0`.
- To issue fastboot commands, the device must be in bootloader mode. One documented way is:

```bash
adb reboot bootloader
```

- Once in bootloader mode, the documented unlock command is:

```bash
fastboot flashing unlock
```

- After the command is sent, the device should show a warning that requires physical user acknowledgment.
- After acknowledgment, the device should perform a factory data reset.

How to phrase this in answers:
- "For devices that support standard Android flashing unlock, the official flow is OEM unlocking -> bootloader mode -> `fastboot flashing unlock` -> on-device confirmation -> data wipe."

## Google Pixel

Primary source:
- <https://developers.google.com/android/images>
- <https://source.android.com/docs/core/architecture/bootloader/locking_unlocking>

What can be stated safely:
- Pixel devices use the standard Android flashing/unlock model documented by Google and AOSP.
- Unlocking the bootloader is part of the factory image flashing workflow and reduces device security.
- The device must still support OEM unlocking and requires physical confirmation.

What not to overclaim:
- Do not claim every Pixel variant or carrier SKU is unlockable without checking OEM unlocking availability on the device.

## Xiaomi / Redmi

Primary source:
- <https://www.miui.com/unlock/>
- <https://www.miui.com/unlock/done.html>
- <https://in.miui.com/unlock/download_en.html>

What Xiaomi's official unlock pages say:
- Unlocking is done with the official `Mi Unlock` tool on a PC, not just a bare fastboot command.
- The phone is put into bootloader/Fastboot mode manually, typically with `Power + Volume Down`.
- The device is then connected to the PC and unlocked through the official tool.

How to phrase this in answers:
- "For Xiaomi/Redmi, use the official Mi Unlock flow rather than assuming a direct `fastboot flashing unlock` path."

## Samsung

Primary source:
- <https://developer.samsung.com/faq>

What Samsung's developer FAQ says:
- Samsung Developer support says they do not have information about unlocking devices and directs users to Samsung Customer Support.

How to phrase this in answers:
- "Samsung appears in SukiSU's GKI-friendly family examples, but I do not have a Samsung official universal bootloader-unlock flow from current primary sources."
- "Treat Samsung bootloader unlock as region/model specific unless the exact model has separate official evidence."

## OnePlus

Current primary-source status:
- This skill has strong primary-source evidence for OnePlus SukiSU build workflows.
- This skill does not currently bundle a OnePlus official universal bootloader-unlock guide from a current primary source.

How to phrase this in answers:
- "OnePlus has strong SukiSU workflow coverage here, but I have not yet confirmed a current official OnePlus universal bootloader-unlock document in this skill's source set."
- "Check the exact model and OEM unlocking availability before presenting an unlock procedure as official."

## Fast Device Checks

These checks are safe and read-only:

```bash
adb shell getprop ro.boot.vbmeta.device_state
adb shell getprop ro.boot.flash.locked
adb shell getprop ro.boot.verifiedbootstate
```

Typical interpretation:
- `ro.boot.flash.locked=0` usually means already unlocked
- `ro.boot.vbmeta.device_state=unlocked` supports the same conclusion
- `ro.boot.verifiedbootstate=orange` often appears on unlocked devices

These values help identify current state. They do not replace vendor policy or official unlock eligibility.

## What To Say When Evidence Is Missing

Use wording like:
- "I can describe the standard Android unlock flow, but I have not confirmed an official vendor-specific unlock path for this exact family."
- "This device may be in SukiSU's supported range, but bootloader unlock support still depends on OEM policy."
- "I would treat this as not confirmed from official sources until we check the exact model."
