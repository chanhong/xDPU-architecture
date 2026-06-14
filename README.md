# xDPU – Cross-Domain Dedicated Processing Unit

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

(On June 3, 2026, Deepseek AI helps me to document my idea about xDPU)