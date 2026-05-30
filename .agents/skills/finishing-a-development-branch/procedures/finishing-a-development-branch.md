# Finishing A Development Branch — Detailed Reference

### Inputs
- Completed implementation on a development branch with passing tests

### Outputs
- Merge, PR, or cleanup decision executed; branch tidied

### Out of Scope
- Code implementation (`spec-kit`)
- Code review process (`requesting-code-review`)
- Test writing (`test-driven-development`)

### Step 1: Verify Tests

**Before presenting options, verify tests pass:**

```bash
### Step 2: Determine Base Branch

<!-- rtk:skip -->
```bash
### Step 3: Present Options

Present exactly these 4 options:

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

**Don't add explanation** - keep options concise.

### Step 4: Execute Choice

#### Option 1: Merge Locally

```bash
### Step 5: Cleanup Worktree

**For Options 1, 2, 4:**

Check if in worktree:
<!-- rtk:skip -->
```bash
rtk git worktree list | grep $(git branch --show-current)
```

If yes:
```bash
rtk git worktree remove <worktree-path>
```

**For Option 3:** Keep worktree.

# Finishing a Development Branch

## Overview

Guide completion of development work by presenting clear options and handling chosen workflow.

**Core principle:** Verify tests → Present options → Execute choice → Clean up.

**Announce at start:** "I'm using the finishing-a-development-branch skill to complete this work."

## The Process

# Run project's test suite
npm test / cargo test / pytest / go test ./...
```

**If tests fail:**
```
Tests failing (<N> failures). Must fix before completing:

[Show failures]

Cannot proceed with merge/PR until tests pass.
```

Stop. Don't proceed to Step 2.

**If tests pass:** Continue to Step 2.

# Try common base branches
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

Or ask: "This branch split from main - is that correct?"

# Switch to base branch
rtk git checkout <base-branch>

# Pull latest
rtk git pull

# Merge feature branch
rtk git merge <feature-branch>

# Verify tests on merged result
<test command>

# If tests pass
rtk git branch -d <feature-branch>
```

Then: Cleanup worktree (Step 5)

#### Option 2: Push and Create PR

```bash
# Push branch
rtk git push -u origin <feature-branch>

# Create PR
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<2-3 bullets of what changed>

## Test Plan
- [ ] <verification steps>
EOF
)"
```

Then: Cleanup worktree (Step 5)

#### Option 3: Keep As-Is

Report: "Keeping branch <name>. Worktree preserved at <path>."

**Don't cleanup worktree.**

#### Option 4: Discard

**Confirm first:**
```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

Wait for exact confirmation.

If confirmed:
```bash
rtk git checkout <base-branch>
rtk git branch -D <feature-branch>
```

Then: Cleanup worktree (Step 5)

## Red Flags

**Never:**
- Proceed with failing tests
- Merge without verifying tests on result
- Delete work without confirmation
- Force-push without explicit request

**Always:**
- Verify tests before offering options
- Present exactly 4 options
- Get typed confirmation for Option 4
- Clean up worktree for Options 1 & 4 only

## Integration

**Called by:**
- **subagent-driven-development** (Step 7) - After all tasks complete
- **spec-kit** implement phase - After all tasks complete

**Pairs with:**
- **using-git-worktrees** - Cleans up worktree created by that skill
