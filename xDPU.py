#!/usr/bin/env python3
"""
xDPU Architecture File Generator
Creates ALL original whitepaper files (full length) and packages them into a ZIP archive.
"""

import os
import zipfile

# ----------------------------------------------------------------------
# FULL FILE CONTENTS (matching the original responses)
# ----------------------------------------------------------------------

README_MD = """# xDPU – Cross-Domain Dedicated Processing Unit

**A no-moving-parts, optically-interconnected, 3D‑stacked heterogeneous processor for extreme power efficiency and built‑in security.**

## Abstract

The xDPU integrates a slim CPU, parallelization unit (PPU), central math unit (MPU), neural engine (NPU), GPU, and **secure processing unit (SPU)** into a single 3D‑stacked package. Shared cache, on‑chip silicon photonics, and thermal interleaving eliminate redundant data movement and active cooling – enabling 65‑80% lower power than conventional SoCs, with no fans or pumps. The SPU handles TPM, DRM, and key storage in an isolated, tamper‑resistant environment.

## Repository contents

- `xDPU_whitepaper.md` – full architecture description (includes SPU)
- `xDPU_whitepaper.tex` – LaTeX source for academic formatting
- `README.md` – this file
- `executive-summary.txt` – two‑page summary

## Call to action

We are looking for collaborators to:

- **Simulate** – extend Gem5 or Sniper to model xDPU tiles (including SPU)
- **FPGA** – implement a single tile (e.g., CPU+MPU+SPU+shared cache) on Xilinx/Altera
- **Tape out** – submit a test chip via Tiny Tapeout or Google's Open MPW shuttle
- **Write** – co‑author an arXiv paper or IEEE conference submission

## Getting involved

- Open an issue for questions or ideas
- Fork the repo and submit a pull request with your simulation code or design files
- Email the maintainer (add your contact here) for direct collaboration

## License

This work is released under **Creative Commons BY‑SA 4.0** (share and adapt with attribution).
"""

# ----------------------------------------------------------------------
# FULL EXECUTIVE SUMMARY
# ----------------------------------------------------------------------
EXECUTIVE_SUMMARY = """xDPU Executive Summary – Page 1 of 2 (updated with SPU)

WHAT IS xDPU?
The xDPU (Cross‑Domain Dedicated Processing Unit) is a single 3D‑stacked chip containing:
- Slim CPU (in‑order, no FPU/SIMD – just control)
- PPU (hardware task‑graph paralleliser)
- MPU (central math engine – FP/INT/transcendental; includes AVX2-level vectors)
- NPU (systolic neural engine)
- GPU (shader cores for graphics & compute)
- SPU (Secure Processing Unit – isolated TPM/DRM/crypto)
- Shared last‑level cache (for non‑secure tiles)
- Optical interconnects (silicon photonics, SPU excluded)
- Thermal vias + interleaving (hot/cool tiles)

WHY IT'S DIFFERENT
- No moving parts → no fans, no pumps; survives space vacuum & vibration
- Passive cooling only (radiative + conductive)
- 65-80% lower total system power for mixed workloads (est. based on 7nm)
- Built‑in hardware security (TPM 2.0, DRM, key storage) without performance penalty

KEY NUMBERS (vs. conventional SoC, same 7nm, 4K AI+video+DRM task)
- CPU power: 3.0W → 0.3W  (90% reduction)
- DRAM access power: 4.0W → 1.2W (70% reduction – shared cache + optics)
- SPU power: 0.1W (new, replaces CPU‑based TPM overhead)
- Total power: 14.0W → 7.6W (46% reduction; idle intervals push to 65-80%)
- Peak junction temp: <85°C at 45°C ambient, no airflow

HOW IT WORKS (secure example)
1. CPU sends encrypted license and key to SPU.
2. SPU decrypts key inside its isolated SRAM, never exposes plaintext.
3. SPU sets up GPU secure channel for content decryption.
4. CPU sleeps, SPU monitors tamper sensors, GPU renders protected video.

ROADMAP (realistic, low‑cost start)
Phase 1 – Simulation (6 months, 1-2 engineers)
→ Extend Gem5 with xDPU tiles; validate power/performance.

Phase 2 – FPGA Emulation (1 year, small team)
→ One tile (CPU+MPU+cache) on Xilinx Alveo; emulate optical link.

Phase 3 – Chiplet Prototype (2-3 years, <$50k)
→ 28nm or 65nm test chip via Tiny Tapeout / Google MPW; measure thermal interleaving.

Phase 4 – Full xDPU (5 years, commercial partner)
→ 7nm/5nm monolithic or UCIe chiplets with integrated photonics.

WHAT WE NEED
- Simulation experts (Gem5, Sniper)
- FPGA / RTL designers (Verilog/VHDL for one tile)
- Packaging / thermal engineers (3D stacking, thermal vias)
- A motivated student team or startup to lead a tape‑out

NEXT STEPS
- Read the full whitepaper (Markdown or LaTeX in the GitHub repo)
- Try the simulation or FPGA path yourself
- Contact [Your Name] to discuss collaboration or sponsorship
"""

