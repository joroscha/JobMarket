# Job Search Tracker

Use [application_tracker.csv](/Users/joroscha/projects/JOB%20MARKET/INDUSTRY/application_tracker.csv) for jobs and [contact_tracker.csv](/Users/joroscha/projects/JOB%20MARKET/INDUSTRY/contact_tracker.csv) for networking in Google Sheets, Excel, or Numbers.

Recommended statuses:

- `saved`
- `networking`
- `ready_to_apply`
- `applied`
- `recruiter_screen`
- `hiring_manager`
- `technical_loop`
- `onsite`
- `offer`
- `rejected`
- `withdrawn`

Recommended fields:

- `role_family`: use values like `applied_economist`, `data_scientist_experimentation`, `research_scientist_empirical`, `applied_scientist`, `policy_research`
- `level`: normalize titles into `entry`, `mid`, `senior`, `staff`
- `fit_score`: quick 1-5 score based on role fit, location, and interest
- `priority`: use `A`, `B`, `C` so the sheet can be sorted quickly
- `next_step` and `next_step_date`: always keep these filled once a role matters

Suggested weekly workflow:

1. Add all interesting roles with `status=saved`.
2. Score each role on fit and set a priority.
3. Convert the top roles into `ready_to_apply` only after you have a tailored resume version.
4. Track every conversation with recruiters, referrals, and hiring managers in `notes`.
5. Review the sheet twice a week and close loops on any role with a blank `next_step_date`.

Suggested views:

- `Pipeline`: company, title, location, status, next step, next step date
- `Targets`: only `A` priority roles, sorted by fit score and next action date
- `Interviews`: only roles at `recruiter_screen` or later

Daily interview rhythm:

- 30 min: one product or company case using a real platform you know
- 30 min: SQL or data manipulation practice
- 30 min: statistics, experimentation, or causal inference review
- 30 min: one behavioral story in STAR format
- 30 min: one research-to-industry translation drill

Translation drill prompt:

"Explain one of my papers as if I were pitching its business value to a hiring manager in 2 minutes."

## Contact Tracker

Recommended statuses:

- `to_reach_out`
- `messaged`
- `replied`
- `meeting_scheduled`
- `met`
- `referred`
- `closed`

Recommended fields:

- `relationship_strength`: use values like `close`, `warm`, `light`, `cold`
- `outreach_goal`: keep this concrete, for example `role triage`, `intro call`, `referral`, `team insight`
- `referral_status`: use values like `not_asked`, `ask_if_fit`, `requested`, `referred`, `declined`
- `next_step` and `next_step_date`: always keep these filled once a contact matters

Suggested workflow:

1. Add a contact as soon as they become relevant to a target company.
2. Track the specific role or job URL tied to the outreach whenever possible.
3. Log the last touchpoint and set the next action immediately after each exchange.
4. Separate `status` from `referral_status` so the pipeline stays clear.
