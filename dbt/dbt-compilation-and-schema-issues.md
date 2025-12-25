# TIL – dbt Lessons Learned in a Real Project

This note is a short summary of practical dbt lessons learned while working on a team data pipeline project. It focuses on real issues I ran into rather than dbt basics.

## dbt Compiles More Than You Expect

Even when I wanted to run a single Gold model, dbt tried to compile the entire project, including Silver models and sources. Because of this behavior, errors in unrelated models still blocked execution.

I also learned that using --exclude does not always help if the failure happens during the compilation phase rather than execution. This made it clear that keeping the whole project in a compilable state matters, even when working on one layer.

## sources.yml Naming Matters More Than It Looks

While debugging compilation errors, I discovered that table names defined in sources.yml must match the case used in SQL models. Using uppercase table names in sources.yml caused dbt to fail when the actual references in Silver SQL were lowercase.

Aligning naming conventions across sources.yml and model SQL files avoided silent mismatches and confusing compile errors.

## Using Macros to Control Target Schemas

By default, dbt respected the SNOWFLAKE_SCHEMA environment variable, which was set to SILVER. As a result, even Gold models were being created under the SILVER schema.

To fix this cleanly, I introduced macros that explicitly map models to existing Snowflake schemas. With this approach, Gold models were written to the GOLD schema while Silver models stayed in SILVER, without changing global environment variables.

This made schema control explicit and easier to reason about in a shared team environment.

## Where dbt Lives Matters (Container vs Host)

Initially, I installed and ran dbt inside a Docker container. This worked fine for personal testing. However, when a teammate rebuilt the container to add a new Airflow DAG, all dbt-related files inside the container were lost.

This highlighted the downside of container-only setups for tools that require persistent state or frequent edits. Moving the dbt project setup outside the container made the environment more stable and team-friendly.

## Project-Wide Consistency Is More Important Than Local Success

Several issues only appeared when teammates interacted with the setup, such as rebuilding containers or running dbt in a slightly different order. This reinforced that dbt projects should be designed to survive clean environments and fresh runs, not just local incremental work.

## Takeaway

Most dbt issues I faced were not about writing SQL, but about compilation scope, naming consistency, environment configuration, and team workflows. These factors had more impact on productivity than individual model logic.
