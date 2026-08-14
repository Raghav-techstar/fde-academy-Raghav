# Day 19 - Exercise 2
# Convert Workshop Outputs into 10 User Stories

########################################################
# Task 1 - Translate Pain Points into Requirements
########################################################

## Pain Point 1

### Pain Point

"We never know a shipment is late until the customer calls angry."

### Diagnosis

The operations team needs earlier visibility into shipments that are likely to be delayed so they can act before the customer complains.

### Requirement

The system should calculate a delay-risk score for active shipments using available historical shipment information and make high-risk shipments visible to the operations team.


## Pain Point 2

### Pain Point

"Checking status takes 10-15 minutes because I check 3 systems."

### Diagnosis

The dispatcher needs a single place to access the shipment information currently spread across multiple systems.

### Requirement

The system should provide a unified shipment view containing the relevant status and location information currently available in the TMS, warehouse system, and other supporting sources.


## Pain Point 3

### Pain Point

"There's no record of who approved rerouting a shipment."

### Diagnosis

The operations team needs traceability for important shipment decisions.

### Requirement

Every shipment rerouting action should record who performed or approved the action, when it happened, and the resulting shipment status.


################################
# Task 2 - 10 User Stories
################################

## Story 1

As an operations dispatcher,

I want to see a delay-risk score on every active shipment,

so that I can proactively reroute or notify customers before they escalate to support.


## Story 2

As an operations dispatcher,

I want to see the current shipment status and location in one view,

so that I can answer customer questions without checking multiple systems.


## Story 3

As an operations dispatcher,

I want high-risk shipments to be clearly highlighted,

so that I can focus on the shipments that need attention first.


## Story 4

As an operations director,

I want to see a list of delayed and high-risk shipments,

so that I can understand where the biggest operational problems are.


## Story 5

As an operations director,

I want shipment actions to have an audit history,

so that I can understand who made important operational decisions.


## Story 6

As a warehouse staff member,

I want the latest shipment information to be visible to dispatch,

so that both teams work from the same information.


## Story 7

As a warehouse staff member,

I want to see which shipments require an operational follow-up,

so that I can prioritize the shipments that need my attention.


## Story 8

As an IT lead,

I want shipment information from the connected systems to be synchronized,

so that dispatchers do not have to manually collect the same information from different systems.


## Story 9

As an operations dispatcher,

I want to record a rerouting decision against the shipment,

so that the reason and outcome of the decision can be traced later.


## Story 10

As an operations director,

I want to see historical carrier performance,

so that I can identify carriers that consistently create delivery problems.


##################################
# Task 3 - Acceptance Criteria
##################################

## Story 1

### Story

As an operations dispatcher, I want to see a delay-risk score on every active shipment, so that I can proactively reroute or notify customers before they escalate to support.

### Acceptance Criteria

1. GIVEN a shipment is currently in transit,
   WHEN a delay-risk score is available,
   THEN the score is displayed on the shipment record.

2. GIVEN a shipment has a delay-risk score above the configured threshold,
   WHEN the dispatcher opens the active shipment list,
   THEN the shipment is clearly highlighted as high risk.


## Story 2

### Story

As an operations dispatcher, I want to see the current shipment status and location in one view, so that I can answer customer questions without checking multiple systems.

### Acceptance Criteria

1. GIVEN a dispatcher opens a shipment,
   WHEN the shipment information is available,
   THEN the current status and location are displayed together.

2. GIVEN information from the connected systems has been updated,
   WHEN the unified shipment view refreshes,
   THEN the latest available status and location are displayed.


## Story 5

### Story

As an operations director, I want shipment actions to have an audit history, so that I can understand who made important operational decisions.

### Acceptance Criteria

1. GIVEN a user performs a shipment action,
   WHEN the action is completed,
   THEN the system records the user and timestamp.

2. GIVEN an operations director opens the shipment history,
   WHEN an action has previously been performed,
   THEN the action and responsible user are visible.


## Story 6

### Story

As a warehouse staff member, I want the latest shipment information to be visible to dispatch, so that both teams work from the same information.

### Acceptance Criteria

1. GIVEN warehouse shipment information has been updated,
   WHEN dispatch views the shipment,
   THEN the latest available warehouse information is displayed.

2. GIVEN the warehouse information is unavailable,
   WHEN dispatch views the shipment,
   THEN the system clearly indicates that the information could not be refreshed.


## Story 10

### Story

As an operations director, I want to see historical carrier performance, so that I can identify carriers that consistently create delivery problems.

### Acceptance Criteria

1. GIVEN historical shipment data exists for multiple carriers,
   WHEN the operations director views carrier performance,
   THEN performance information is grouped by carrier.

2. GIVEN enough historical shipment data exists,
   WHEN the carrier performance view is generated,
   THEN the director can compare carrier performance over time.

############################
# Reflection Questions
############################

## A1.

I would build Story 2 first: the unified shipment view.

The current problem is that dispatchers spend 10-15 minutes checking multiple systems for one status inquiry. Solving that gives an immediate operational benefit and also creates a foundation for several other features.

This is similar to the prioritization phase of the workshop because I am considering both impact and frequency rather than simply choosing the most technically interesting feature.

## A2.

Story 10 was the hardest because "carrier performance" can mean many things.

It made me realize that the requirement would need more clarification around what performance metrics should be used, what historical period matters, and how much data is needed before the comparison becomes useful.

## A3.

That would show that the workshop did not explore financial impact deeply enough.

We discussed operational time, delays, customer impact, and system problems, but we did not ask enough questions about the financial cost of delayed shipments, manual work, rerouting, or poor carrier performance.

I would add cost-related questions to the next discovery session.