# Releases

CI runs on pull requests and pushes to `main`. It synchronizes locked dependencies, runs `just check`, audits dependencies, builds the source distribution and wheel, and retains those distributions as workflow artifacts.

Pushing a tag named `v<version>` creates a GitHub Release. The workflow requires the tag version to exactly match `[project].version` in `pyproject.toml`, reruns the CI checks and audit, then attaches the built source distribution and wheel to the release.

For the current version, create and push a signed tag after the release commit is on `main`:

```bash
git tag -s v0.1.0 -m "v0.1.0"
git push origin v0.1.0
```

The release workflow has GitHub `contents: write` permission only. It does not publish to PyPI.
