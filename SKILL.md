---
name: sukisu-kernel-root
description: Use when the user wants to use SukiSU-Ultra and its companion GKI or OnePlus build repos to plan or automate Android kernel root, inspect a connected device over adb, classify it into generic GKI vs OnePlus workflow vs source integration, or list only the clearly supported models and kernel ranges backed by upstream repo evidence.
---

# SukiSU Kernel Root

Plan SukiSU-Ultra based kernel-root work without guessing. This skill is evidence-first: it distinguishes explicitly named devices, clearly documented compatibility ranges, special-case vendor workflows, and devices that still require source integration.

## Installation Path

This skill assumes the default Codex skill location:

```bash
$HOME/.codex/skills/sukisu-kernel-root
```

## Safety Rules

- Default to read-only discovery first.
- Do not flash partitions, patch boot images, reboot to bootloader, switch slots, or edit kernel sources unless the user explicitly asks.
- Do not call a device "supported" unless that claim is backed by the current upstream documents or workflow files in `references/supported-devices.md`.
- Separate these buckets in every answer: `explicitly named`, `clearly in supported range`, `special workflow required`, `manual/source integration required`, `not confirmed`.
- If the connected device falls outside the documented evidence, say that plainly and stop short of claiming compatibility.

## Quick Start

1. Read the support evidence before making recommendations:

```text
$HOME/.codex/skills/sukisu-kernel-root/references/supported-devices.md
```

2. Read the upstream repo map when the user asks how to use this stack:

```text
$HOME/.codex/skills/sukisu-kernel-root/references/repo-map.md
```

3. If a phone is connected, collect facts first:

```bash
python3 "$HOME/.codex/skills/sukisu-kernel-root/scripts/collect_device_info.py" --json
```

4. Classify the route:
- `generic-gki-candidate`: Android 12+ and kernel 5.10+, not in the vendor exception list
- `oneplus-special-workflow`: OnePlus and other OPPO-family entries handled by the dedicated workflow
- `source-integration-required`: non-GKI or vendor-modified kernels that need manual integration
- `blocked-bootloader`: bootloader state prevents flashing work

5. Produce a structured answer with:
- device snapshot
- evidence-backed support bucket
- selected repo and workflow
- exact inputs still needed
- commands or automation steps
- risks and stop points

## Workflow Decision Tree

### Route A: Generic GKI Candidate

Use this route when the device is in the explicit GKI-friendly range documented by upstream: Android 12+, kernel 5.10+, and not called out as a vendor exception. This is the best fit for many Xiaomi, Redmi, Samsung, and likely Pixel-family devices, but only the categories and notes in `references/supported-devices.md` may be stated as explicit support.

Actions:
- Match the device kernel line to the available build matrix in the GKI helper repos.
- Prefer the lighter GKI path for Pixel devices because the upstream Japanese README explicitly tells Pixel users to use the less-patched GKI build.
- When the user wants prebuilt artifacts or GitHub Actions automation, start from the helper repos in `references/repo-map.md`.
- Only move from planning to flashing when the user explicitly asks.

### Route B: OnePlus Special Workflow

Use this route for OnePlus devices with explicit workflow entries in the dedicated GitHub Action repo. Treat those workflow inputs as explicit automation coverage, not as a blanket guarantee that every firmware build will boot.

Actions:
- Read `references/supported-devices.md` for the explicit OnePlus model list and the exact workflow source.
- Ask for or detect the needed inputs: Android version, kernel version, SoC family, and the matching OnePlus kernel manifest/config entry.
- Drive the user toward the OnePlus workflow repo rather than the generic GKI route.
- If the model is OnePlus-branded but not listed in the workflow options, downgrade to `source-integration-required`.

### Route C: Source Integration Required

Use this route for non-GKI, older kernels, or vendor-modified kernels explicitly called out by upstream docs, such as Meizu and many OPPO or realme builds.

Actions:
- Start from the core SukiSU-Ultra repo and its integration docs in `references/repo-map.md`.
- Use `kernel/setup.sh` for the initial source-tree insertion step.
- Choose `main`, `builtin`, or `susfs-*` based on the kernel path the user is targeting.
- If the kernel source is old or heavily customized, rely on the manual integration and tracepoint docs rather than promising a one-command flow.

### Route D: Blocked Bootloader

If bootloader state is locked or verified boot state blocks flashing, stop at preparation. Provide the device snapshot and explain that no kernel-root path is safe until the bootloader problem is resolved.

## Repository Roles

When the user asks "how do we use this repo," map the repos like this:

- `SukiSU-Ultra`: core root implementation, manual integration docs, `kernel/setup.sh`, manager build logic, `repack_apk.py`
- `GKI_KernelSU_SUSFS`: prebuilt and workflow-driven GKI kernels with broader patch set
- `GKI_SukiSU_SUSFS`: lighter GKI path; upstream notes mention Pixel 8 boot evidence and recommend it for Pixel-family users
- `Action_OnePlus_MKSU_SUSFS`: workflow-driven OnePlus kernel builds with explicit model/config inputs

See:

```text
$HOME/.codex/skills/sukisu-kernel-root/references/repo-map.md
```

## Output Format

Use this structure when answering:

```markdown
## Device Snapshot
- Model:
- Android:
- Kernel:
- Bootloader state:

## Support Classification
- Bucket:
- Why:
- Source:

## Recommended Path
- Repo:
- Build or install route:
- Inputs still needed:

## Safety Notes
- Blocking risks:
- Actions I will not take without approval:
```

## When Listing Supported Devices

Always separate:
- explicitly named device models
- explicitly named vendor families
- kernel or Android ranges that are clearly documented
- exceptions that upstream says should not use the generic GKI path

Never turn "Pixel users should use the less-patched GKI build" into "all Pixel models are explicitly supported." That is an inference and must be labeled as such.
