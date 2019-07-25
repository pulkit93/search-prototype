# Commit message guidelines

A good commit message should describe what changed and why. 

Commit Message format:

```
<prefix>: <short description> (refs #<jira ticket>)
<long description>
```

Common prefixes:
* fix: A bug fix
* feat: A new feature
* docs: Documentation changes
* test: Adding missing tests or correcting existing tests
* build: Changes that affect the build system
* ci: Changes to our CI configuration files and scripts
* perf: A code change that improves performance
* refactor: A code change that neither fixes a bug nor adds a feature
* style: Changes that do not affect the meaning of the code (linting)
* depend: Bumping a dependency 

Other things to keep in mind when writing a commit message:

1. The first line should:
    * contain a short description of the change (preferably 50 characters or less, and no more than 72 characters)
    * be entirely in lowercase with the exception of proper nouns, acronyms, and the words that refer to code, like function/variable names
2. Keep the second line blank.
3. Wrap all other lines at 72 columns.

# Breaking Changes

A commit that has the text BREAKING CHANGE: at the beginning of its optional body or footer section introduces a breaking API change. A breaking change can be part of commits of any type.


# Merging into master

Always squash before merge into master
