# MATRIX ROOM MANAGEMENT SCRIPTS - TUTORIAL

Written by: vlp and botbot 🤖

Last updated: 2025-10-17

Version: 1.0

NO WARRANTY EXPRESSED OR IMPLIED. USE AT YOUR OWN RISK.

## INTRODUCTION
This tutorial explains how to use four bash scripts designed for Matrix server maintenance on FDN infrastructure. These tools help administrators:

    * Identify rooms needing maintenance with too much event history
    * Clean this room
    * Find empty/unused rooms
    * Safely purge abandoned rooms

The scripts work together but can also be used independently.

## PREREQUISITES

    * Linux/Unix system with bash 4.0+
    * synadm (Synapse admin tool) installed and configured
    * Standard Unix utilities (awk, grep, sed)
    * Matrix server admin privileges (token provided to synadm)

## SCRIPT OVERVIEW

### create_list.sh

Purpose: Generates a prioritized list of top 150 rooms for cleaning

Output: Creates 'room.list' file with room IDs and message counts

Usage: ./create_list.sh

### clean.sh

Purpose: Purges messages older than 30 days from active rooms

Input: 'room.list' file from create_list.sh

Usage: ./clean.sh

Note: Destructive operation - events are permanently deleted

### create_empty.sh

Purpose: Identifies empty rooms or rooms with only one external user

Output: List of room IDs with member counts

Usage: ./create_empty.sh > empty_rooms.list

### purge_empty.sh

Purpose: Removes empty/unused rooms with three safety modes

Input: List of empty rooms from create_empty.sh

Usage:

* Automatic: ./purge_empty.sh empty_rooms.list
* Dry-run: ./purge_empty.sh --dry-run empty_rooms.list
* Manual: ./purge_empty.sh --manual empty_rooms.list

## RECOMMENDED WORKFLOW 

### Monthly Maintenance:

    * Generate cleaning list: $ ./create_list.sh
    * Review the generated room.list: $ less room.list
    * Execute cleaning: $ ./clean.sh

### Quarterly Space Reclamation:

    * Find empty rooms: $ ./create_empty.sh
    * Verify with dry run: $ ./purge_empty.sh --dry-run empty_candidates.list
    * Execute purge: $ ./purge_empty.sh

### Reindex & Vacuum:
In order to claim back database space and improve performance after cleaning or purging rooms, it is mandatory to reindex and vacuum the database:

    * After cleaning/purging, reindex and vacuum the database for performance:
    * Connect to the database with the postgres user:
      $ sudo -u postgres psql synapse
    * Run the following SQL commands:
      REINDEX TABLE events;
      VACUUM FULL;


### Always:

    * Verify generated lists before execution
    * Use dry-run modes when available
    * Maintain current database backups
    * Start with manual mode when unsure

### Protected Rooms:

    * Scripts automatically skip rooms ending with 'fdn.fr'
    * To add more protected patterns, modify PROTECTED_ROOM_PATTERN variable

### Common Issues:

Issue: Permission denied errors

Solution: Verify synadm configuration and admin credentials

Issue: Invalid room listay cleanup threshold?

A: Yes, edit the DAYS_THRESHOLD variable in clean.sh

Q: How do I add more protected rooms?

A: Modify PROTECTED_ROOM_PATTERN variable using pipe separator:
readonly PROTECTED_ROOM_PATTERN='fdn.fr|protected.domain|another.domain'

Q: What happens if I interrupt a script?

A: Scripts are interrupt-safe. Completed operations persist, incomplete ones abort.

Q: Can I test on a subset of rooms?

A: Yes, create a test list file with a few room IDs and use as input.

Q: How often should I run these scripts?

A: create_list.sh + clean.sh: Monthly
create_empty.sh + purge_empty.sh: Quarterly
Adjust based on server activity level.

## LICENSE AND DISCLAIMER

NO WARRANTY EXPRESSED OR IMPLIED. USE AT YOUR OWN RISK.

These scripts are provided "as is" without any guarantees.

The authors are not responsible for any data loss or service disruption.

Always test in a safe environment before production use.

