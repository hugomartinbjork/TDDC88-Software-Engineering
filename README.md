**Version handling**

| **Name ** | **Changes ** | **Date ** | **Inspector name** | **Comments ** | **Date ** | **Version ** |
| --- | --- | --- | --- | --- | --- | --- |
| Fredrik Hammarbäck (Development Manager), Oscar Söderlund (Technical Writer)   | Wrote the first version on how we use Git | 2022-09-20 | Madeleine Jacobsson (Process Manager), Adam Åström (R&D Line Manager) |   |  2022-09-20 | V1.0  |
| Fredrik Hammarbäck | Added a Summary.Added Contents section. Added section for Testers and tests. Clarified Developers' and Testers' responsibilities when merging to dev and main, respectively. | 2022-10-04 | Oscar Söderlund | Inspected and prepared feedback | 2022-10-16 |  V2.0 |
| Oscar Söderlund | Fixed some spelling errors. | 2022-10-16 | Fredrik Hammarbäck |
 | 2022-11-06 | V2.1 |
| Oscar Söderlund | Removed any mentions of trunk-based and made clarifications. | 2022-10-19 | Fredrik Hammarbäck | Fixed grammatical error in "How does Git branching work for testers | 2022-11-06 | V2.2 |
| Fredrik Hammarbäck | Added clarification regarding unit testing of written code by Developers and an example | 2022-11-08 | Madeleine Jacobson | Good clarifications | 2022-11-10 | V2.3 |

# Summary

For Developers:

1. Create a Feature branch
2. Write your Feature
3. Pull/merge to dev (the code must be unit tested)

For Testers:

1. Create a Test Branch
2. Test the code on it
3.
 a) The code passes the tests and is pull/merged to main (ready for delivery)

b) The code fails but can be hotfixed in the Test Branch. Tester or Developer fixes it. Pull/merge it to main

c) The code fails and cannot be hotfixed in the Test Branch. Developer fixes it. Repeat from step 1.

# Contents:

- Git branching process: feature-based development - Let's git good
  - About feature-based development
  - How will the Git structure look?
  - Why should we use this Git strategy?
  - How will the flow of version handling look?
- How does branching work for testers?
- How does feature-based development work for Developers?
- What happens if the code fails the Tests
- How will simultaneous coding work in practice?
- Instruction of how to use process
  - How to see our branches
  - Some useful Git commands

# Git branching process: Feature-based development - Let's git good

This guide will explain how we use branches in Git. This **mainly** concerns **Developers** and **Tester** s, but **everyone** who will take part in the **development** and manage their code with our Company's GitLab repo must **familiarize** themselves with this process' contents.

**About feature-based development:**

Continuously integrating progress made by developers using this method is very similar to simple feature branching. The main difference is the frequency with which new branches are created, updated, integrated and closed.

**How will the Git structure look?**

![Bildobjekt 1](RackMultipart20221110-1-bks5au_html_ffd7177bc9d8081e.gif)

The "Main Branch" will contain the absolute confirmed progress (version 1, version 2, etc.). This branch will be the least frequently updated branch.

The "Developer Branch" will be the most frequently branch and will be the base for continuous updating and branching.

The "Feature Branch(es)" will be temporary branches created for very specific tasks by each developer working on the task. Once tasks are completed, the branches will be terminated.

The "Test Branch(es)" will also be temporary branches created for testing the code Feature Branches. Testers have ownership of these branches.

**Why should we use this Git strategy?**

If feature-based development is used successfully, the developer branch will be continuously updated, and the developers respective feature branches will most often contain the latest updates on the developer branch. Since all merge conflicts are solved by each developer on their working branch, no single person will be responsible for or approving all merges. This makes version handling very easy since the developers will handle conflicts that are related to what they themselves are currently working on.

![Bildobjekt 8](RackMultipart20221110-1-bks5au_html_907457c25c8eb85d.gif)

**How will the flow of version handling look?**

Pulling and merging occurs frequently. Pulling before merging is crucial to solving and avoiding merge conflicts.

# How does the branching work for Testers?

![Bildobjekt 8](RackMultipart20221110-1-bks5au_html_907457c25c8eb85d.gif)
 ![Shape1](RackMultipart20221110-1-bks5au_html_a08835991ac94961.gif)As the image above illustrates, when a Feature branch is merged to dev, the Testers creates a new branch from dev. This is the Testing Branch (seen in yellow). The Testers can perform whatever tests they want on the features on that branch.

- If the Test Branch is testing a feature called "feature 1", it is recommended that the Test Branch is named "test-feature-1"
  - Alternatively, the Test Branch can be named "test-\<name-of-feature-branch\>"
  - Ultimately, Testers may decide on other names for the Test Branches
- If the code in the Test Branch fulfills the requirements and passes the tests designed by the Testers, the Test Branch can be merged to the main branch. **This is only to be done if the code is deemed ready for delivery by the Testers.** Tick the box to squash the commits when merging.
- If testing reveals that the code needs a fix, it is up to the Testers to decide if the Test Branch can be hotfixed and merged to the main branch
  - Alternatively, if the Testers conclude that the code on the Test Branch needs exhaustive fixes, it will be passed to the Developer who wrote the feature in the first place
