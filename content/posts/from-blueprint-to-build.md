---
title: "From Blueprint to Build with Baton"
date: 2026-06-26
excerpt: "I write the blueprint. A crew of AI agents builds code worth reviewing."
---

<img src="/img/baton.jpg" alt="Two robot hands passing a rainbow baton — spec, tests, implement, review, ship" style="width:100%;border-radius:8px;margin-bottom:1.5rem;">

**[Check out baton on GitHub →](https://github.com/cbohara/baton)**

For a while now I have wanted to hand a whole task off to an AI agent, go get a coffee, and come back to working code. I use AI assistants all day at work, but that copilot-style workflow kept me glued to the keyboard, steering the agent one message at a time. I had a feeling we were a lot closer to walk-away-and-come-back than my daily routine was letting me get, but I didn't know how to get there.

I am grateful a coworker shared the blog post that gave me the push I needed: [The 8 Levels of Agentic Engineering](https://www.bassimeledath.com/blog/levels-of-agentic-engineering). It lays out a staircase from chatting with an assistant at the bottom all the way up to systems where agents do the work on their own. I could see where I wanted to go on that staircase, but I could not picture the actual steps to climb it. Shortly after, I read an O'Reilly piece called [How to Write a Good Spec for AI Agents](https://www.oreilly.com/radar/how-to-write-a-good-spec-for-ai-agents/), and everything clicked. Just like an architect hands a builder a blueprint, the most useful thing I can hand an agent is a clear spec. If I write the plan clearly enough, the agent can build from it. I would highly recommend reading both!

So I built [baton](https://github.com/cbohara/baton), a workflow for Claude Code that takes a GitHub issue all the way from a written plan to a pull request that is ready for review. It is one slash command and a handful of agent files, all plain markdown, and it has changed how I spend my days as a developer.

## Why the blueprint matters

I grew up around blueprints. My dad built homes, and my husband is a civil engineer, so I have spent a lot of my life around people whose whole job is to get the plan right before anyone picks up a tool. They will be the first to tell you that the quality of a house is decided long before the foundation is poured. If the blueprint is wrong, even the best crew will build the wrong house.

For most of my career, software has not worked that way. Depending on the team and the deadline, there might be some architecture work up front, but the actual task usually got figured out at the keyboard, one decision at a time, while I was already typing. That approach made sense when I was the one writing every line. Now that an agent is doing the typing, the quality of what I get back depends on how well I describe what I want, not on how well I write code.

## The workflow

Every run is the same five phases, in the same order. I've been calling it STIRS. You point it at a GitHub issue and it takes that issue from an approved plan to a merged pull request:

```
/baton 163

Spec → Tests → Implement → Review → Ship
```

I named it baton because each phase does its piece and passes the work to the next, like runners in a relay race. The spec hands off to the tests, the tests hand off to the implementer, and the implementer hands off to the reviewer. The anchor leg, ship, opens the pull request and lands it. (Fun side note - a baton is also what a conductor uses to keep an orchestra full of specialists playing in time without playing a single note themselves, which fits too.) I run a version of this at work as well, wired up a little differently for my team and the tools there.

There is one rule that makes the whole thing work: baton never writes a line of code itself. Think of it like a general contractor. Growing up, my dad didn't pour every foundation or hang every door. He ran the crew and made sure the house matched the plans. baton does the same thing for a GitHub issue. It brings in each agent at the right moment and holds all of them to the same spec.

Each phase runs as its own agent with a fresh context, and the only thing that passes from one phase to the next is the work itself, not the whole conversation. I learned this separation matters the hard way. If you hand one agent the entire job, it starts agreeing with itself: it writes the code, writes tests that pass for the code it just wrote, and then approves its own work in review. Keeping the phases separate keeps everyone honest.

Let me walk through each phase, starting where every build starts: the plan.

## Spec

The spec is where my energy goes now, but I don't start from a blank page. Before the *spec-writer* agent writes a word, a *code-explorer* agent reads the actual code and hands back a short map of the files the task touches. This step matters because a GitHub issue describes the behavior I want, not the files where that behavior lives. Letting an agent trace the real code first means the plan reflects the system that is actually there, not the one I imagined when I wrote the issue.

Every spec comes back in the same shape:

- **Goal** — the problem, and who it's for.
- **Acceptance criteria** — numbered, testable, and observable. Each one maps to a test.
- **Boundaries** — the files the agent may touch, and the ones it must not.
- **Implementation** — one line per file describing what changes. No code, just intent.
- **Tests** — a short table: each test, what it proves, and whether the file is new or already exists.

Before that spec gets anywhere near me, a *spec-critic* agent reads it cold and sorts what it finds into two piles. Anything with one right answer — a vague criterion, a missing edge case, a file the boundaries forbid — goes back to the spec-writer, and I never see it. What is left are the real forks, where two reasonable readings would build two different things. It caps those at three and labels each one cheap to reverse or a one-way door.

That last label is what finally got me my coffee. By default baton no longer stops to ask. It takes the critic's recommendation on the cheap-to-reverse calls and writes down what it assumed — the question, the options, what it picked, and why — in the spec, in the issue, and near the top of the pull request. The reviewer is told to read that section with extra suspicion, because it is the one part of the contract no human signed off on. Two things still stop the run and wait for me: a spec too vague to be a contract at all, and a one-way door like a schema change or a public interface.

When I do want to read every spec before a test gets written, I flip it to ask mode and it stops there instead. Either way, the approved spec is the contract every phase after it answers to.

## Tests

Test-driven development is one of those practices I learned about early in my career and nodded along to, but I never once saw a team consistently do it in the wild. Agents are what finally made it real for me.

A *test-writer* agent turns each acceptance criterion in the spec into a failing test, before any implementation exists. The order matters here. If you build first and test second, especially with the same agent, the tests tend to rubber-stamp whatever got built. If you write the tests first from the spec, they become an honest definition of done: they check for the behavior the spec promised, not just that the code runs without crashing.

Those failing tests are the baton handed to the implementer. They give the next agent something concrete to push against.

## Implement

For most of my career, this part was the job: pick up a ticket, sit down, and write the code. It is where almost all of my time used to go.

Now an *implementer* agent starts from the approved spec and the failing tests, and it writes code until the tests pass. Because the tests are just the spec made executable, getting the tests to green means building what we agreed to. And because the spec spells out its boundaries, a one-line fix can't quietly grow into a weekend-long refactor.

I am not watching it type. When the agent comes back, the code runs and does what the spec asked. Whether it is *good* code is a question for the next phase.

## Review

The last phase is the one nobody likes to do on their own work: review. A civil engineer doesn't get to sign off on their own drawings, and for good reason. The person who built the thing is the worst person to catch its blind spots.

A separate *reviewer* agent comes in fresh and reads the diff three ways: for correctness, for standards, and for simplification. Then it argues against its own findings and throws out the ones that don't hold up, so a style preference doesn't get reported as a bug. It caps what is left at a few blockers and a few suggestions, because I want a short list of real issues instead of a wall of nitpicks.

Even as a solo developer, this gives me the second set of eyes I would otherwise get from a coworker on a team.

## Ship

The last leg is the one I used to do by hand at the end of a good day: open the pull request, wait around, merge it. baton writes that pull request itself — what changed, what the tests prove, and any decisions it made on my behalf copied in near the top, so `git log` leads back to them. It links the issue, so merging closes the thread.

Then it lands it. By default it merges right there, which is the whole walk-away promise: fire it off, go do something else, come back to a merged main with the pull request as the record. When I want an independent run on a clean machine, I point it at auto-merge instead and CI does the merging once the checks go green. And when I would rather look first, I tell it to leave the pull request open for me.

## Barely anything to install

My favorite part of baton is how little there is to it. There is no binary, no package to install, no background daemon, and no database. The whole thing is markdown: one slash command and a few agent files in my Claude Code config.

```
.claude/
  commands/
    baton.md
  agents/
    baton-code-explorer.md
    baton-spec-writer.md
    baton-spec-critic.md
    baton-test-writer.md
    baton-implementer.md
    baton-reviewer.md
```

If I want to change how a phase behaves, I open its markdown file and edit the prose. That's it.

That is all of it. An earlier version had a zsh script wrapped around the outside to set each run up, and it worked, but it was one more thing to install and keep working on every machine I use. So I moved that job into the workflow itself. A setup phase does it now, from inside whatever session I am already in, in markdown like the rest.

What it sets up is a directory per issue, off to the side and out of my way. Inside is a git worktree, so an agent's branch switching and commits never touch my main checkout and I can have a few issues going at once. Next to it is a log file with one plain line per phase. If a run stalls halfway through, the worktree is still sitting there and the log says exactly where it stopped, so running `/baton 163` again picks up where it left off instead of starting over.

## Where my time goes now

My days feel different now. The energy that used to go into writing code, and then into steering an agent through a chat to write code, goes into the blueprint instead: the goal, the boundaries, the acceptance criteria. The crew handles the rest. I get to spend my time on *what* I am building and *why*, and a lot less on the fiddly *how*.

If any of this sounds useful, [baton is up on GitHub](https://github.com/cbohara/baton). Clone it, fork it, strip it down to the parts you like, and make it your own. I built it to scratch my own itch, but I am sharing it in case it helps someone else. Write the blueprint, let the crew build, and have fun with it!
