Recording Changes
=================


First-time setup
----------------

    git config --global user.name "Your Name"
    git config --global user.email user@domain.tld

Git is a distributed system, so it uses email addresses to uniquely identify users.

**hints**

* try `git help config`



Your first repository
---------------------

    git init repo
    cd repo

This creates a new, empty repository which lives only on your computer (for
now).

    echo git > cool_stuff.txt
    git status

**hints**

* you can also run `git init` without argument to start tracking existing files



Staging changes
---------------

    git add cool_stuff.txt
    git status

This adds a snapshot of `cool_stuff.txt` to the staging area. Changes made
afterwards will not be recorded, unless you run `git add` again.

The staging area can track only one version of each file, so we're not done yet.

**hints**

* you can also add entire directories with `git add`



Committing (to) a version
-------------------------

    git commit
    git status

    gitk

**hints**

* you can skip `git add` for files known to Git using `git commit -a`



The why of commit messages
--------------------------

* the who/when/what of a change is recorded automatically
* commit messages primarily explain the "why"
* they summarize changes for history overviews (e.g. in `gitk`)
* they may contain pointers to ticket IDs for future reference



The how of commit messages
--------------------------

```
First line: very short summary, what changed?

After a blank line follows the answer to the "why". What was the motivation
for the change? How is the need addressed by this commit?

If applicable: Which alternatives were considered, and why were they
discarded?
```



Training Time
-------------

    git config --global user.name "Your Name"
    git config --global user.email user@domain.tld

1. create a new, empty repository
2. commit some changes
3. view the resulting history

**freestyle**

* look at the contents of the `.git` directory - what changes at each step?