# ----------------------------------------------------------------------
# FULL MARKDOWN WHITEPAPER
# ----------------------------------------------------------------------
WHITEPAPER_MD = """# xDPU: A Heterogeneous, Optically‑Interconnected, 3D‑Stacked Processing Unit  
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
"""

# ----------------------------------------------------------------------
# FULL LATEX WHITEPAPER (exactly as originally provided)
# ----------------------------------------------------------------------
WHITEPAPER_TEX = r"""\documentclass[10pt,twocolumn]{article}
\usepackage{amsmath, amssymb}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{caption}
\usepackage{hyperref}
\usepackage{cite}

\title{xDPU: A Heterogeneous, Optically-Interconnected, 3D-Stacked Processing Unit\\ 
\large for Extreme Power Efficiency, No-Moving-Parts Reliability, and Built-in Security}

\author{Architecture Whitepaper}
\date{\today}

\begin{document}

\twocolumn[
\maketitle
\begin{abstract}
The end of Dennard scaling and the rise of edge, mobile, and space computing demand a radical departure from general-purpose CPUs. The xDPU (Cross-Domain Dedicated Processing Unit) integrates a slim control CPU, a parallelization unit (PPU), a central math unit (MPU), a neural engine (NPU), a graphics core (GPU), and a \textbf{secure processing unit (SPU)} into a single 3D-stacked package. Shared cache, on-chip silicon photonics, and thermal interleaving eliminate redundant data movement and active cooling. The SPU provides isolated TPM, DRM, and cryptographic functions. This paper presents the architecture, operation, power estimates, and a roadmap to implementation.
\end{abstract}
]

\section{Introduction}

Modern system-on-chips (SoCs) rely on a few large CPU cores augmented by fixed-function accelerators. While GPUs and NPUs improve throughput, they still suffer from:
\begin{itemize}
\item \textbf{Redundant logic} – CPUs include ALUs/FPUs that duplicate accelerator capabilities.
\item \textbf{Costly data movement} – cache coherency across separate dies wastes power.
\item \textbf{Thermal constraints} – fans and pumps fail in vacuum or high-vibration environments (space, deep drilling).
\item \textbf{Security isolation} – software-based TEEs (Trusted Execution Environments) are vulnerable to side-channel attacks.
\end{itemize}
The xDPU solves these by \textbf{specialisation, optical communication, passive thermal management, and hardware-isolated security}.

\section{Architectural Overview}

\subsection{Processing Tiles}
All tiles are \textbf{3D-stacked} and communicate via a shared last-level cache (LLC) and optical links (except the SPU, which uses a dedicated bus to the CPU).

\begin{table}[ht]
\centering
\caption{xDPU processing tiles}
\label{tab:tiles}
\begin{tabular}{@{}lll@{}}
\toprule
\textbf{Tile} & \textbf{Function} & \textbf{Key Features} \\
\midrule
Slim CPU & Sequential control, dispatch, I/O & In-order, no FPU/SIMD, tiny L0 I-cache \\
PPU & Parallelisation & Hardware task-graph generator, dependency analysis \\
MPU & Central math engine & FP/INT ALUs, transcendental (sin, log, etc.); supports AVX2-width vectors \\
NPU & Neural inference & Systolic array, sparse tensor core \\
GPU & Graphics \& massive parallel compute & Shader cores, texture units, rasteriser \\
SPU & Secure processing & Isolated microcontroller, hardware crypto (AES-256, SHA-256, RSA, ECC), OTP memory, tamper detection \\
\bottomrule
\end{tabular}
\end{table}

\subsection{Shared Cache Hierarchy}
\begin{itemize}
\item \textbf{L2 slices} (256 KiB each) distributed across tiles, aggregated as a shared L3 via directory.
\item \textbf{Coherence} – directory-based with optical snooping; no write-invalidates over electrical buses.
\item \textbf{Benefits} – MPU results written once, read by NPU/GPU without DRAM traffic.
\item \textbf{SPU exception} – SPU does not share the LLC; it has its own secure SRAM (64-256 KiB) and cannot be DMAed by other tiles.
\end{itemize}

\subsection{Optical Interconnects}
\begin{itemize}
\item \textbf{Physical layer} – silicon waveguides, ring modulators, Ge photodetectors (e.g., GlobalFoundries Fotonix).
\item \textbf{Topology} – 2D mesh over the 3D stack; each non-secure tile has an optical interface.
\item \textbf{Energy} – \(<100\) fJ/bit (vs. \(>1\) pJ/bit for long electrical lines). Latency \(\sim1\) ns per hop.
\item \textbf{SPU exception} – SPU communicates with slim CPU via a dedicated, encrypted bus (e.g., I2C or APB) to prevent side-channel leaks through optics.
\end{itemize}

\subsection{3D Stacking \& Thermal Interleaving}

\textbf{Stack order (bottom to top, through-silicon vias – TSVs):}
\begin{enumerate}
\item Thermal spreader (diamond or pyrolytic graphite)
\item Cool tiles: LLC slices, MPU, SPU
\item Warm tiles: PPU, NPU
\item Hot tiles: Slim CPU, GPU
\item Top radiative coating
\end{enumerate}

\textbf{Holes:} TSVs for power/ground and \textbf{thermal vias} (copper or diamond-filled) to conduct heat laterally/vertically. No microfluidic channels – fully solid-state.

\subsection{SPU (Secure Processing Unit) – Detailed}

The SPU is a \textbf{simple, secure microcontroller} running at low frequency (100–300 MHz) to minimise side-channel leakage. It includes:
\begin{itemize}
\item \textbf{Hardware crypto engines} – AES-256 (GCM, CBC), SHA-256, SHA-3, RSA-4096, ECDSA (P-256/384).
\item \textbf{True Random Number Generator (TRNG)}.
\item \textbf{Secure non-volatile storage} – 256 KiB OTP, plus small flash/eFuses for keys.
\item \textbf{Tamper detection} – active shield, temperature/voltage sensors, zeroisation logic.
\item \textbf{Isolated power domain} – can remain powered while other tiles are off.
\end{itemize}

\textbf{Typical use cases:}
\begin{itemize}
\item Platform attestation (measured boot, TPM 2.0).
\item DRM decryption (e.g., Widevine L1, PlayReady).
\item Key storage (disk encryption, secure boot).
\item Hardware-accelerated TLS for embedded servers.
\end{itemize}

The slim CPU sends commands to the SPU via a \textbf{mailbox} – a small shared SRAM (4 KiB) with hardware encryption. The SPU never executes code from untrusted memory.

\section{Operation Modes \& Task Flow}

\subsection{Sequential to Parallel Conversion}
\begin{enumerate}
\item \textbf{Slim CPU} receives a high-level request (e.g., "decrypt this DRM-protected video and upscale it with AI").
\item \textbf{PPU} decomposes into a dependency graph:
      \begin{itemize}
      \item SPU → decrypt content key and license
      \item NPU → AI upscaling (frame by frame)
      \item GPU → motion interpolation + rendering
      \item MPU → blending math
      \end{itemize}
\item PPU dispatches directly to each tile via optical link (except SPU via mailbox), waking them from power-gate.
\item CPU sleeps until completion interrupt.
\end{enumerate}

\subsection{Data Movement Minimisation}
\begin{itemize}
\item \textbf{Shared LLC} – MPU writes results to a cache line; NPU/GPU reads same line.
\item \textbf{Optical forwarding} – GPU reads texture data directly from CPU's LLC slice without evicting to DRAM.
\item \textbf{No redundant copies} – zero-copy semantics enforced by hardware.
\item \textbf{Secure channel} – SPU sends clear keys to GPU via a dedicated, encrypted one-way path (bypassing CPU and LLC).
\end{itemize}

\subsection{Race-to-Idle Power Management}
All tiles run at maximum frequency to finish the job as fast as possible. After completion, tiles enter \textbf{clock gating} (sub 1 mW) or \textbf{power gating} (near-zero leakage). Optical links shutdown after 10 µs inactivity. SPU may remain powered in low‑power mode to monitor tamper sensors.

\section{Power \& Thermal Analysis (Estimated)}

\subsection{Power Breakdown vs. Conventional SoC}
Workload: 4K video with AI upscaling + optical flow + DRM decryption (30 fps), 7 nm process.

\begin{table}[ht]
\centering
\caption{Power comparison (conventional vs. xDPU)}
\label{tab:power}
\begin{tabular}{@{}lcc@{}}
\toprule
\textbf{Component} & \textbf{Conventional (W)} & \textbf{xDPU (W)} \\
\midrule
CPU (including TEE overhead) & 3.0 & 0.3 \\
GPU & 5.0 & 4.0 \\
NPU & 2.0 & 2.0 \\
DRAM access & 4.0 & 1.2 \\
SPU & (included in CPU) & 0.1 \\
\midrule
\textbf{Total} & \textbf{14.0} & \textbf{7.6} \\
\bottomrule
\end{tabular}
\end{table}

For mixed AI + physics + graphics + security workloads, total system power is \textbf{65–80\% lower} (idle intervals dominate).

\subsection{Thermal Performance}
\begin{itemize}
\item \textbf{Power density} – 20 W/mm² hot spots (GPU) interleaved with 0.5 W/mm² cache and 0.1 W/mm² SPU → effective peak temperature rise \(\Delta T = 35^\circ\)C above ambient.
\item \textbf{Passive cooling} – natural convection + radiative emission (\(\varepsilon=0.9\) coating) + chassis conduction.
\item \textbf{Maximum ambient} – 45 °C (spacecraft interior) keeps junction \(<85^\circ\)C. No fans, no pumps.
\end{itemize}

\section{Use Cases}

\begin{table}[ht]
\centering
\caption{Target use cases and benefits}
\label{tab:usecases}
\begin{tabular}{@{}lp{6cm}@{}}
\toprule
\textbf{Domain} & \textbf{Why xDPU Wins} \\
\midrule
Deep space probes & No moving parts – survives launch vibration \& vacuum; radiation-tolerant optics. \\
Smartphones / wearables & Lower active power → 2× battery life; cooler surface; SPU handles payments/DRM. \\
Edge AI cameras with DRM & Real-time NPU + MPU + GPU without fan; SPU protects decryption keys. \\
Secure edge servers & Hardware-isolated TPM and crypto; no CPU overhead for encryption. \\
Data center "cold storage" & Passive cooling reduces PUE; SPU manages encryption keys. \\
\bottomrule
\end{tabular}
\end{table}

\section{Implementation Roadmap}

\begin{table}[ht]
\centering
\caption{Roadmap phases}
\label{tab:roadmap}
\begin{tabular}{@{}lp{7cm}@{}}
\toprule
\textbf{Phase} & \textbf{Description} \\
\midrule
1 – Simulation (6 months) & Extend Gem5 with xDPU tiles (including SPU model); validate \(>\)50\% power reduction. \\
2 – FPGA Emulation (1 year) & Single tile (CPU+MPU+SPU+cache) on Xilinx Alveo; emulate optical link via high-speed transceivers; test SPU isolation. \\
3 – Chiplet Prototype (2-3 years) & 28 nm or 65 nm chiplets, 3D stacking, thermal vias test chip; SPU on separate power domain. \\
4 – Full xDPU (5 years) & Monolithic 7 nm/5 nm or advanced chiplet integration (UCIe), integrated photonics; SPU with active shield. \\
\bottomrule
\end{tabular}
\end{table}

\section{Challenges \& Mitigations}

\begin{table}[ht]
\centering
\caption{Key challenges and proposed mitigations}
\label{tab:challenges}
\begin{tabular}{@{}lp{7cm}@{}}
\toprule
\textbf{Challenge} & \textbf{Mitigation} \\
\midrule
Optical link temperature sensitivity & Athermal design + closed-loop heater control; drift \(<0.1\) nm/°C. \\
3D stacking heat removal & Interleaving + thermal TSVs + diamond heat spreader (2000 W/m·K). \\
Coherence across optical links & Directory-based with speculative optical probing (2-3 cycle latency). \\
Software ecosystem & Extend OpenCL 3.0, ONNX Runtime; provide LLVM backend for slim CPU; SPU firmware toolchain. \\
Manufacturing cost & High-volume markets (phones, laptops) amortise; space-grade tolerates lower volume. \\
SPU isolation & Separate power/clock, dedicated bus, active shield, TVLA side-channel testing. \\
\bottomrule
\end{tabular}
\end{table}

\section{Conclusion}

The xDPU redefines heterogeneous computing for a future where \textbf{power efficiency, reliability, and security} are paramount. By integrating a slim CPU, dedicated accelerators (PPU, MPU, NPU, GPU, SPU), shared cache, optical interconnects, and thermal interleaving into a single 3D-stacked package, the xDPU achieves:
\begin{itemize}
\item \textbf{65–80\% lower total system power} for mixed workloads.
\item \textbf{No moving parts} – ideal for space and vibration-prone environments.
\item \textbf{Passive cooling} – eliminates fans and liquid pumps.
\item \textbf{Hardware-isolated security} – SPU protects keys and DRM without performance penalty.
\end{itemize}

Every subsystem already exists as a separate research prototype; integration is the remaining engineering challenge. We invite academic and industrial partners to collaborate on simulation, prototyping, and standardisation.

\begin{thebibliography}{9}
\bibitem{darpa} DARPA CHIPS (Common Heterogeneous Integration and IP Reuse Strategies) program.
\bibitem{foveros} Intel Foveros 3D stacking technology.
\bibitem{ayar} Ayar Labs – optical I/O for compute.
\bibitem{tpu} Google TPUv4: systolic array NPU.
\bibitem{apple} Apple M2 / M3 matrix coprocessor (MPU analogue) and Secure Enclave (SPU analogue).
\bibitem{gf} GlobalFoundries Fotonix™ – monolithic silicon photonics platform.
\bibitem{mitll} MIT Lincoln Laboratory – thermal via arrays for 3D ICs.
\bibitem{gem5} Gem5 simulator – architectural modelling.
\bibitem{tpm} TCG TPM 2.0 Library Specification.
\bibitem{widevine} Google Widevine L1 DRM – hardware security requirements.
\end{thebibliography}

\appendix
\section{Acronyms}

\begin{table}[ht]
\centering
\begin{tabular}{@{}ll@{}}
\toprule
\textbf{Acronym} & \textbf{Meaning} \\
\midrule
xDPU & Cross-Domain Dedicated Processing Unit \\
PPU  & Parallelization Processing Unit \\
MPU  & Math Processing Unit \\
NPU  & Neural Processing Unit \\
GPU  & Graphics Processing Unit \\
SPU  & Secure Processing Unit \\
LLC  & Last-Level Cache \\
TSV  & Through-Silicon Via \\
PIC  & Photonic Integrated Circuit \\
UCIe & Universal Chiplet Interconnect Express \\
TPM  & Trusted Platform Module \\
DRM  & Digital Rights Management \\
OTP  & One-Time Programmable (memory) \\
\bottomrule
\end{tabular}
\end{table}

\end{document}
"""

# ----------------------------------------------------------------------
# Main: write files and create ZIP
# ----------------------------------------------------------------------
def main():
    files = {
        "README.md": README_MD,
        "executive-summary.txt": EXECUTIVE_SUMMARY,
        "xDPU_whitepaper.md": WHITEPAPER_MD,
        "xDPU_whitepaper.tex": WHITEPAPER_TEX,
    }

    # Write files to current directory
    for filename, content in files.items():
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✓ Created {filename}")

    # Create ZIP archive
    zip_name = "xDPU-architecture.zip"
    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        for filename in files.keys():
            zipf.write(filename)
            print(f"✓ Added {filename} to {zip_name}")

    print(f"\n✅ All done! Archive ready: {zip_name}")
    print("You can now share or extract the files.")

if __name__ == "__main__":
    main()