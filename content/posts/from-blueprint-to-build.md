---
title: "From Blueprint to Build"
date: 2026-06-26
excerpt: "How I stopped writing code at the keyboard and started writing blueprints instead — and the handful of markdown files I rigged up to run the rest: baton."
---

For a while now I've wanted to hand a whole task off to an AI agent and just walk away. Describe what I want, go get a coffee, come back to working code. I had a hunch we weren't quite there yet. But I also had a hunch we were a lot closer than my copilot-style, back-and-forth chatting was letting me get.

The thing that nudged me forward was a blog post a coworker shared, [The 8 Levels of Agentic Engineering](https://www.bassimeledath.com/blog/levels-of-agentic-engineering). It lays out a staircase, from chatting with an assistant at the bottom all the way up to systems where agents do the work on their own. It was a great map. The trouble was that it stayed a map. I could see where I wanted to go, but I couldn't picture the actual steps.

It clicked when I read an O'Reilly piece, [How to Write a Good Spec for AI Agents](https://www.oreilly.com/radar/how-to-write-a-good-spec-for-ai-agents/). The idea is simple. Just like an architect hands a builder a blueprint, the most useful thing I can do for an agent is hand it a spec. Write the plan clearly enough, and the agent can build from it.

## The blueprint decides what gets built

I grew up around blueprints. My dad built homes, and my husband is a civil engineer. So I've spent a lot of my life around people whose whole job is to get the plan right before anyone picks up a tool. They'll tell you the quality of the house is decided long before the foundation is poured. A great crew working off a bad blueprint just gives you a really well-built mistake.

For most of my career, software hasn't worked that way. Depending on the team and the deadline, there might be some architecture work up front. But the actual task? That mostly got figured out at the keyboard, one decision at a time, while I was already typing.

That made sense when I was the one writing every line. It makes a lot less sense now. When an agent is doing the typing, the quality of what I get back isn't set by how well I write code. It's set by how well I describe what I want. The blueprint is back to being the thing that matters most.

## The workflow

So I built it. There's barely anything to install, which I'll get to in a bit. But the part worth keeping was never the code anyway. It's the shape: the same four steps every time, spec, tests, implement, review. (I've started calling it STIR.) `baton` is just my own take on that shape, one slash command and a few agent files, all markdown, sitting in my Claude Code setup. I run a version at work too, wired up a little differently for my team and the tools there. You point baton at a GitHub issue and it takes that issue from an approved plan all the way to a pull request worth reviewing:

```
/baton 163

Spec → Tests → Implement → Review
```

A baton is the thing that gets passed from one hand to the next, and that's the whole idea. Each phase does its piece and hands the work to the phase after it. The spec hands off to the tests, the tests to the implementer, the implementer to the reviewer. (A baton is also what a conductor uses to keep a room full of specialists in time without playing a single note, which turns out to be about right.)

Because here's the one rule that makes the whole thing work: `baton` never writes a line of code itself. Think of it like a general contractor. Growing up, my dad didn't pour every foundation or hang every door. He ran the crew and made sure the house matched the plans. `baton` does that for an issue. It runs a crew of agents, brings in each one at the right moment, and holds all of them to the same spec.

This is where the name earns its keep. Each phase runs as its own agent with a fresh, clean context, and the only thing that passes from one to the next is the baton: the work itself, not the whole conversation. Hand one agent the entire job and it starts agreeing with itself. It writes the code, then writes tests that bless the code it just wrote, then reviews its own work and finds it excellent. You can watch the quality slide as one long conversation fills up with its own assumptions. Passing a clean baton between separate agents is what keeps everyone honest.

Let me walk through each phase, starting where every build starts: the plan.

## Spec

The spec is where my energy goes now, but I don't write it from a blank page. The phase actually starts with a different agent: before the *spec-writer* writes a word, a *code-explorer* goes and reads the actual code and hands back a short map of the files the task really touches.

That step matters more than it sounds. An issue describes the behavior I want. It doesn't describe the handful of files that behavior actually touches. Letting an agent trace the real code first means the plan reflects the system that's actually there, not the one I imagined when I wrote the issue. The map is what the spec-writer builds its boundaries and implementation plan on.

Every spec comes back in the same shape:

