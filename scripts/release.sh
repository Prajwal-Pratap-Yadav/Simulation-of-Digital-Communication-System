#!/usr/bin/env bash
# Executed only by the release CI job after all validation jobs succeed.
set -euo pipefail
expected_repo='Prajwal-Pratap-Yadav/Simulation-of-Digital-Communication-System'
[[ "${GITHUB_REPOSITORY:-}" == "$expected_repo" ]] || exit 1
[[ "${GITHUB_REF:-}" == 'refs/heads/main' ]] || exit 1
head=$(git rev-parse HEAD)
[[ "$head" == "$GITHUB_SHA" ]] || exit 1
version=$(.venv/bin/python -c 'from commsim import __version__; print(__version__)')
tag="v$version"
if gh release view "$tag" --repo "$expected_repo" >/dev/null 2>&1; then
  tagged=$(gh api "repos/$expected_repo/git/ref/tags/$tag" --jq '.object.sha')
  [[ "$tagged" == "$head" ]] || {
    echo 'Existing release belongs to a different commit; bump the version.' >&2
    exit 1
  }
  exit 0
fi
# Create a lightweight tag with no additional commit; never move an old tag.
git tag "$tag" "$head"
git push origin "refs/tags/$tag"
sha256sum dist/* > dist/SHA256SUMS
gh release create "$tag" dist/* --repo "$expected_repo" --verify-tag \
  --title "Digital Communication Simulation $version" \
  --notes-file docs/release-notes.md
[[ "$(git rev-parse "$tag^{commit}")" == "$head" ]]
