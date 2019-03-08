Branching and Merging
=====================

Visualizing history
-------------------

::::::::: {.columns}
::: {.column width="30%"}
![linear history](img/git-branch.svg)
:::
::: {.column width="70%" .textcolumn}
    git log --graph --oneline

    * 5567e85 (HEAD -> master) commit c
    * df5a1e0 commit b
    * d3a1a32 commit a
:::
:::::::::

Branching off
-------------

::::::::: {.columns}
::: {.column width="30%"}
![two branches](img/git-branch-diverge.svg)
:::
::: {.column width="70%" .textcolumn}
    git branch feature master~2
    git checkout feature
    $EDITOR; git commit -a

    * 16ae900 (feature) feature commit d
    | * 5567e85 (master) commit c
    | * df5a1e0 commit b
    |/
    * d3a1a32 commit a
:::
:::::::::

Listing branches
----------------

::::::::: {.columns}
::: {.column width="30%"}
![two branches](img/git-branch-diverge.svg)
:::
::: {.column width="70%" .textcolumn}
    git branch
  
    master
    * feature

The current branch (`feature`) is marked with a `*`. It is also referred to as `HEAD`.
:::
:::::::::

Merging
-------

::::::::: {.columns}
::: {.column width="30%"}
![merge](img/git-branch-merge.svg)
:::
::: {.column width="70%" .textcolumn}
    git checkout master
    git merge feature

* all changes in `feature` are added to `master`
* parallel histories are preserved
:::
:::::::::

Merge conflicts
---------------

Git merges histories of the entire repository; until _all_ conflicts are
resolved and committed, the merge is "in progress" for all files.

<ul class="hints">
<li>You can abort a merge in progress with `git merge --abort`</li>
</ul>

Rebasing
--------

::::::::: {.columns}
::: {.column width="30%"}
![rebase](img/git-branch-rebase.svg)
:::
::: {.column width="70%" .textcolumn}
    git checkout feature
    git rebase master

* all changes in `feature` are re-committed against `master`
* => conflicts may have to be resolved multiple times
* result is similar to merge, but looks as if `feature` development had started on top of current `master`
:::
:::::::::

Cherry-picking
--------------

::::::::: {.columns}
::: {.column width="30%"}
![cherry-pick](img/git-cherry-pick.svg)
:::
::: {.column width="70%" .textcolumn}
    git checkout master
    git cherry-pick feature

* only specific changes are re-committed against `master`
* useful for backporting bugfixes to a release branch
:::
:::::::::

Merge/Rebase/Cherry-pick
-------------------------

::::::::: {.columns}
::: {.column width="25%"}
![two branches](img/git-branch-diverge.svg)
:::
::: {.column width="25%"}
![merge](img/git-branch-merge.svg)
:::
::: {.column width="25%"}
![rebase](img/git-branch-rebase.svg)
:::
::: {.column width="25%"}
![cherry-pick](img/git-cherry-pick.svg)
:::
:::::::::

Training Time
-------------
