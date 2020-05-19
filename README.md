# orgRealmMigration
For migrating dashboard groups and detectors to new org in another realm


# Usage

## For exporting dashboard groups (caution: using undocumented APIs that may not work in the future)

Apart from the realm+tokens it needs a list of dashboard group IDs in a file (newline separated list)
 
Usage: python exportDashboardGroup.py SF_REALM1 SF_TOKEN1 SF_REALM2 SF_TOKEN2 DASHBOARD_GROUPS_FILE
 
Example contents of DASHBOARD_GROUPS_FILE (dgroups):
Dylv1kMAcAA
DYMbT3iAgAA


## For exporting detectors

NOTE: For tokens, you MUST use the User Session Tokens for an admin, since we would need permissions and users and team details.
This will transfer over the following detector permissions:
1. Users (email address)
2. Teams (The same team name MUST exist in the new org)

This will transfer over the following notifications:
1. Emails
2. Teams (The same team name MUST exist in the new org)

This will transfer over the following links:
1. Teams (The same team name MUST exist in the new org)

TODO: Slack and other notification transfers

Usage: python exportDetectors.py SF_REALM1 SF_TOKEN1 SF_REALM2 SF_TOKEN2 