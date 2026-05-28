# Deep Modules

## What it is

A deep module provides a simple, narrow interface that hides substantial internal complexity. A shallow module has an interface nearly as complex as the implementation it wraps, providing little abstraction benefit. The depth of a module is the ratio of functionality provided to interface complexity imposed on callers.

## Core principle

The best modules maximise information hiding: expose the simplest interface possible while absorbing as much complexity as possible behind it. The cognitive cost a caller must pay (interface complexity) should be far smaller than the benefit the module delivers.

## When to invoke

- Deciding how to split or consolidate a module, class, or function
- Evaluating whether to extract a helper function or inline it
- Reviewing whether an abstraction is worth the overhead it introduces
- Diagnosing why adding features to a codebase feels increasingly expensive

## How to apply

1. Identify the interface cost: count the concepts, parameters, and knowledge a caller must hold to use the module correctly
2. Identify the functionality benefit: assess how much complexity the module absorbs from its callers
3. Evaluate depth: if the interface cost is close to the implementation complexity, the module is shallow and provides little value -- consider merging or redesigning it
4. Prefer fewer, more powerful modules over many narrow ones that leak complexity upward
5. Hide complexity, not information: expose only what callers need; bury everything else behind a clean boundary

## Anti-patterns

- **Classitis** -- a bias toward many small classes or functions to achieve "clean" structure, producing a shallow, fragmented design where no single module provides meaningful abstraction
- **Pass-through methods** -- methods that simply forward calls to another module without adding any abstraction; a sign the module boundary is in the wrong place
- **Interface inflation** -- adding parameters "for flexibility" that every caller must understand and manage, eroding the depth of the module over time

## Source

*A Philosophy of Software Design* (2nd ed.) -- John Ousterhout (Stanford University Press, 2021)
