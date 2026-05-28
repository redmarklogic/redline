# MoSCoW

## What it is

MoSCoW is a communication framework for translating a prioritised backlog into four unambiguous release-criteria buckets: **Must have**, **Should have**, **Could have**, and **Won't have**. It makes explicit what a release requires, intends, may include, and consciously excludes.

## Core principle

MoSCoW is not a prioritisation method -- it is a translation layer that converts an already-ranked list into clear, binary release decisions. The ranking must come from a prior exercise (e.g., Value-Effort matrix, ROI Scorecard). MoSCoW then communicates what those ranks mean in terms of launch criteria.

## When to invoke

- After completing prioritisation, to communicate what "high priority" means in practice
- When a team is uncertain about what must ship in the current release
- Before sprint or release planning to pre-empt scope debates
- When coordinating across teams who need unambiguous go/no-go criteria

## How to apply

1. Complete a prioritisation exercise first -- MoSCoW requires an existing ranked list
2. Assign each item to one of four buckets:
   - **Must have**: Critical-path requirements without which the product cannot launch; absence causes rejection (dissatisfiers); also called minimum-to-ship features
   - **Should have**: Important but not launch-critical; painful to exclude but not blocking; last items to cut under deadline pressure
   - **Could have**: Wanted but low importance relative to Should-haves; first items cut if budget or deadline risk arises; often delighters
   - **Won't have**: Explicitly out of scope for this release; agreed up front to prevent scope creep and mid-project rehashing
3. Validate that no dissatisfiers appear in Won't have -- if a critical need is out of scope, the release cannot provide value
4. Share with the development team so they understand release criteria, not just rank order

## Anti-patterns

- **Using MoSCoW as the prioritisation method** -- without a prior ranked list, bucket assignments become subjective and contested
- **Putting dissatisfiers in Won't have** -- if a critical customer need is out of scope, there is no viable release
- **Skipping Won't have** -- leaving scope undefined invites creep; the explicit exclusion list is as important as the Must-have list
- **Treating Could-have items as optional padding** -- they represent genuine value; acknowledge that cutting them reduces competitiveness

## Source

*Product Roadmapping: A Practical Guide to Prioritizing Opportunities, Aligning Teams, and Delivering Value to Customers* -- C. Todd Lombardo, Bruce McCarthy, Evan Ryan, Michael Connors
