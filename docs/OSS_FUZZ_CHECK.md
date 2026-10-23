# OSS-Fuzz enrollment verification: libmobi

**Review date:** 23 October 2026  
**Target:** `bfabiszewski/libmobi` (`https://github.com/bfabiszewski/libmobi`)  
**Question:** Is libmobi enrolled as its own project in Google's OSS-Fuzz service?

## Finding

**No standalone public OSS-Fuzz project registration was found for libmobi as of the review date.** This is an evidence-based negative finding about the *public standalone registry*, not proof that libmobi has never been fuzzed by any OSS-Fuzz project indirectly or that an integration cannot be registered under an unexpected name.

## Verification method and evidence

1. OSS-Fuzz's official onboarding guide says each integrated project is represented by a project directory under `projects/` with a `project.yaml` configuration. Official documentation: https://google.github.io/oss-fuzz/getting-started/new-project-guide/
2. Checked the canonical raw GitHub file URLs for two plausible standalone project names. Both returned **HTTP 404 Not Found** at the time of review:
   - https://raw.githubusercontent.com/google/oss-fuzz/master/projects/libmobi/project.yaml
   - https://raw.githubusercontent.com/google/oss-fuzz/master/projects/mobi/project.yaml
3. Searched public web-indexed references to `libmobi` in `google/oss-fuzz` without finding a project-specific registration or configuration entry.
4. Searched the public Fuzz Introspector project overview for `libmobi`, `mobi`, and `kindle`: no matching entry appeared. **Important limitation:** the service states that its published overview contains only a subset of enrolled projects (924 of 1,385 at the time inspected), so absence from that table alone is insufficient to establish non-membership. Overview: https://introspector.oss-fuzz.com/projects-overview
5. libmobi's v0.11 release notes credit several external fuzzing researchers, including an account with `oss-fuzz` in its name. Such a credit does **not** establish enrollment in Google's OSS-Fuzz registry. Releases: https://github.com/bfabiszewski/libmobi/releases

## Recommended entry for the university report

**In OSS-Fuzz?** `No standalone public integration found (checked 23 Oct 2026).`

Suggested explanatory sentence:

> We found no publicly registered standalone OSS-Fuzz project for libmobi. The expected project.yaml entries for `libmobi` and `mobi` were absent from the official OSS-Fuzz repository, and libmobi was not listed in the public Fuzz Introspector overview. Because this overview is incomplete and indirect dependencies or differently named integrations are possible, we interpret the result as a negative public-registry finding rather than proof of complete non-enrollment.

## Scope

This assessment concerns *enrollment in OSS-Fuzz*, not whether the library was previously fuzzed by independent researchers, other infrastructures, or this university experiment. No private OSS-Fuzz dashboard was accessed; no assertion is made about confidential integrations or internal build targets.
