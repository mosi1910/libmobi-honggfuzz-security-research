# Publication, attribution and licensing checklist

Before making this repository public, confirm:

1. The university course rules allow public posting of the individual report and relevant experimental evidence, particularly before the course's final hand-in. If not, leave the repository **private** until permission is clear.
2. Every script and patch in this repository is your work or has permission from its coauthors. The report may be public only if its content and diagrams are yours to publish; remove teammates' unpublished data where applicable.
3. Do not push the entire `Fuzzing_Project` directory, generated corpora, VM images, private crash binaries, emails, tokens, internal university artifacts, or GitHub SSH keys.
4. The `sample-obfuscated-fonts.mobi` original seed and fuzz-generated MOBI derivatives are **omitted** due to unverified redistribution rights. Check licenses and attribution before publishing any example book binaries.
5. A historical libmobi vulnerability was fixed upstream in 2022. Do not claim to have discovered it first, obtained a CVE, or submitted the custom patch upstream.
6. Upstream libmobi is licensed LGPL-3.0-or-later. If you later vendor source files, honor that license and its notices. Do not imply that choosing MIT for your **own scripts** relicenses libmobi or other third-party content.
7. No top-level blanket `LICENSE` has been selected in this starter, because public upload rights and authorship for all included materials have not been independently established. Choose a license deliberately if appropriate.
8. The portfolio README describes **your Honggfuzz workstream only**, not AFL++ or zzuf/Radamsa tasks performed by teammates.

If a detail is not supported by evidence, qualify it instead of making it sound more impressive. For example, use **“rediscovered and validated a historical out-of-bounds read”**, not **“discovered a new zero-day.”**
