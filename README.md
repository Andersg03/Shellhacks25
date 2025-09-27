# Shellhacks25

Great—let’s walk the exact message flow for your scenario (“Python → Beginner → Loops → learn + example problem”), and spell out which parts are parallel (A2A) and which are continuous loops (ADK).
0) UI → Orchestrator (kickoff)
Payload
{ "user_id":"u123", "language":"python", "topic":"loops", "level":"intro" }
Orchestrator does immediately
Maps toolchain: {runner: python3, lint: pylint, filters: {language:python, topic:loops}}
Creates session_id and context_id (shared across agents)
Fetches user’s prior_failures for loops (if any)
1) Parallel fan-out (A2A) — the swarm “builds the lesson”
All of these start at the same time, using the same context_id and retrieval snippets.
1.1 Retrieval Agent (fast)
Pulls 2–3 authoritative snippets (Python tutorial: for, range) with source URLs
Broadcasts retrieved_snippets to all agents
1.2 Curriculum Planner
Input: {language: python, topic: loops, level: intro, prior_failures: []}
Output: sub_concepts = ["for-range inclusive pattern", "off-by-one risk"]
Sends to Orchestrator
1.3 Example Synthesizer
Input: sub_concepts + snippets
Output:
explanation_md (≤120 words, grounded in snippets)
demo_snippet (runnable for i in range(1, n+1))
1 canonical example + 1 counterexample
Sends to Orchestrator
1.4 Test Author
Input: sub_concepts + constraints ("use for-loop")
Output: tests JSON (runner=python3, stdout cases), edge-cases (n=1, n=0)
Sends to Orchestrator
1.5 Hint Writer
Input: tests + common_errors["off-by-one","wrong range bounds"]
Output: Tiered hints aligned to failing test names
Sends to Orchestrator
1.6 Static Analyst (pre-compute)
Input: starter_code skeleton + known wrong patterns
Output: static_feedback_rules (detect starts-at-0, prints odd numbers, etc.)
Sends to Orchestrator
1.7 Critic / Verifier (adversarial QA)
Pulls everything as it arrives; runs checks:
Do tests fail on “Trickster” wrong solutions?
Are constraints enforceable (no list comps)?
Is explainer consistent with citations?
If gaps found, pings the responsible agent to patch, then rechecks.
Output: verified=true (or reasons + diffs)
Orchestrator reduce step
Waits for all required parts (Planner, Example, Tests, Hints, Critic ✅)
Merges to a single LessonBundle and caches it under {language, topic, level}
Returns LessonBundle to UI/Teaching Agent
2) Teaching phase (front-facing Teaching Agent)
What it does
Renders the explanation_md, demo_snippet, and the exercise with starter_code
Offers Run (demo) and Run Tests (on user submission)
Shows Sources (citations from Retrieval Agent)
3) Evaluation on submit — small parallel pass
User submits code → Orchestrator invokes two fast paths in parallel:
3.1 Test Runner
Executes tests.cases against user code in a Python sandbox
Output: pass/fail per case + stdout diffs
3.2 Static Analyst
Lints/regexes user code
Output: targeted feedback (“Loop starts at 0; spec is 1..n”)
Orchestrator combines results → sends to Teaching Agent:
If all pass → award stars/XP; proceed to loop updates
If fail → Teaching Agent offers Hint 1; on another fail, Hint 2, etc.
4) Continuous loops (ADK) — always-on adaptation
4.A Mastery Loop (trigger: every submission)
Updates per-concept mastery (e.g., loops.inclusive_range +=)
Schedules a review chip (spaced repetition) for 24h
Logs hint usage, TTFC, error tags
4.B Weakness Miner (periodic: hourly/daily)
Clusters this user’s mistakes (and cohort’s) → e.g., “off-by-one”, “forgot ValueError”
Requests a targeted micro-drill from Planner + Test Author (A2A fan-out) and queues it as the next “Practice” card
4.C Freshen Loop (daily)
Rotates names/themes/examples for this lesson (avoid memorization)
Re-verifies cached LessonBundles with Critic if sources changed
5) State machine snapshot (your backend logic)
SESSION_INIT
  → PREP_LESSON (A2A parallel build)
    → LESSON_READY
      → SUBMIT → { TEST_RUNNER || STATIC_ANALYST } (parallel)
        → FEEDBACK
          → {RETRY | ADVANCE}
            → MASTERY_LOOP (schedule review)
6) What happens on common edge cases
Tests flake: Critic rejects; Orchestrator falls back to a known-good cached bundle.
User code times out: Runner returns “Time limit”; Teaching Agent suggests complexity hint; Mastery still updates.
Retrieval empty: Planner uses seed fundamentals JSON; cites seed pages.
7) Why this is efficient & convincing
Parallelism cuts “lesson compile time” (examples, tests, hints, QA) from sequential seconds → overlapping seconds. Judges can see this in a swarm log view.
Loops prove it’s not a one-shot tutor: the system learns the learner and keeps pushing targeted drills and reviews.
