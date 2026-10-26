# Workflow Standards

## Git Standards

### Branch Naming
 - Branch names should be all lowercase.
 - Recommended branch prefixes are:
   - feature
   - fix
      - hotfix
   - refactor
   - chore
   - release
 - Branch name format: {prefix}/{name}
   - Ex. `feature/paypal-sync`

### Commit Standards
 - Commit messages should:
   - Be all lowercase.
   - Not end with a period.
   - Utilize branch prefixes.
 - Commit message format: "{prefix}({code-context}): {message}"
    - Ex. `"chore(readme): update setup steps"`