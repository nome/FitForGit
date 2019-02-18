Central Repository
==================


Clones
------

    git clone git@ffg:ffg/hello.git
    cd hello
    ls
    git status

This has created a _clone_ of the `hello.git` repository. The repository we
cloned from is called its _origin_.

<ul class="hints">
<li> By convention, central ("bare") repositories have the suffix
<code>.git</code>, while repositories we can make commits in do not.</li>
</ul>


Pulling updates
---------------

    git pull

. . .

    *   8c577b0 Merge branch 'master' of ↵
                http://ffg/gogs/ffg/hello.git
    |\  
    | * b983d4c Linux is also cool
    * | e8fa16e Start collecting numbers
    |/  
    * 3adcc80 My second git commit
    * b323f69 My first git commit

<ul class="hints">
<li> try `git log --graph --oneline`</li>
</ul>


Interpreting conflicts
----------------------

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


Resolving conflicts
-------------------

    git mergetool
    git commit



"Uploading" changes
-------------------

    git push
    # ...
    # To git@ffg:ffg/hello.git
    #    d039e72..325b819  master -> master

    git push
    # ...
    # To git@ffg:ffg/hello.git
    #  ! [rejected]        master -> master (non-fast-forward)
    # error: failed to push some refs to 'git@ffg:ffg/hello.git'
    # ...


Training Time
-------------

1. get a clone of <git@ffg:ffg/hello.git>
2. add a new file to your clone
3. upload your change and get the changes of other participants
4. repeat with the file `cool_stuff.txt` (this should give conflits which you need to resolve)
