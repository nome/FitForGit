Recording Changes
=================


First-time setup
----------------

    git config --global user.name "Your Name"
    git config --global user.email user@domain.tld

Git is a distributed system, so it uses email addresses to uniquely identify users.

<ul class="hints">
<li> try `git help config`</li>
</ul>


Creating a repository
---------------------

    git init repo
    cd repo

This creates a new, empty repository which lives only on your computer (for
now).

    echo git > cool_stuff.txt
    git status

<ul class="hints">
<li> run `git init` without argument to start tracking existing files in `./`</li>
</ul>


Staging changes
---------------

    git add cool_stuff.txt
    git status

![](img/git-add.svg)

<ul class="hints">
<li> you can also add entire directories with `git add`</li>
<li> make changes in different parts of a file and try `git add -p`</li>
</ul>

<div class="notes"><ul>
<li>The staging area can track only one version of each file, so we're not done yet.</li>
</ul></div>


Committing (to) a version
-------------------------

    git commit
    git status

![](img/git-commit.svg)

<ul class="hints">
<li> you can skip `git add` for files known to Git using `git commit -a`</li>
</ul>


Viewing history
---------------

--------- ------- ---------------
`gitk`    GUI     separate tool
`tig`     ncurses separate tool
`git log` text    included in git
--------- ------- ---------------

Every commit contains a snapshot of the entire repository; unlike checkins in
RCS or Subversion, which operate on individual files or directories,
respectively.


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

After a blank line follows the answer to the "why". What was
the motivation for the change? How is the need addressed by
this commit?

If applicable: Which alternatives were considered, and why
were they discarded?

If applicable: Reference to #bugid
```



Training Time
-------------

    git config --global user.name "Your Name"
    git config --global user.email user@domain.tld

1. create a new, empty repository
2. commit some changes
3. view the resulting history

<ul class="hints">
<li> Try `git revert HEAD~1`. What does it do? Can you revert other changes?</li>
<li> Look at the contents of the `.git` directory - what changes at each step?</li>
</ul>
