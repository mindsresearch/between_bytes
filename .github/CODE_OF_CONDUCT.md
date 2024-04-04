# SelfScape Insight Repo Guidelines

## Introduction
This document outlines the standards, specifications, and style guidelines for collaborating on the Facebook Senior Project repository. Adhering to these guidelines ensures a smooth and efficient development process, minimizes conflicts, and maintains code quality.

## Definitions
The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED",  "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt).

## Repo Structure
- The `main` branch MUST be treated as the **PROD** environment.
  - This branch MUST always be in a deployable state.
  - The file `requirements.txt` MUST remain up-to date
>[!NOTE]
> `$ python3 main.py` on the `main` branch MUST always run without errors (except for errors resolved via `$ pip install -r requirements.txt`).

- Branches other than `main` SHOULD be treated as **DEV** environments.

## Procedures
1. **Feature/task branches**
   - Each feature/task SHOULD be isolated to its own branch
   - The name of a new feature/task branch SHOULD be fairly short (no longer than 2 words), and MUST be fully descriptive
   - New feature/task branches MUST be based on the latest version of `main`, with the exception of feature/task sub-branches
2. **Coding standards**
   - Code SHOULD conform to [PEP 8](https://peps.python.org/pep-0008/) style guidelines
   - Refer to [[docs/codeStandards.md]] for a more detailed look at coding standards
3. **Commits**
>[!WARNING]
> Except for weekly slides, __commits MUST NOT be made directly to the `main` branch__.
   - Commits SHOULD be made often
   - Commit messages MUST be clear and concise
   - Commit messages SHOULD use the imperative mood (e.g. "~~Did stuff~~" -> "Do stuff")
>[!NOTE]
> Commit messages SHOULD be made often enough that they MAY be reviewed to identify the source of (and trace) errors during the code review process.
4. **Merging**
   - Upon completing a feature or task, the associated branch SHALL be merged to the `main` branch via a Pull Request (PR) or another code review process.
   - Merges SHALL NOT be executed without approval from all other group members
5. **Pull Requests (PRs)**
   - Learning as we go here...
6. **Code Reviews**
   - For a group member to approve a merge/PR, the test conditions described below MUST be met.
   - Learning as we go RE: PR commenting/editing stuff...
7. **Testing**
   - The group member MUST test the changes in accordance with the "repo standards" section of this document using their own data download.
   - The group member MUST verify that the changes conform to the code standards.
8. **Documentation**
     - Code MUST be well documented with header comments for each file and each method. `features/sample.py` provides a "gold standard" example.
     - Code documentation SHOULD be in the style of a "formal" reference manual (such as the text of the [Pandas DataFrame reference](https://pandas.pydata.org/docs/reference/frame.html)) with minimal modification.
     - Information on the `main.py` commandline argument structure MUST be provided/updated in the README, and any changes to this structure within a **DEV** branch SHOULD be mentioned in the initial PR comment.
     - Commit descriptions beyond the summary message are OPTIONAL.