- **Goal** — the problem, and who it's for.
- **Acceptance criteria** — numbered, testable, and observable. Each one maps to a test.
- **Boundaries** — the files the agent may touch, and the ones it must not.
- **Implementation** — one line per file describing what changes. No code, just intent.
- **Tests** — a short table: each test, what it proves, and whether the file is new or already exists.

Then the spec-writer stops and waits. Nothing moves until I read it and type `yes`. I'm not reading it for syntax. I'm reading it for intent: right problem, right boundaries. I either approve it or send it back with notes. Once I approve it, that spec stops being a document and becomes a contract. Every phase after this answers to it.

## Tests

Test-driven development is one of those things I learned early, nodded along to, and then never once saw a team actually do in the wild. Agents are what finally made it real for me.

A *test-writer* agent turns each acceptance criterion into a failing test, before any implementation exists. The order is the whole point. If you build first and test second, especially with the same agent, the tests just rubber-stamp whatever got built. Write the tests first, from the spec, and they become an honest definition of done. They check for the real behavior the spec promised, not just that the code ran without crashing.

Those failing tests are the baton handed to the implementer. They're the backpressure. They give the next agent something concrete to push against.

## Implement

This is the part that, for most of my career, was the job. Pick up a ticket, sit down, write the code. It's where almost all my time used to go.

Now the *implementer* agent starts from the approved spec and the failing tests and writes code until the tests pass. Because the tests are just the spec made executable, "get the tests to green" is the same thing as "build what we agreed to." And because the spec spelled out its boundaries, a one-line fix can't quietly sprawl into a weekend-long refactor.

I'm not watching it type. The tests are the guardrails, the spec is the map, and when the agent comes back the code runs and does what the spec asked. Whether it's *good* code is a separate question. That's the next phase's job.

## Review

The last phase is the one nobody likes to do on their own work: review. Same reason a civil engineer doesn't get to sign off on their own drawings. The person who wrote the thing is the worst person to catch its blind spots.

So a separate *reviewer* agent comes in fresh and reads the diff three ways: for standards, for correctness, and for simplification. Then it turns adversarial and argues against its own findings, throwing out the ones that don't hold up — taste dressed up as a defect doesn't survive. What's left it caps at a few blockers and a few suggestions, because I want signal, not a wall of nitpicks. The review checks the diff against the spec, and when I can, I run it on a different model than the one that wrote the code. A reviewer from a different background catches more than an author grading their own homework, and the same model tends to be blind to the same kinds of bugs it writes.

Even as a solo developer, this is the second set of eyes I'd otherwise get from a coworker on a team.

## How little there is to it

The part I'm most pleased with is how little there is. No binary, no package to install, no background daemon, no database. The whole thing is markdown: one slash command and a few agent files in my Claude Code config.

```
.claude/
  commands/
    baton.md                 # the slash command that runs the phases
  agents/
    baton-code-explorer.md
    baton-spec-writer.md
    baton-test-writer.md
    baton-implementer.md
    baton-reviewer.md
    baton-qa-browser.md      # web apps only
```

If I want to change how a phase behaves, I open its file and edit the prose. That's it. There's no clever machinery to keep in my head, which is the only reason I'll still understand this in six months.

A couple of small habits keep separate runs from stepping on each other. Each issue gets its own git worktree off to the side, so an agent's branch switches and commits never touch my main checkout, and I can kick off a few at once. Each background run streams its progress to a plain log on disk, and if one stalls partway through it leaves its worktree sitting there, so I can open it up and pick up where it stopped instead of starting over. No state lives anywhere I can't just open and read.

## Where my time goes now

The honest result of all this is that my days feel different. The energy that used to go into writing code, and then into steering an agent through a chat to write code, goes into the blueprint instead. The goal, the boundaries, the acceptance criteria. The crew handles the rest.

What that buys me is simple. I get to spend my time on *what* I'm building and *why*, and a lot less on the fiddly *how*.

If any of this sounds useful, `baton` is up on GitHub. Clone it, fork it, strip it down to the parts you like, and make it your own. I built it to scratch my own itch, but I'm sharing it in case it helps someone else who has seen the staircase and wasn't sure how to take the first step.

Write the blueprint, and let the crew build. Have fun with it.
