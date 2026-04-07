# SukiSU Kernel Root

A Codex skill for planning and preparing `SukiSU-Ultra` based Android kernel root work without guessing.

This repo packages a reusable skill that:

- inspects a connected Android device over `adb`
- classifies it into `generic GKI`, `OnePlus special workflow`, `manual source integration`, or `blocked bootloader`
- maps the correct upstream repo for the job
- separates explicit support claims from inference
- ships a support matrix document backed by current upstream repo evidence

## Status

The skill and docs are prepared and statically checked.

- `SKILL.md` passes the bundled skill validator
- `scripts/collect_device_info.py` passes Python syntax compilation
- no live flashing, rooting, or end-to-end device validation is included in this repository state

## Files

- `SKILL.md`: the Codex skill instructions
- `agents/openai.yaml`: UI metadata for the skill
- `scripts/collect_device_info.py`: read-only `adb` probe and route classifier
- `references/repo-map.md`: how the upstream SukiSU helper repos fit together
- `references/supported-devices.md`: explicit model and range coverage, with sources
- `references/unlock-bootloader.md`: conservative, source-backed bootloader unlock guidance

## What The Skill Covers

### Route selection

The skill chooses among:

- `generic-gki-candidate`
- `oneplus-special-workflow`
- `source-integration-required`
- `blocked-bootloader`

### Upstream repos

It understands the roles of:

- `SukiSU-Ultra`
- `GKI_KernelSU_SUSFS`
- `GKI_SukiSU_SUSFS`
- `Action_OnePlus_MKSU_SUSFS`

### Evidence-first support claims

The skill does not treat community assumptions as support.

It keeps these categories separate:

- explicitly named models
- clearly documented compatibility ranges
- families that require a dedicated workflow
- devices that still need source integration
- devices that may be SukiSU-compatible but do not have a clearly confirmed official bootloader-unlock path

## Supported Devices Summary

Short version:

- Explicit model coverage currently comes mainly from the OnePlus workflow repo and the `Pixel 8` note in `GKI_SukiSU_SUSFS`.
- Explicit GKI-friendly family examples in upstream docs include `Xiaomi`, `Redmi`, and `Samsung`.
- Pixel users are explicitly advised upstream to prefer the less-patched GKI build, but that is not the same as a full Pixel model whitelist.
- `OPPO`, `OnePlus`, `realme`, and `Meizu` are explicitly called out upstream as cases where the generic GKI path may not be enough.

For the full, source-backed list, read:

- [`references/supported-devices.md`](./references/supported-devices.md)
- [`references/unlock-bootloader.md`](./references/unlock-bootloader.md)

## Install

Clone or copy this repo into your Codex skills directory:

```bash
mkdir -p "$HOME/.codex/skills"
git clone https://github.com/JackLee992/sukisu-kernel-root.git "$HOME/.codex/skills/sukisu-kernel-root"
```

If you already keep the repo elsewhere, you can also symlink it into the same directory.

## Usage

Example prompts:

```text
Use $sukisu-kernel-root to inspect my connected Android phone and choose the safest SukiSU-Ultra path.
```

```text
Use $sukisu-kernel-root to list only the explicitly supported OnePlus models from the current workflow repo.
```

```text
Use $sukisu-kernel-root to explain whether this device should use generic GKI, the OnePlus workflow, or source integration.
```

## Local Checks

The following non-invasive checks were used while preparing this repo:

```bash
python3 -m py_compile scripts/collect_device_info.py
python3 /Users/liyilin02/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

## Notes

- This repo is intentionally conservative about support claims.
- It is designed to help plan and automate the workflow selection stage first.
- Flashing, patching, or modifying a device should happen only after explicit user approval.
