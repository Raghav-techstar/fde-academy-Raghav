# Day 19 - Exercise 3
# Current-State Data Flow and Automation Opportunities

################################
# Task 1 - Data-Level Flow
################################

## Current Data Flow

[TMS: Transit Status]
        |
        | MANUAL
        v
[Dispatcher reads status]
        |
        |
[Warehouse System: Physical Location]
        |
        | MANUAL
        v
[Dispatcher reads location]
        |
        |
[Email Threads: Warehouse Notes]
        |
        | MANUAL
        v
[Dispatcher reads manual notes]
        |
        v
[Dispatcher compares information]
        |
        | MANUAL
        v
[Shared Spreadsheet: Shipment Summary]
        |
        | MANUAL
        v
[Customer Phone Call]


## Detailed Flow

### Step 1

The TMS contains the shipment transit status.

**Flow:** TMS → Dispatcher

**Type:** Manual

The dispatcher manually opens the TMS and reads the shipment status.


### Step 2

The warehouse system contains the physical shipment location.

**Flow:** Warehouse System → Dispatcher

**Type:** Manual

The dispatcher manually checks the warehouse system.


### Step 3

Additional warehouse information exists inside email threads.

**Flow:** Email → Dispatcher

**Type:** Manual

The dispatcher searches through email threads to find additional notes.


### Step 4

The dispatcher combines information from the three sources.

**Flow:** Dispatcher → Shared Spreadsheet

**Type:** Manual

The dispatcher manually types the combined information into a spreadsheet.


### Step 5

The dispatcher uses the collected information to contact the customer.

**Flow:** Spreadsheet / Dispatcher → Customer

**Type:** Manual

The dispatcher manually communicates the shipment status to the customer.


# Manual Arrow Count

There are five main manual handoffs in the current process:

1. TMS → Dispatcher
2. Warehouse System → Dispatcher
3. Email → Dispatcher
4. Dispatcher → Shared Spreadsheet
5. Dispatcher → Customer


#####################################
# Task 2 - Classify Manual Steps
#####################################

| Manual Step | Signal Category | Automation Opportunity |
|---|---|---|


| Dispatcher checks TMS | Data retrieval / copying information | Direct integration with TMS through Pipeline Builder or another system connector |


| Dispatcher checks warehouse system | Data retrieval / copying information | Integrate warehouse data into the unified shipment view |


| Dispatcher searches email threads | Manual information gathering | Capture structured warehouse updates in a connected system instead of relying on email |


| Dispatcher combines information into spreadsheet | Pure data copying | Pipeline Builder / direct integration to create a unified shipment record |


| Dispatcher prepares and sends customer status update | Status communication | Automated notification triggered by a shipment status change |


# Highest-Value Automation Opportunities

## 1. Unified Shipment Data

The strongest opportunity is connecting the TMS and warehouse system so that dispatchers no longer have to manually check both.

This directly addresses the 10-15 minute lookup problem.

## 2. Automated Delay Notification

If a shipment crosses a delay-risk threshold, the operations team could receive an automated notification.

This addresses the problem of finding out about delays only after customers complain.

## 3. Automated Customer Status Updates

For appropriate shipment status changes, notifications could be generated automatically rather than requiring the dispatcher to prepare every update manually.


##########################################
# Task 3 - What Should Stay Manual?
##########################################

## Step That Should Stay Manual

Final decisions on rerouting a shipment in unusual or high-impact situations should remain manual.

## Why

A rerouting decision may involve several factors that are not always captured cleanly in structured data.

For example, a shipment could be delayed, but the dispatcher may know about a customer commitment, special handling requirement, operational restriction, or other situation that changes what the best action should be.

A rule or model can provide recommendations, but I would not fully automate the final decision for ambiguous or high-impact cases.

## What Could Still Be Improved

The human decision-maker should still get better information.

For example, the system could show:

- Current shipment status
- Current physical location
- Delay-risk score
- Carrier information
- Relevant shipment history
- Available rerouting options
- Previous actions taken

The dispatcher would then make the final decision with better information.

############################
# Reflection Questions
############################

## 1.

Most of the opportunities are rules-based or integration/pipeline work.

The biggest category in this scenario is direct data integration because the dispatcher is mainly copying information between systems.

There is also an ML opportunity for delay-risk scoring and potentially a rules-based trigger for notifying the operations team.

This makes sense for logistics because there is a lot of repetitive data movement and status monitoring.

## 2.

I would build the unified shipment view first.

The dispatcher currently spends 10-15 minutes checking multiple systems for a single inquiry. Removing that repeated manual work would provide a clear benefit.

If the client's priority were customer satisfaction, I would consider automated delay notifications very highly because they help the team act before the customer complains.

If the priority were cost reduction, I would prioritize the unified data integration because it directly reduces repetitive manual work.

## A3.

The process map showed that the dispatcher checks multiple systems, but the data-level map made the actual problem clearer.

It showed exactly where the information lives and where humans have to manually move or copy it.

It also showed that the problem is not only the number of steps. The bigger issue is that the systems are disconnected, which creates repeated manual handoffs.

That makes the automation opportunity much clearer.