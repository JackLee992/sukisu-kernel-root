# SukiSU Supported Devices and Ranges

This document lists only support claims that are explicit in the current upstream repo docs or workflow files. It does not treat community guesses as support.

## Reading This Document

Buckets used here:
- `Explicit model`: a specific device model appears in a workflow or README.
- `Explicit family/range`: upstream docs name a vendor family or compatibility range, but not every exact model.
- `Special workflow`: upstream points the family to a dedicated repo instead of the generic GKI path.
- `Manual integration`: upstream explicitly says the generic GKI route is not enough and kernel-source integration is needed.

## 1. Explicit Model Coverage

### OnePlus models with explicit workflow entries

Source:
- `Action_OnePlus_MKSU_SUSFS/.github/workflows/Build-SukiSU.yml`
- <https://github.com/ShirkNeko/Action_OnePlus_MKSU_SUSFS/blob/main/.github/workflows/Build-SukiSU.yml>

These model/config names appear directly in the workflow options:

| Human name | Workflow config token | Bucket |
| --- | --- | --- |
| OnePlus Nord CE4 | `oneplus_nord_ce4_v` | Explicit model |
| OnePlus Ace 3V | `oneplus_ace_3v_v` | Explicit model |
| OnePlus Nord 4 | `oneplus_nord_4_v` | Explicit model |
| OnePlus 10 Pro | `oneplus_10_pro_v` | Explicit model |
| OnePlus 10T | `oneplus_10t_v` | Explicit model |
| OnePlus 11R | `oneplus_11r_v` | Explicit model |
| OnePlus Ace 2 | `oneplus_ace2_v` | Explicit model |
| OnePlus Ace Pro | `oneplus_ace_pro_v` | Explicit model |
| OnePlus 11 | `oneplus_11_v` | Explicit model |
| OnePlus 12R | `oneplus_12r_v` | Explicit model |
| OnePlus Ace 2 Pro | `oneplus_ace2_pro_v` | Explicit model |
| OnePlus Ace 3 | `oneplus_ace3_v` | Explicit model |
| OnePlus Open | `oneplus_open_v` | Explicit model |
| OnePlus 12 | `oneplus12_v` | Explicit model |
| OnePlus 13R | `oneplus_13r` | Explicit model |
| OnePlus Ace 3 Pro | `oneplus_ace3_pro_v` | Explicit model |
| OnePlus Ace 5 | `oneplus_ace5` | Explicit model |
| OnePlus Pad 2 | `oneplus_pad2_v` | Explicit model |
| OnePlus 13 | `oneplus_13` | Explicit model |
| OnePlus 13T | `oneplus_13t` | Explicit model |
| OnePlus Ace 5 Pro | `oneplus_ace5_pro` | Explicit model |
| OnePlus Pad 2 Pro | `oneplus_pad_2_pro` | Explicit model |
| OnePlus Pad 3 | `oneplus_pad_3` | Explicit model |
| OnePlus 15 | `oneplus_15` | Explicit model, but treat as tentative until upstream build evidence is seen |

Interpretation:
- These are explicit automation entries, not a promise that every firmware version will boot.
- If a OnePlus device is not in this list, downgrade from `explicit model` to `special workflow family` or `manual integration`.

### Pixel 8

Sources:
- `GKI_SukiSU_SUSFS/README.md`
- <https://github.com/MiRinFork/GKI_SukiSU_SUSFS/blob/main/README.md>

Upstream evidence:
- The README states that Pixel 8 was tested for its generic kernel image dynamics and could boot.

Bucket:
- Explicit model

## 2. Explicit Family and Compatibility Range

### Generic GKI-friendly families named by upstream

Source:
- `SukiSU-Ultra/docs/ja/README.md`
- `SukiSU-Ultra/docs/tr/README.md`
- <https://github.com/SukiSU-Ultra/SukiSU-Ultra/blob/main/docs/ja/README.md>
- <https://github.com/SukiSU-Ultra/SukiSU-Ultra/blob/main/docs/tr/README.md>

Families explicitly named as suitable examples for the Universal GKI route:
- Xiaomi
- Redmi
- Samsung

Pixel note from the same Japanese README:
- Pixel users are told to use the less-patched GKI build.

Bucket:
- Explicit family/range for Xiaomi, Redmi, Samsung
- Explicit guidance for Pixel users, but not an explicit all-model whitelist

### Core compatibility range from SukiSU-Ultra

Sources:
- `SukiSU-Ultra/docs/README.md`
- `SukiSU-Ultra/docs/guide/installation.md`
- <https://github.com/SukiSU-Ultra/SukiSU-Ultra/blob/main/docs/README.md>
- <https://github.com/SukiSU-Ultra/SukiSU-Ultra/blob/main/docs/guide/installation.md>

Explicit compatibility statements:
- Android 12+ devices with kernel 5.10+ may use GKI or LKM paths.
- Older kernels are also compatible, but must be built manually.
- Backports can extend support down to 3.x kernels in some cases.
- Current architecture support called out upstream: `arm64-v8a`, `armeabi-v7a (bare)`, and `x86_64` in some cases.

Bucket:
- Explicit family/range

### Workflow build ranges currently exposed by helper repos

Sources:
- `GKI_KernelSU_SUSFS/.github/workflows/*.yml`
- `GKI_SukiSU_SUSFS/.github/workflows/*.yml`
- `SukiSU-Ultra/.github/workflows/build-lkm.yml`

Explicit build matrices currently visible:
- Android 12 / kernel 5.10
- Android 13 / kernel 5.10
- Android 13 / kernel 5.15
- Android 14 / kernel 5.15
- Android 14 / kernel 6.1
- Android 15 / kernel 6.6
- Android 16 / kernel 6.12 in the lighter GKI and LKM workflows

Bucket:
- Explicit family/range

Interpretation:
- This is workflow coverage, not a per-device whitelist.

## 3. Families That Need a Different Path

### OnePlus

Sources:
- `SukiSU-Ultra/docs/guide/installation.md`
- `SukiSU-Ultra/docs/ja/README.md`
- `Action_OnePlus_MKSU_SUSFS/.github/workflows/Build-SukiSU.yml`

Upstream behavior:
- OnePlus is explicitly routed away from the generic GKI path and toward the dedicated workflow repo.

Bucket:
- Special workflow

### OPPO, realme, Meizu

Source:
- `SukiSU-Ultra/docs/guide/installation.md`
- <https://github.com/SukiSU-Ultra/SukiSU-Ultra/blob/main/docs/guide/installation.md>

Upstream wording:
- Some devices cannot be installed by using the generic GKI kernel and need manual kernel modification and compilation.
- The examples explicitly named are OPPO, OnePlus, realme, and Meizu.

Bucket:
- Manual integration

## 4. What Is Not Explicitly Confirmed

The current upstream evidence does not give a full per-model whitelist for:
- all Xiaomi models
- all Redmi models
- all Samsung models
- all Pixel models
- all OPPO or realme devices

When answering users, phrase those as:
- "clearly in the documented compatibility range" if they match the GKI criteria
- "not explicitly listed as a model in upstream docs"

Do not silently upgrade those into explicit model support.
