# GLVD DB Schema draft

This is a place to draft a new, braking change of the DB Schema for glvd.

The current schema as of April 1st, 2025 is in `glvd-schema_v0.sql`.

A simplified, not yet working draft schema is in `glvd-schema_v1alpha1.sql`.


Why should we go the route of an incompatible schema change?

- The naming of the v0 schema is not consistent, a breaking change is the chance to fix this
- The requirement to join the `dist_cpe` table only to resolve the `dist_id` of a garden linux version is annoying
- The triage process will be simpler if this join is not needed
- With this change, we should also setup tooling that allows database migrations, allowing is to migrate from schema v1.0 to v1.1 etc
