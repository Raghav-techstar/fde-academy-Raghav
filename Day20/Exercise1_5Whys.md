# Exercise 1 — Apply 5 Whys to a Real Operational Problem


###############################################
## Task 1: Select and State Your Problem
###############################################

**My chosen problem:**
Carrier on-time delivery rate has dropped 12% over the last quarter (from 94% to 82%).

This is specific and numeric — it names a measurable metric, a direction, a magnitude, and a timeframe, rather than a vague "delivery performance isn't great."


#########################################
## Task 2: Run the Full 5 Whys Chain
#########################################


PROBLEM: Carrier on-time delivery rate has dropped 12% over the last quarter.

Why? -> Because a growing share of shipments are missing their carrier
 pickup window at the warehouse.

Why? -> Because the warehouse team is frequently staging shipments late,
 after the carrier's scheduled pickup time has already passed.

Why? -> Because the picking and staging queue is prioritized by order
 creation time, not by each shipment's carrier pickup deadline --
 so time-sensitive shipments compete equally with non-urgent ones.

Why? -> Because the warehouse management system has no concept of a
 "pickup deadline" field at all -- it was never modeled when the
 WMS was implemented, since the original carrier contracts didn't
 have strict pickup windows.

Why? -> Because nobody re-evaluated the WMS's queue-prioritization logic
 after the company renegotiated carrier contracts eight months ago
 to include penalty clauses for missed pickup windows -- the
 operational process was never updated to match the new contract
 terms.

ROOT CAUSE: The warehouse's shipment-staging process has no way to
 prioritize by carrier pickup deadline, because that requirement was
 never incorporated into the WMS or picking workflow after the carrier
 contracts changed eight months ago -- not "warehouse staff are
 working too slowly" (the original surface-level explanation).


#######################################
## Task 3: Reframe as How Might We
#######################################

**HOW MIGHT WE:** How might we ensure every shipment is staged and ready before its specific carrier pickup deadline, regardless of when the order was originally created?

**SELF-CHECK:**

- **Names an outcome, not a mechanism?** Yes — "staged and ready before its pickup deadline" is the outcome. It doesn't presuppose a specific fix like "add a deadline column to the WMS" or "hire more staging staff"; multiple mechanisms could achieve it.
- **Could 3 different teams propose 3 different valid answers?** Yes — a WMS/engineering team might propose adding a deadline field and re-sorting the picking queue; an operations team might propose a dedicated "urgent lane" staging process; a carrier-relations team might propose renegotiating pickup windows to align with existing staging patterns. All three are legitimate, different answers.
- **Still tied to the Task 2 root cause, not a tangent?** Yes — it stays anchored to the actual root cause (no deadline-aware prioritization in staging), rather than drifting toward something adjacent like "how might we reduce overall warehouse headcount costs," which would be solving a different problem.

###########################
## Reflection Questions
###########################

**A1.
The gap is large. The Task 1 statement ("on-time delivery dropped 12%") is a downstream, customer-facing symptom. The root cause is an internal process/systems gap — a WMS that was never updated to reflect new contract terms. Someone looking only at the surface symptom would likely conclude "carriers are unreliable" or "warehouse staff need to move faster," both of which point at the wrong target entirely. The size of that gap suggests this problem was genuinely easy to misdiagnose — the visible symptom (late deliveries) and the actual cause (a stale system configuration from a contract change) live in completely different parts of the organization, so nobody naturally connects them without deliberately tracing the chain.

**A2.
The third "why" — landing on "the WMS has no concept of a pickup deadline field at all" — was tempting to stop at, because it's an easy, satisfying-sounding technical explanation ("the system just doesn't support this"). It would have been simple to write that off as an unfalsifiable limitation ("that's just how the WMS works") rather than pushing one level further to ask *why* that gap was never closed. What kept me going was the Section 3 guidance that a real root cause has to be something the organization can act on — "the system doesn't support it" isn't actionable on its own, but "nobody updated the process after the contract changed" is, because it points to a concrete, fixable ownership/process gap.

**A3.
I'd point to the timing correlation surfaced in the fourth and fifth "whys": the carrier contracts changed eight months ago to add pickup-window penalty clauses, and the staging process was never updated to reflect that change. If the problem were really about staff working too slowly in general, the on-time rate would likely have been degrading gradually and continuously, not specifically tracking a contract change that introduced a new deadline concept the WMS doesn't model. That specific, dated event is concrete evidence a "staff speed" explanation can't account for.