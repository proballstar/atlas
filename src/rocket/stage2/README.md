# Stage 2
Stage 2 is equipped with features that you must be aware of before attempting to use.

## Hardware Requirements
Please make sure that you are on a Linux 18.04 computer with at least 2 NVIDIA TITAN X GPUs(aaronhma setup). If you don't have one, please note that Stage 2 will not always work and if it does, will work very slowly so on a real rocket, make sure you have these requirements.

## Software Requirements
Make sure you meet at least 1 of these requirements:
1. Latest Windows version
2. Latest macOS version
3. Linux Ubuntu 18.04 (or Ubuntu 20.04 after April 4, 2020)

## Quick Start Guide
1. Startup Stage 2.
```bash
bash scripts/startup.sh
```

2. Build Stage 2 modules.
```bash
bash scripts/stage2.sh build_gpu # change this if no gpu
```

3. Launch Stage 2 UI in Honeycomb.
(refer to Rohan Fernandes guide)
```bash
bash scripts/honeycomb.sh stage2_ui
```