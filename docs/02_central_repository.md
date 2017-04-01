Central Repository
==================


Clones
------

    git clone git@ffg:ffg/hello.git
    cd hello
    ls
    git status

This has created a _clone_ of the hello.git repository. The repository we
cloned from is called its _origin_.

**hints**

* by convention, central repositories have the postfix `.git`, while
  repositories we can make commits in do not



Pulling updates from upstream
-----------------------------

    git pull

Now the history of the repository looks like this:

    *   8c577b0 Merge branch 'master' of http://ffg/ffg/hello.git
    |\  
    | * b983d4c Linux is also cool
    * | e8fa16e Start collecting numbers
    |/  
    * 3adcc80 My second git commit
    * b323f69 My first git commit

**hints**

* the above graph was printed by `git log --graph --oneline`



Resolving conflicts
-------------------

    git pull

In `cool_stuff.txt`:

```conflict
Tübix
Git
<<<<<<< HEAD
reveal.js
=======
Linux
>>>>>>> b983d4cc25261780d3b2a21a142d4750394c5c77
```

Recommended solution:

    git mergetool
    git commit



"Uploading" changes
-------------------

    git push
    # Counting objects: 3, done.
    # Writing objects: 100% (3/3), 265 bytes | 0 bytes/s, done.
    # Total 3 (delta 0), reused 0 (delta 0)
    # To git@ffg:ffg/hello.git
    #    d039e72..325b819  master -> master

    git push
    # Counting objects: 3, done.
    # Writing objects: 100% (3/3), 265 bytes | 0 bytes/s, done.
    # Total 3 (delta 0), reused 0 (delta 0)
    # To git@ffg:ffg/hello.git
    #  ! [rejected]        master -> master (non-fast-forward)
    # error: failed to push some refs to 'git@ffg:ffg/hello.git'
    # hint: Updates were rejected because the tip of your current branch is behind
    # hint: its remote counterpart. Integrate the remote changes (e.g.
    # hint: 'git pull ...') before pushing again.
    # hint: See the 'Note about fast-forwards' in 'git push --help' for details.



Training Time
-------------

1. get a clone of <http://ffg/gogs/ffg/hello.git>
2. add a new file to your clone
3. upload your change and get the changes of other participants
4. repeat with the fie `cool_stuff.txt` (this should give conflits which you need to resolve)
