# xDPU: A Heterogeneous, Optically‑Interconnected, 3D‑Stacked Processing Unit  
## for Extreme Power Efficiency and No‑Moving‑Parts Reliability (with SPU)

## Abstract

The end of Dennard scaling and the rise of edge, mobile, and space computing demand a radical departure from general‑purpose CPUs. The xDPU (Cross‑Domain Dedicated Processing Unit) integrates a slim control CPU, a parallelization unit (PPU), a central math unit (MPU), a neural engine (NPU), a graphics core (GPU), and a **secure processing unit (SPU)** into a single 3D‑stacked package. Shared cache, on‑chip silicon photonics, and thermal interleaving eliminate redundant data movement and active cooling. The SPU provides isolated TPM/DRM/crypto functions. This paper presents the architecture, operation, power estimates, and a roadmap to implementation.

## 1. Introduction

Modern system-on-chips (SoCs) rely on a few large CPU cores augmented by fixed-function accelerators. While GPUs and NPUs improve throughput, they still suffer from:
- **Redundant logic** – CPUs include ALUs/FPUs that duplicate accelerator capabilities.
- **Costly data movement** – cache coherency across separate dies wastes power.
- **Thermal constraints** – fans and pumps fail in vacuum or high-vibration environments (space, deep drilling).
- **Security isolation** – software-based TEEs are vulnerable to side-channel attacks.

The xDPU solves these by **specialisation, optical communication, passive thermal management, and hardware-isolated security**.

## 2. Architectural Overview

### 2.1 Processing Tiles

All tiles are **3D‑stacked** and communicate via a shared last‑level cache (LLC) and optical links (except the SPU, which uses a dedicated bus to the CPU).

| Tile | Function | Key Features |
|------|----------|---------------|
| **Slim CPU** | Sequential control, dispatch, I/O | In‑order, no FPU/SIMD, tiny L0 I‑cache |
| **PPU** | Parallelisation | Hardware task‑graph generator, dependency analysis |
| **MPU** | Central math engine | FP/INT ALUs, transcendental (sin, log, etc.); supports AVX2‑width vectors |
| **NPU** | Neural inference | Systolic array, sparse tensor core |
| **GPU** | Graphics & massive parallel compute | Shader cores, texture units, rasteriser |
| **SPU** | Secure processing | Isolated microcontroller, hardware crypto (AES‑256, SHA‑256, RSA, ECC), OTP memory, tamper detection |

### 2.2 Shared Cache Hierarchy

- **L2 slices** (256 KiB each) distributed across tiles, aggregated as a shared L3 via directory.
- **Coherence** – directory-based with optical snooping; no write-invalidates over electrical buses.
- **Benefits** – MPU results written once, read by NPU/GPU without DRAM traffic.
- **SPU exception** – SPU does not share the LLC; it has its own secure SRAM (64-256 KiB) and cannot be DMAed by other tiles.

### 2.3 Optical Interconnects

- **Physical layer** – silicon waveguides, ring modulators, Ge photodetectors (e.g., GlobalFoundries Fotonix).
- **Topology** – 2D mesh over the 3D stack; each non-secure tile has an optical interface.
- **Energy** – <100 fJ/bit (vs. >1 pJ/bit for long electrical lines). Latency ~1 ns per hop.
- **SPU exception** – SPU communicates with slim CPU via a dedicated, encrypted bus (e.g., I2C or APB) to prevent side-channel leaks through optics.

### 2.4 3D Stacking & Thermal Interleaving

**Stack order (bottom to top, through-silicon vias – TSVs):**
1. Thermal spreader (diamond or pyrolytic graphite)
2. Cool tiles: LLC slices, MPU, SPU
3. Warm tiles: PPU, NPU
4. Hot tiles: Slim CPU, GPU
5. Top radiative coating

**Holes:** TSVs for power/ground and **thermal vias** (copper or diamond-filled) to conduct heat laterally/vertically. No microfluidic channels – fully solid-state.

### 2.5 Secure Processing Unit (SPU) – Detailed

The SPU is a **simple, secure microcontroller** running at low frequency (100-300 MHz) to minimise side-channel leakage. It includes:
- **Hardware crypto engines** – AES-256 (GCM, CBC), SHA-256, SHA-3, RSA-4096, ECDSA (P-256/384).
- **True Random Number Generator (TRNG)**.
- **Secure non-volatile storage** – 256 KiB OTP, plus a small amount of flash/eFuses for keys.
- **Tamper detection** – active shield, temperature/voltage sensors, zeroisation logic.
- **Isolated power domain** – can remain powered while other tiles are off.

**Typical use cases:**
- Platform attestation (measured boot, TPM 2.0).
- DRM decryption (e.g., Widevine L1, PlayReady).
- Key storage (e.g., for disk encryption, secure boot).
- Hardware‑accelerated TLS (for small embedded servers).

The slim CPU sends commands to the SPU via a **mailbox** – a small shared SRAM (4 KiB) with hardware encryption. The SPU never executes code from untrusted memory.

## 3. Operation Modes & Task Flow

### 3.1 Sequential to Parallel Conversion

1. **Slim CPU** receives a high-level request (e.g., "decrypt this DRM-protected video and upscale it with AI").
2. **PPU** decomposes into a dependency graph:
   - SPU → decrypt content key and license
   - NPU → AI upscaling (frame by frame)
   - GPU → motion interpolation + rendering
   - MPU → blending math
