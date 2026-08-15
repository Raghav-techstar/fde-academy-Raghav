# Exercise 3 — Present Your Problem Frame and Defend Your Prioritization


######################################################
## Task 1: Generate and Plot Solution Candidates
######################################################

HOW MIGHT WE: How might we ensure every shipment is staged and ready
 before its specific carrier pickup deadline, regardless of when the
 order was originally created?

Candidate 1: Add a "carrier pickup deadline" field to the WMS and
 re-sort the picking/staging queue by deadline instead of order
 creation time.
Quadrant: Major Project
Why: High impact -- directly closes the identified root cause for
 every shipment, permanently. High effort -- requires a WMS data
 model change, workflow logic change, and testing against live
 operations.

Candidate 2: Create a manual "urgent lane" where staging staff flag
 and prioritize shipments with tight carrier windows by eye, using a
 shared spreadsheet updated each morning.
Quadrant: Quick Win
Why: Moderate impact -- catches the most visible cases quickly and
 stops the immediate bleeding. Low effort -- no system change, just
 a new manual process staff can adopt within days.

Candidate 3: Add a "rush" button warehouse staff can press to bump a
 single shipment to the front of the physical staging queue.
Quadrant: Fill-In
Why: Low impact -- solves one shipment at a time reactively rather
 than preventing the problem systematically, and doesn't scale as
 volume grows. Low effort -- a small UI/process addition, not a
 deadline-aware redesign.

Candidate 4: Replace the entire WMS with a new platform that has
 deadline-aware prioritization built in natively.
Quadrant: Thankless Task
Why: High effort -- a full platform migration, months of work,
 major operational risk. Doesn't address the root cause any better
 than Candidate 1 does, since the actual gap is a missing
 deadline-aware sort in the existing system, not a fundamentally
 broken platform -- so most of that effort buys nothing extra.

Recommended build order: Candidate 2 first (Quick Win), then
 Candidate 1 (Major Project). The manual urgent lane stops the
 immediate delivery-rate bleeding within days and builds
 stakeholder trust and evidence that deadline-based prioritization
 works, which then supports the case for investing in the proper
 WMS fix. Candidate 3 is worth keeping as a lightweight fallback
 but not prioritizing. Candidate 4 should be explicitly deprioritized
 and named as such if a stakeholder proposes it.


##################################################
## Task 2: Prepare the 5-Minute Presentation
##################################################

0:00-0:30  Conclusion: Recommend building a manual "urgent lane"
 staging process this week as a Quick Win, then investing in a
 WMS deadline-field change as the Major Project that permanently
 fixes on-time delivery.

0:30-2:00  How I got there: Carrier on-time delivery dropped 12%
 this quarter. Running the 5 Whys traced this past "staff moving
 slowly" to the real root cause -- the staging queue has no way to
 prioritize by carrier pickup deadline, a gap that opened up when
 carrier contracts changed eight months ago and the WMS was never
 updated to match. That reframes as: how might we ensure every
 shipment is staged before its deadline, regardless of when the
 order was created?

2:00-3:30  Why THIS solution first: Plotted four candidates on the
 Impact/Effort Matrix. The urgent lane is a Quick Win -- low effort,
 meaningful impact -- so it ships first to stop the immediate
 problem and earn trust. The WMS deadline field is the Major
 Project that actually closes the root cause permanently, but it
 needs proper scoping, so it's sequenced second, not skipped.

3:30-4:30  What I'm NOT doing yet, and why: Not proposing a full WMS
 replacement -- it's high effort and doesn't address the actual root
 cause any better than a targeted deadline-field change would.
 Also holding off on the "rush button" idea -- it's a reasonable
 Fill-In but doesn't scale, so it's not worth prioritizing ahead of
 the two solutions above.

4:30-5:00  Open for questions.

##############################################################
## Task 3: Present and Defend Live — Prepared Responses
##############################################################

