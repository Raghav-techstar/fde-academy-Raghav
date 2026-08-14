# Day 19 - Exercise 1
# 60-Minute Mock Discovery Workshop

## Client

Regional Logistics Operator

## Participants

- Ops Director
- Dispatcher
- IT Lead
- FDE / Facilitator

##################################
# Task 1 - Facilitation Plan
##################################

## Phase 1 - Framing

### Framing Statement

The goal of today's workshop is to understand how shipment delays are currently handled, where the biggest problems occur, and what a better process should look like. I would like to leave the session with a clear current-state process, the main pain points, and a prioritized list of areas that we can take into the next phase.

### Opening Question

"Can you walk me through what normally happens from the moment a shipment starts showing signs of a delay until the customer is informed?"


## Phase 2 - Current State

### Opening Question

"Can you walk me through how your team handles a shipment status or delay question today, step by step?"

### Follow-up Questions

- Which system do you check first?
- What information do you get from each system?
- How do you know when the shipment is actually delayed?
- What happens after you collect the information?
- How long does this normally take?
- Who else needs to be involved?

---

## Phase 3 - Pain Points

### Opening Question

"Looking at that process, where does it normally break down, take too much time, or create problems for the team?"

### Follow-up

"Can you give me an example of the last time that happened?"


## Phase 4 - Future State

### Opening Question

"If we could improve this process, what would an ideal version look like for you?"

### Follow-up

"What information would you want to see immediately without having to search for it?"


## Phase 5 - Prioritization

### Opening Question

"Of all the problems we discussed, which ones have the biggest impact on customers or your team's daily work?"

### Prioritization Criteria

I would rank the issues based on:

- Customer impact
- Frequency
- Time wasted
- Operational impact
- Business risk


## Phase 6 - Close

### Closing Statement

Let me quickly summarize what I heard today. The biggest problems are the lack of early visibility into delays, the time spent checking multiple systems, and the lack of a shared and traceable process. We also identified opportunities to improve the way information reaches the dispatcher and customer.

I will use these findings to create the requirements and backlog for the next phase. Before we close, I would like to confirm whether I missed anything important.


#############################
# Task 2 - Workshop Notes
#############################

## Phase 2 - Current State

### Step-by-Step Process

1. A customer asks for the status of a delayed shipment.
2. The dispatcher checks the TMS for transit information.
3. The dispatcher checks the warehouse inventory system for the physical location.
4. The dispatcher searches email threads for additional warehouse notes.
5. The dispatcher compares the information from all three sources.
6. The dispatcher manually prepares a summary.
7. The dispatcher records the information in a shared spreadsheet.
8. The dispatcher contacts the customer with the current status.
9. If further action is required, the dispatcher coordinates with the warehouse team.


# Phase 3 - Pain Points

## 1. Delays are discovered too late

**Who:** Ops Director

The Ops Director explained that the team often finds out about shipment delays only after the customer calls and is already upset.

## 2. Status checks take too long

**Who:** Dispatcher

The dispatcher explained that answering a status question requires checking three different systems and can take around 10-15 minutes.

## 3. Information is spread across different systems

**Who:** Dispatcher

The dispatcher has to combine information from the TMS, warehouse system, and email threads before giving the customer an answer.

## 4. The systems do not communicate properly

**Who:** IT Lead

The IT Lead explained that the three systems do not currently communicate with each other because a legacy integration was never completed.

## 5. There is no clear audit trail

**Who:** Dispatcher / Operations

The current process does not provide a clear record of who checked the shipment, who made a decision, or what action was taken.

## 6. Different teams may work from different information

**Who:** Dispatcher

The dispatcher has to manually compare information from different sources, which creates a possibility that warehouse and dispatch teams are working from different updates.


# Handling the Ops Director's Assumption

The Ops Director said that the warehouse team "sits on information."

I would not record this as a confirmed fact.

I would ask:

"What makes you think the warehouse is holding the information, and can you walk me through the last example where this happened?"

This keeps the stakeholder's concern but separates the actual pain point from an assumption.


# Technical Detail Discovered

After asking specifically about how the systems communicate, the IT Lead explained that there is a legacy integration that was never completed.

This explains why the dispatcher currently has to manually collect information from multiple systems.


# Phase 4 - Future State

### Desired Process

1. Shipment information from the different systems is available through one unified view.
2. The dispatcher can immediately see the current shipment status and location.
3. The system identifies shipments that have a high risk of delay.
4. The appropriate operations team receives an alert before the customer complains.
5. The dispatcher can take the required action from one place.
6. Customer communication can happen using the latest available information.
7. All important actions are recorded for audit purposes.


# Phase 5 - Prioritized Pain Points

| Rank | Pain Point | Impact |
|---|---|---|
| 1 | Delays discovered only after customer complaints | Very High |
| 2 | Dispatcher checks three systems for every inquiry | Very High |
| 3 | Systems do not share information | High |
| 4 | No clear audit trail | High |
| 5 | Teams can work from different information | Medium-High |


# Phase 6 - Close

### Summary

The main issue is not simply that the dispatcher has to check multiple systems. The bigger problem is that the current process does not give the operations team timely and shared visibility into shipment delays.

The most important improvement would be to provide earlier visibility, reduce manual information gathering, and make important actions traceable.


#################################
# Task 3 - As-Is / To-Be Map
#################################
## AS-IS - Manual Shipment Delay Handling

Customer asks for shipment status
        ->
Dispatcher checks TMS
        ->
Dispatcher checks warehouse system
        ->
Dispatcher checks email threads
        ->
Dispatcher manually compares information
        ->
Dispatcher types summary into spreadsheet
        ->
Dispatcher contacts customer
        ->
Manual follow-up with warehouse if needed

### Main Pain Points

- Delays are often discovered too late.
- Three systems must be checked manually.
- Systems do not communicate properly.
- Information is spread across different places.
- Status information can become inconsistent.
- No complete audit trail.
- Significant dispatcher time is spent on each inquiry.


## TO-BE - Unified Shipment Visibility

Shipment data from source systems
        ->
Unified Shipment view
        ->
Current status and location available
        ->
Delay-risk identification
        ->
Operations alert
        ->
Dispatcher takes action
        ->
Customer receives updated information
        ->
Action recorded in audit history


##########################
# Reflection Questions
##########################

## A1.

No. It required a more specific technical question about how the three systems communicate.

This shows why an FDE should make sure both business and technical stakeholders are heard. The business team explains the symptoms, while the technical team may explain the underlying cause.

## A2.

I treated it as a concern rather than a fact. I would ask for a specific example instead of immediately accepting the statement.

I think this makes the stakeholder feel heard while still keeping the workshop objective and factual.

## A3.

I would avoid completely removing Current State or Pain Points because they are the foundation of the requirements.

If I absolutely had to shorten the workshop, I would combine parts of Framing and Close, and reduce the amount of time spent on Future State.

I would still protect Prioritization because an unranked list of problems is less useful for the next phase.