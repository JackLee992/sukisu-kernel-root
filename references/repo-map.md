# SukiSU Repo Map

This reference summarizes the repos that matter when using the SukiSU-Ultra stack for kernel-root work.

## 1. Core Repo: SukiSU-Ultra

Repo:
- <https://github.com/SukiSU-Ultra/SukiSU-Ultra>

Use this repo for:
- the core root implementation
- integration docs
- `kernel/setup.sh` for adding SukiSU to a kernel source tree
- `repack_apk.py` for repacking the manager APK with rebuilt `ksud`
- manager and LKM build workflows

Important upstream entry points:
- `docs/guide/installation.md`
- `docs/guide/how-to-integrate.md`
- `docs/guide/tracepoint-hook.md`
- `kernel/setup.sh`
- `.github/workflows/build-lkm.yml`
- `.github/workflows/build-manager.yml`

Key commands from upstream docs:

```sh
curl -LSs "https://raw.githubusercontent.com/SukiSU-Ultra/SukiSU-Ultra/main/kernel/setup.sh" | bash -s main
curl -LSs "https://raw.githubusercontent.com/SukiSU-Ultra/SukiSU-Ultra/main/kernel/setup.sh" | bash -s builtin
curl -LSs "https://raw.githubusercontent.com/SukiSU-Ultra/SukiSU-Ultra/main/kernel/setup.sh" | bash -s susfs-main
```

Use this repo when:
- the user has kernel source
- the device is non-GKI or vendor-modified
- the helper repos do not cover the model
- the user wants to build or repack the manager APK

## 2. Generic GKI Helper Repo: GKI_KernelSU_SUSFS

Repo:
- <https://github.com/ShirkNeko/GKI_KernelSU_SUSFS>

Use this repo for:
- broader-patch GKI builds
- downloadable AnyKernel3 or boot image artifacts
- GitHub Actions workflows keyed by Android version and kernel version

Documented workflow/build coverage in the repo:
- Android 12 / kernel 5.10
- Android 13 / kernel 5.10
- Android 13 / kernel 5.15
- Android 14 / kernel 5.15
- Android 14 / kernel 6.1
- Android 15 / kernel 6.6

Notes from upstream README:
- download artifacts from releases
- AnyKernel3 zips are intended for direct flashing
- boot images must match the device compression format

## 3. Lighter GKI Helper Repo: GKI_SukiSU_SUSFS

Repo:
- <https://github.com/MiRinFork/GKI_SukiSU_SUSFS>

Use this repo for:
- lighter GKI builds
- Pixel-friendly recommendations
- workflow-driven builds up to Android 16 / kernel 6.12 in the current repo

Notable upstream evidence:
- README says it applies to GKI-compatible phones
- README includes explicit boot evidence for Pixel 8
- SukiSU-Ultra's Japanese README tells Pixel users to prefer the less-patched GKI build

Current workflow files show build coverage for:
- Android 12 / kernel 5.10
- Android 13 / kernel 5.10
- Android 13 / kernel 5.15
- Android 14 / kernel 5.15
- Android 14 / kernel 6.1
- Android 15 / kernel 6.6
- Android 16 / kernel 6.12

## 4. OnePlus Workflow Repo: Action_OnePlus_MKSU_SUSFS

Repo:
- <https://github.com/ShirkNeko/Action_OnePlus_MKSU_SUSFS>

Use this repo for:
- OnePlus models that have explicit workflow config entries
- GitHub Action based builds using OnePlus OSS manifests

The current workflow takes explicit inputs for:
- CPU branch
- config XML name
- processor codename
- Android version
- kernel version
- build method
- SUSFS, VFS, KPM, ZRAM toggles

Use this repo instead of the generic GKI route when the device is OnePlus and has a matching workflow entry.
