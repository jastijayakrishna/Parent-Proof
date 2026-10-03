# First run, 2026-10-03

These 20 records decided only each pull request's last commit that touched a
.proto file, against its parent. From the next run on, each pull request is
decided as one change, from its merge base to its head; these pull requests are
decided again that way in predictions/.
