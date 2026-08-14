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
