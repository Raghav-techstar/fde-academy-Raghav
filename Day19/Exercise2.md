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
