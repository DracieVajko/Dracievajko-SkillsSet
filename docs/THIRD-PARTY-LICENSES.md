# Third-Party Licenses and Notices

This repository contains **three different kinds of content**. They are never
interchangeable, and this page records the licensing position of each.

| Content class | Where it lives | Licensing |
|---------------|----------------|---------------|
| **Original content** | `skills/original/`, `prompts/`, `instructions/`, `docs/`, `scripts/`, `catalog/` | MIT, © 2026 DracieVajko - see the root [LICENSE](../LICENSE) |
| **External content referenced by URL** | `catalog/links/*.txt`, `catalog/items.json` (199 `link-only` records) | Upstream licenses apply. No content is copied into this repository. |
| **Third-party content physically bundled** | `skills/third-party/` (7 `SKILL.md` copies) | Upstream MIT licenses, reproduced in full below |

A link is not a license grant. A bundled copy is a redistribution, so the
upstream license terms - including the copyright notice - travel with it.

## Bundled third-party skills

Seven reverse-engineering skills are bundled as local copies under
`skills/third-party/`. They were copied into this repository with the
maintainer's approval and remain the property of their upstream authors.

| Bundled skill | Upstream project | Upstream license | Copyright |
|---------------|------------------|------------------|-----------|
| [`apk-reverse`](../skills/third-party/apk-reverse/SKILL.md) | [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) | MIT | © 2026 zhaoxuya520 |
| [`binary-diff`](../skills/third-party/binary-diff/SKILL.md) | [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) | MIT | © 2026 zhaoxuya520 |
| [`ghidra-reverse`](../skills/third-party/ghidra-reverse/SKILL.md) | [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) | MIT | © 2026 zhaoxuya520 |
| [`js-reverse`](../skills/third-party/js-reverse/SKILL.md) | [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) | MIT | © 2026 zhaoxuya520 |
| [`mobile-reverse`](../skills/third-party/mobile-reverse/SKILL.md) | [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) | MIT | © 2026 zhaoxuya520 |
| [`reverse-engineering`](../skills/third-party/reverse-engineering/SKILL.md) | [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) | MIT | © 2026 zhaoxuya520 |
| [`reverse-engineer-anything`](../skills/third-party/reverse-engineer-anything/SKILL.md) | [morluto/rea](https://github.com/morluto/rea) | MIT | © 2026 morluto |

Each bundled file carries a short provenance notice directly under its
frontmatter. No functional content was changed: the only difference from the
upstream file is that notice line.

The companion files that each bundled skill links to inside its own directory
are bundled as well, so the vendored skill works without a network round trip:

| Bundled skill | Companion files bundled |
|---------------|--------------------------|
| `reverse-engineer-anything` | `references/` - 8 files |
| `reverse-engineering` | 14 sibling files plus `references/` - 4 files |

A few upstream links point at **sibling skills that are not vendored here**
(for example `dotnet-reverse`, `field-journal` and `ops/`). Those links are
kept exactly as upstream wrote them and are reported by
`scripts/check-markdown-links.py` as warnings. Fetch the missing files from
the upstream repository if you need them.

## License text - zhaoxuya520/reverse-skill

```
MIT License

Copyright (c) 2026 zhaoxuya520

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## License text - morluto/rea

```
MIT License

Copyright (c) 2026 morluto

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## External skills referenced by URL

The other 199 external skills are **not copied** into this repository. They are
recorded in [`catalog/links/`](../catalog/links/) and
[`catalog/items.json`](../catalog/items.json) with `authorship: link-only`, and
their licenses stay with their upstream authors.

Verifying that a URL returns HTTP 200 confirms availability only. It does not
confirm the license, the content, the security posture or the runtime
compatibility of the linked file. Check the upstream project before installing
anything it contains.

## Adding third-party content

1. Confirm the upstream license permits redistribution.
2. Record the copyright holder and the full license text on this page.
3. Add the file to the approved bundled list in
   `scripts/test_skills_tooling.py` (`APPROVED_THIRD_PARTY_SKILLS`).
4. Add the provenance notice under the file's frontmatter.
5. Update [ATTRIBUTION.md](../ATTRIBUTION.md) and
   [skills/third-party/README.md](../skills/third-party/README.md).

Everything else stays link-only.

---

*Upstream licenses were read from the `LICENSE` files of
`zhaoxuya520/reverse-skill` and `morluto/rea` on 2026-11-12.*