3. PPU dispatches directly to each tile via optical link (except SPU via mailbox), waking them from power-gate.
4. CPU sleeps until completion interrupt.

### 3.2 Data Movement Minimisation

- **Shared LLC** – MPU writes results to a cache line; NPU/GPU reads same line.
- **Optical forwarding** – GPU reads texture data directly from CPU's LLC slice without evicting to DRAM.
- **No redundant copies** – zero-copy semantics enforced by hardware.
- **Secure channel** – SPU sends clear keys to GPU via a dedicated, encrypted one-way path (bypassing CPU and LLC).

### 3.3 Race-to-Idle Power Management

All tiles run at maximum frequency to finish the job as fast as possible. After completion, tiles enter **clock gating** (sub-1 mW) or **power gating** (near-zero leakage). Optical links shutdown after 10 µs inactivity. SPU may remain powered in low-power mode to monitor tamper sensors.

## 4. Power & Thermal Analysis (Estimated)

### 4.1 Power Breakdown vs. Conventional SoC

Workload: 4K video with AI upscaling + optical flow + DRM decryption (30 fps), 7 nm process.

| Component | Conventional (W) | xDPU (W) |
|-----------|------------------|----------|
| CPU (including TEE overhead) | 3.0 | 0.3 |
| GPU | 5.0 | 4.0 |
| NPU | 2.0 | 2.0 |
| DRAM access | 4.0 | 1.2 |
| SPU | (included in CPU) | 0.1 |
| **Total** | **14.0** | **7.6** |

For mixed workloads with idle intervals, total system power is **65-80% lower**.

### 4.2 Thermal Performance

- **Power density** – 20 W/mm² hot spots (GPU) interleaved with 0.5 W/mm² cache and 0.1 W/mm² SPU → effective peak temperature rise ΔT = 35°C above ambient.
- **Passive cooling** – natural convection + radiative emission (ε=0.9 coating) + chassis conduction.
- **Maximum ambient** – 45°C (spacecraft interior) keeps junction <85°C. No fans, no pumps.

## 5. Use Cases

| Domain | Why xDPU Wins |
|--------|----------------|
| Deep space probes | No moving parts – survives launch vibration & vacuum; radiation-tolerant optics. |
| Smartphones / wearables | Lower active power → 2× battery life; cooler surface; SPU handles payments/DRM. |
| Edge AI cameras with DRM | Real-time NPU + MPU + GPU without fan; SPU protects decryption keys. |
| Secure edge servers | Hardware-isolated TPM and crypto; no CPU overhead for encryption. |
| Data center "cold storage" | Passive cooling reduces PUE; SPU manages encryption keys. |

## 6. Implementation Roadmap

| Phase | Description |
|-------|-------------|
| 1 – Simulation (6 months) | Extend Gem5 with xDPU tiles (including SPU model); validate >50% power reduction. |
| 2 – FPGA Emulation (1 year) | Single tile (CPU+MPU+SPU+cache) on Xilinx Alveo; emulate optical link; test SPU isolation. |
| 3 – Chiplet Prototype (2-3 years) | 28nm or 65nm chiplets, 3D stacking, thermal vias test chip; SPU on separate power domain. |
| 4 – Full xDPU (5 years) | Monolithic 7nm/5nm or advanced chiplet integration (UCIe), integrated photonics; SPU with active shield. |

## 7. Challenges & Mitigations

| Challenge | Mitigation |
|-----------|------------|
| Optical link temperature sensitivity | Athermal design + closed-loop heater control; drift <0.1 nm/°C. |
| 3D stacking heat removal | Interleaving + thermal TSVs + diamond heat spreader (2000 W/m·K). |
| Coherence across optical links | Directory-based with speculative optical probing (2-3 cycle latency). |
| Software ecosystem | Extend OpenCL 3.0, ONNX Runtime; provide LLVM backend for slim CPU; SPU firmware toolchain. |
| Manufacturing cost | High-volume markets amortise; space-grade tolerates lower volume. |
| SPU isolation | Separate power/clock, dedicated bus, active shield, TVLA side-channel testing. |

## 8. Conclusion

The xDPU redefines heterogeneous computing for a future where **power efficiency, reliability, and security** are paramount. By integrating a slim CPU, dedicated accelerators (PPU, MPU, NPU, GPU, SPU), shared cache, optical interconnects, and thermal interleaving into a single 3D-stacked package, the xDPU achieves:
- **65-80% lower total system power** for mixed workloads.
- **No moving parts** – ideal for space and vibration-prone environments.
- **Passive cooling** – eliminates fans and liquid pumps.
- **Hardware-isolated security** – SPU protects keys and DRM without performance penalty.

## 9. References

1. DARPA CHIPS (Common Heterogeneous Integration and IP Reuse Strategies) program.
2. Intel Foveros 3D stacking technology.
3. Ayar Labs – optical I/O for compute.
4. Google TPUv4: systolic array NPU.
5. Apple M2 / M3 matrix coprocessor (MPU analogue) and Secure Enclave (SPU analogue).
6. GlobalFoundries Fotonix™ – monolithic silicon photonics platform.
7. MIT Lincoln Laboratory – thermal via arrays for 3D ICs.
8. Gem5 simulator – architectural modelling.
9. TCG TPM 2.0 Library Specification.
10. Google Widevine L1 DRM – hardware security requirements.

**Document version 1.1 – added SPU.**
