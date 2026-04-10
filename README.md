# Redline

An AI-powered retaining wall concept design tool. It generates **concept design** options for retaining walls
by searching and interpolating a curated database of 512 historical projects.

Target users are intermediate civil and structural engineers who need rapid,
multi-scenario concept designs without relying on the institutional memory of
senior staff.

## What it does

Given three inputs — **location**, **sector** (commercial/highway/rail/etc.),
and **retained height** — the tool returns preliminary wall dimensions:

| Output              | Description                                        |
| ------------------- | -------------------------------------------------- |
| Pile hole diameter  | Thickness of the structural pillars                |
| Pile spacing        | Distance between each pillar                       |
| Embedment depth     | How deep the wall foundation is buried             |
| Performance ranking | Cost and embodied-carbon comparison across options |

The database covers six wall types: concrete pile, sheet pile, gravity L wall,
post and panel, MSE (mechanically stabilised earth), and timber pole.

## Delivery tracks

| Track | Name             | Scope                                                      |
| ----- | ---------------- | ---------------------------------------------------------- |
| 1     | Proof of Concept | Search/Explorer — filter and retrieve raw historical data |
| 2     | Pilot            | AI Estimator — interpolation and cost/carbon ranking      |
| 3     | Production       | Full rollout and automated PDF ingestion                   |

## Important limitations

Outputs are **concept-level only** — not suitable for detailed engineering
design or building-consent submissions. The tool is restricted to walls under
8 m. A human engineer must always review the output before use.

See [docs/project/goals.md](docs/project/goals.md) for full goals, limitations,
assumptions, and open questions.
