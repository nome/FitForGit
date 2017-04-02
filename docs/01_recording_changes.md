Recording Changes
=================


First-time setup
----------------

    git config --global user.name "Your Name"
    git config --global user.email user@domain.tld

Git is a distributed system, so it uses email addresses to uniquely identify users.

<ul class="hints">
<li> try <code>git help config</code></li>
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
<li> run <code>git init</code> without argument to start tracking existing files in <code>./</code></li>
</ul>


Staging changes
---------------

    git add cool_stuff.txt
    git status

-------- ---------- ---------------- ------ ----
**file** **&rarr;** **staging area** &rarr; HEAD
-------- ---------- ---------------- ------ ----

. . .

The staging area can track only one version of each file, so we're not done yet.

<ul class="hints">
<li> you can also add entire directories with <code>git add</code></li>
</ul>


Committing (to) a version
-------------------------

    git commit
    git status

---- ------ ---------------- ---------- --------
file &rarr; **staging area** **&rarr;** **HEAD**
---- ------ ---------------- ---------- --------

    gitk

<ul class="hints">
<li> you can skip <code>git add</code> for files known to Git using <code>git commit -a</code></li>
</ul>


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
<li> Try <code>git revert HEAD~1</code>. What does it do? Can you revert other changes?</li>
<li> Look at the contents of the <code>.git</code> directory - what changes at each step?</li>
</ul>
