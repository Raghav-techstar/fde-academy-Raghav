# Exercise 2 — Build a Stakeholder Map for a Manufacturing Plant Deployment


###########################################
## Task 1: Classify the 6 Stakeholders
###########################################

**Stakeholder 1 (Plant Manager): Quadrant = Manage Closely**
Evidence: Owns production targets and has explicit approve/block authority over any change that could slow the line (high influence), and meets with the team weekly (high, sustained interest/engagement). Both influence and interest are high — the textbook Manage Closely profile.

**Stakeholder 2 (Quality Lead): Quadrant = Manage Closely**
Evidence: Directly responsible for defect rates (high interest — the outcome is literally their KPI) and will use the system daily (high interest, hands-on). Has been pushing for this for a year, indicating strong influence over whether the project has organizational backing. High interest and meaningful influence over adoption place this stakeholder alongside the Plant Manager.

**Stakeholder 3 (Plant Director): Quadrant = Keep Satisfied**
Evidence: One level above the Plant Manager, meaning formal authority/influence over the plant's overall numbers is high — they could escalate or override a decision. But rarely attends working sessions, indicating low day-to-day interest in the mechanics of this specific deployment. High influence, low routine interest is exactly Keep Satisfied.

**Stakeholder 4 (Line 3 Operators): Quadrant = Keep Informed**
Evidence: Will directly see alerts on their floor displays every shift — the system changes their daily work, so interest is high. But they were not consulted on the original request and have no approve/block authority over the deployment — low influence. High interest, low influence is Keep Informed.

**Stakeholder 5 (Corporate IT Security): Quadrant = Monitor** *(with a documented escalation trigger — see note below and Reflection Q2)*
Evidence: Must formally approve any new system touching the plant network — this is real influence, since they can block deployment. However, they have no opinion on quality outcomes, meaning day-to-day interest in this specific project is low. This is a borderline case between Keep Satisfied and Monitor; I'm placing it at Monitor by default because their influence here is narrow and gate-like (a one-time approval checkpoint) rather than ongoing decision-making influence over the project's direction.

**Stakeholder 6 (Corporate Data Governance): Quadrant = Monitor**
Evidence: Cares only that sensor data handling meets retention policy, and is explicitly "engaged only if policy is at risk" — both influence over day-to-day project decisions and routine interest are low. Classic Monitor.

*Note on Stakeholder 5: unlike Data Governance, IT Security's approval is a hard gate the project cannot pass without — reasonable teams could argue this pushes them toward Keep Satisfied instead of Monitor. I've kept them at Monitor because their engagement is genuinely episodic (one approval gate, not sustained interest), but flagged this explicitly since it's the placement most likely to be challenged.*


#####################################################
## Task 2: Build the Matched Communication Plan
#####################################################

| Stakeholder | Quadrant | Frequency | Channel | Content |
|---|---|---|---|---|


| Plant Manager | Manage Closely | Weekly | Working meeting | Full status, open decisions, anything that could affect line throughput |


| Quality Lead | Manage Closely | Weekly (same session) | Working meeting | Full status, defect-rate impact, requests for input on alert design |


| Plant Director | Keep Satisfied | Bi-weekly | Email | Concise executive summary: plant-level metrics, risk flags only |


| Line 3 Operators | Keep Informed | Weekly | Floor briefing / Slack | What's changing on their displays, when, and what to do if an alert fires |


| Corp. IT Security | Monitor | As-needed (pre-launch gate + any network/architecture change) | Email | Only what's needed for security review/approval |


| Corp. Data Governance | Monitor | As-needed (only if retention policy is implicated) | Email | Only if sensor data handling or retention approach changes |


Frequency, channel, and content clearly differ by quadrant: the two Manage Closely stakeholders get a shared weekly working session with full detail; Keep Satisfied gets infrequent, summary-only email; Keep Informed gets a lighter-touch but still regular update; both Monitor-quadrant stakeholders get contact only when something in their specific area of concern is actually triggered.


#########################################
## Task 3: Build the Engagement RACI
#########################################

DECISION: 'Approve the sensor-drift alert thresholds'

R (Responsible): Quality Lead -- defines and proposes the specific
 threshold values, since defect detection is their domain expertise
 and daily responsibility.

A (Accountable, exactly ONE): Plant Manager -- ultimately owns
 whether a threshold that could trigger a line slowdown or shutdown
 is acceptable; production impact is their responsibility, so the
 final approval sits with them alone.

C (Consulted): Plant Director (wants visibility into anything that
 could affect plant-level output numbers), Corp. IT Security (only
 if threshold logic changes what data leaves the plant network).

I (Informed): Line 3 Operators (need to know what a triggered alert
 means for them), Corp. Data Governance (only if the underlying
 sensor data being evaluated changes).


###########################
## Reflection Questions
###########################

**A1.
The Plant Director is the clearest example — their title outranks the Plant Manager, but they land in Keep Satisfied rather than Manage Closely, because influence and interest are evaluated separately from seniority. Title alone would suggest "manage the most senior person most closely," but the actual guidance is about influence *and* interest together — the Director has influence but not the sustained, hands-on interest that would justify weekly deep engagement. Rarely attending working sessions is the specific evidence that overrides the seniority assumption.

**A2.
IT Security would jump to Manage Closely if the deployment architecture changed to introduce a new network path, an external data connection, or any component that raises a genuine security concern beyond a one-time approval — for example, if the drift-detection model needed to call an external cloud API instead of staying on the plant's internal network. Data Governance would jump to Manage Closely if the sensor data collection scope expanded to include something retention-policy-sensitive, such as capturing operator identity alongside sensor readings, or if a regulator inquiry made data handling itself the active topic rather than a background concern. In both cases, the trigger is the same pattern: a decision starts directly affecting their specific system or mandate, which converts a low-interest bystander into an actively invested stakeholder.

**A3.
In this case they do match — the Plant Manager is both the RACI's sole Accountable owner and one of the two Manage Closely stakeholders — but if they hadn't matched, that would be a real warning sign worth investigating, not necessarily an automatic error. Mapping RACI against the stakeholder map often reveals a mismatch worth catching early. A mismatch could mean one of two things: either the RACI is wrong (the wrong person was assigned Accountable, and it should be reassigned to whoever the stakeholder map shows actually has decision authority), or the stakeholder map is wrong (someone holds real decision-making authority but was under-classified as Keep Satisfied or Keep Informed, and their quadrant placement needs to be revised upward). Either way, the mismatch itself is the useful signal — it's a checkpoint prompting a second look, not automatically a mistake in one specific document.