- Testers are allowed to fix code on the Test Branch at their own discretion

# How does feature-based development work for Developers?

Whenever you are to continue or start working on a feature or any coding task, following these steps will ensure that you and your fellow developers maintain and work on the latest version of our product.

1. Before you start working on a task, branch out from the Developer Branch and name your new branch after your task. If, for example, you are to start working on a function that allows for editing of user information, simply name the branch "feature/edit-user-info". Checking out using the command _git checkout -b "feature/edit-user-info"._
2. After some time of coding (about once an hour or if commits to the dev branch has been made), update your branch with what has changed in the developer branch. This is done using the command _git pull origin dev_ where "dev" is the name of the developer branch.
3. Pulling from the developer branch will sometimes result in merge conflicts. As long as the different branches are working on different things, these conflicts are usually solved very quickly by simple clicking "accept incoming changes". If there is some overlapping or conflicting code, further investigate and solve merge conflicts until none remain.
4. Whenever you feel it's time to commit and save your progress (the task has been completed and your code is compiling), simply follow these steps:
  1. Git pull origin dev (and solve for eventual merge conflicts)
  2. Git status.
  3. Git add \<\<files you have edited\>\>
  4. Git commit -m "\<\<descriptive comment\>\>"
5. The commits you make during your work should be merged to dev as soon as possible after task completion. **The code must be considered functional before it is merged to dev.** This means that it compiles and executes correctly; all functions, classes and contents of the code must work as intended by the Developer. To confirm that the code functions correctly, the Developer must unit test the code. This can be done by testing the functionality with Postman.

  - For example, if the Developer has finished task 9.7.1 "Create view called get\_user\_transactions etc.", the Developer must add items to their local instance of the database and make a request to with Postman to the URL /api/user/\<user\_id\>/transactions and check that the correct data is returned

1. When you have completed your task, repeat steps 1-5 and merge one final time. The Feature Branch must be kept, so make sure to **not tick the box to delete the source branch** when merging to dev. Also, **make sure that the tick box to squash commits IS ticked.**

# What happens if the code fails the Tests

One of two things can happen:

1. The tester concludes that the problem can be hotfixed in the Test Branch.
 Testers will then decide this on their own whether a developer will be assigned to fix it (preferably the code's author) or if they shall fix it themselves. When fixed, they may merge the Test Branch to main

1. The testers conclude that the problems cannot be hotfixed in the Test Branch.
 The Testers will decide this on their own discretion. Testers are required to notify the Developer who wrote the code in question. The Developer is responsible for fixing the code on their Feature Branch and make another pull/merge to dev, after which the Testers can test it again

# ![Bildobjekt 4](RackMultipart20221110-1-bks5au_html_8acc3fc1dc12bb1b.gif)
How will simultaneous coding work in practice?

Developing branches will continuously receive and submit progress from and to other branches. In the example case above, the second pull to branch A will contain merged changes made on branch B. Each pull that contains changes to the developer branch might cause conflicts. If the task division between developers is clear, conflicts rarely happen.

# Instruction of how to use process

**We use the following GitLab repo for our code:**

[https://gitlab.liu.se/tddc88-2022/c4/rdx-solutions-backend-project](https://gitlab.liu.se/tddc88-2022/c4/rdx-solutions-backend-project)

**How to see our branches:**

For an overview of the branching structure of the repo, press Repository in the menu on the left-hand side in Gitlab. Press Graph (as seen in the below figure).

![Picture 3](RackMultipart20221110-1-bks5au_html_fdc0c4d7e8b123c.gif)

You will be met with a graph of the current branches, where the latest commits are presented at the top, see the image below. Note that this image is taken from Stack Overflow, our graph will look a bit different.

![Picture 1](RackMultipart20221110-1-bks5au_html_a966ed9118350324.gif)

## Some useful Git commands

**You can propose changes** (add it to the Index) using the command:

_git add \<filename\>_

**You can add several files at once** if you want to by using one of the following commands:

_git add \<filename1\> \<filename2\> ... \<filenameN_\>, several files separated by spaces

_git add -A_, stages all changes

_git add ._, stages new files and modifications, without deletions (on the current directory and its subdirectories).

_git add -u_, stages modifications and deletions, excluding new files.

**If something goes wrong.**

If you are in need of comparison between your current branch and the developer branch, using the command _git checkout \<\<name of the developer branch\>\>_ will move you to the developer branch. Make sure you commit the changes in your own feature branch before switching branch or else you will lose the progress you have made locally.

Should you be unable to resolve any eventual conflict in your branch or need help with version control, contact the configurations team and ask for help. Be sure to never merge any branch containing unresolved issues.

**Some other useful commands for resolving issues with your version handling are:**

_Git stash__ **,** _ **Your changes will then be "saved for later"** and can be fetched later to the active branch using:

_git stash apply,_ the stored changes can then be deleted from the stash using:

_git stash drop_

**If you mess up your versions big time** , it might be a good idea to revert your version to a specific commit by using

_git revert \<commit id\>_

**The commit id** can be found by using the command

_git log_

and find ex. "commit f668c5f186aeb35f0fff5049c847ef2056512290", where the commit id is the long string of letters and numbers.