*(Deliver live to a partner; responses below are prepared for each possible challenge question, so you're ready regardless of which one they pick.)*

**Challenge: "Why not just do what I originally asked for?"**
> "The original ask was framed as 'staff need to work faster.' When I ran the 5 Whys on the actual on-time delivery drop, it traced past staff speed entirely — the real gap is that the staging queue has no concept of a carrier pickup deadline, which became a problem specifically after the carrier contracts changed eight months ago. Asking staff to move faster wouldn't fix that; they'd still be working from a queue that doesn't know which shipments are actually urgent. The urgent-lane and WMS-deadline fixes both target that gap directly."

**Challenge: "This seems like a lot of effort for something so small — why prioritize it first?"**
> "I'm actually not prioritizing the big-effort option first. The Impact/Effort Matrix put the manual urgent lane — low effort, real impact — as the first thing to ship, specifically because it's small. The WMS deadline-field change is the higher-effort Major Project, and it's sequenced second on purpose, once the Quick Win has already proven the approach works."

**Challenge: "How do you know this is the REAL problem and not just what people happened to complain about?"**
> "The complaint I started from was the 12% drop in on-time delivery — that's the symptom, not something I'm treating as the root cause. I traced it through five whys to a specific, dated, verifiable event: the carrier contracts changed eight months ago to add pickup-window penalties, and the staging process was never updated to reflect that. That's a concrete process gap I can point to, not just 'what people happened to complain about.'"

**Challenge: "What if [a specific stakeholder] disagrees with this priority?"**
> "Then I'd want to understand whether they're disagreeing with the root cause itself or with the build order. If it's the root cause, I'd walk them through the 5 Whys chain and ask which specific link they think is wrong — the framework is there so the disagreement is about evidence, not opinion. If it's the build order, I'd want to know what's actually non-negotiable for them, separating positions from underlying interests, and see if the sequence can accommodate both without abandoning the Quick-Win-first logic."

**SELF-SCORE:**
- Did you trace back to the 5 Whys / Impact-Effort framework, rather than restating your opinion? **Yes** — every prepared response above points to a specific artifact (the whys chain, the matrix placement, a dated event) rather than asserting "trust me, this is right."
- Did you stay calm and non-defensive? **Yes** (self-assessed from the prepared responses; confirm this holds in the actual live delivery, since script and delivery can diverge under real-time pressure — this is the one item worth re-checking honestly after the actual session, not just the plan).


###########################
## Reflection Questions
###########################

**A1.
"Why not just do what I originally asked for?" is the hardest in practice, because it can land as a direct challenge to the stakeholder's own judgment — they're the one who made the original ask, and explaining that it wouldn't have worked risks sounding like "you were wrong." What makes it answerable calmly is keeping the explanation entirely about the evidence trail (the 5 Whys chain) rather than about their original framing being mistaken — the goal is to make the *root cause* the subject of the sentence, not their original request.

**A2.
If the framework held, the right next step is simply to note that the challenge validated the existing work — no changes needed, just confirmation. If a genuine gap surfaced (for example, a partner asks about a candidate solution or stakeholder that wasn't considered at all), the right next step is different: go back to Exercise 1 or 2 and actually extend the analysis — add the missing candidate to the Impact/Effort Matrix, or add the missing stakeholder to the map — rather than only improving how the answer is delivered next time. The difference matters because one is a presentation-skill fix and the other is a content fix; treating a content gap as just a delivery problem means the same gap resurfaces with the next stakeholder who asks.

**A3.
For the Plant Manager alone, the presentation would compress the "how I got there" section and spend more time on production-line impact specifically — since that's their direct concern (Manage Closely, weekly working sessions, approve/block authority over anything that could slow the line). For the full panel including the Plant Director, Quality Lead, and others, the presentation would need to hold more ground simultaneously: keep the Impact/Effort reasoning intact for the Quality Lead's benefit, add a brief plant-level-metrics framing for the Director's Keep Satisfied profile, and be ready for IT Security or Data Governance to ask about their specific concern even though they're Monitor-quadrant stakeholders who weren't expected to be deeply engaged day-to-day. In short: single-stakeholder audiences let the presentation go deep on one axis; a mixed panel requires touching every stakeholder's specific "why this matters to me" without letting the core Pyramid Principle structure (recommendation first) get lost.