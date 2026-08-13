# Day 18 - Exercise 2
# Role-Play: Explain a Pipeline Failure to a Non-Technical CFO

##########################################
## Task 1 - Prepare Your Translation
##########################################

### Technical Fact

The overnight sales data load failed because an upstream system changed the information it was sending.

### Business Impact

No incorrect or corrupted financial data reached the dashboards, but the reports are currently one day behind.

### Recommended Action

No action is needed from the CFO or finance team right now. The team will deploy the fix within the hour and reload the missing sales data.


#######################################
## Task 2 - 90-Second Explanation
#######################################

The good news is that no incorrect financial data reached the dashboards. The overnight sales update failed before it could write anything, so the reports are simply showing data from the previous day.

We found the cause and have a fix ready. We expect to deploy it within the next hour and then reload last night's sales data.

There is no action needed from your team right now. The only impact is that the dashboard is currently one day behind. We will provide an update once the missing data has been loaded.

### Possible Follow-Up Question

**CFO:** Should I be worried about this happening again?

**Answer:** We have identified the cause and are fixing it. We will also monitor the next load to make sure the data is updated correctly.


#######################################################
## Task 3 - Self-Audit Against the Forbidden List
#######################################################

| Forbidden Pattern | Did it appear? | Evidence |
|---|---|---|

| Stack traces / error codes / jargon | No | I avoided technical terms and explained the issue in business language. |


| Minimizing language | No | I clearly explained the impact without calling it a small or minor issue. |


| Blame | No | I described the upstream change without blaming the client's system. |


| Silence about the fix/timeline | No | I clearly explained that the fix would be deployed within the hour. |


##########################
# Reflection Questions
##########################

## 1. Which forbidden pattern were you most likely to slip into under live pressure?

I was most likely to use technical terms because I am used to explaining problems from a developer's perspective. Words related to the pipeline can come naturally when explaining an incident.

## 2. Did your prepared translation cover the follow-up question?

It covered most of it, but I still had to think about the exact wording when answering the follow-up. I think it is better to prepare the key facts and impact rather than memorize a full script.

## 3. How would this same 90 seconds change if the person asking were the client's data engineering lead?

I would include more technical details about the changed field, validation issue, fix, and reload process. The main facts would stay the same, but the level of technical detail would be higher.