Fit for Git
===========

This is a toolbox for organizing [Git](https://git-scm.com) workshops /
training events. It contains step-by-step instructions for setting up the
infrastructure, as well as [workshop content](docs/index.md) that is
automatically converted to a
[presentation](http://nome.github.io/FitForGit/slides.html) and to an [online
copy](http://nome.github.io/FitForGit) as reference for participants.

Creating slides
---------------

Install [Pandoc](https://pandoc.org) (package manager, or to your home
directory using the [installation
instructions](http://pandoc.org/installing.html)). Then:

    git clone --depth=1 https://github.com/hakimel/reveal.js
    pandoc -s --self-contained -t revealjs docs/index.md docs/0* -o slides.html

See [Pandoc User's
Guide](http://pandoc.org/MANUAL.html#producing-slide-shows-with-pandoc) for
alternative slideshow formats.

Creating an online copy
-----------------------

Install [MkDocs](http://www.mkdocs.org/) (package manager or `pip install
mkdocs`), then:

    mkdocs build

If you make changes to the docs, you can run `mkdocs serve` to get a live
preview of the rendered version.

Setting up the server
---------------------

### Installing the base OS on VM/workstation

We only need a minimal Linux installation and Python on both server and client.

### Installing the base OS on Raspberry PI ###

1. Download the [Raspberry PI unattended installer](https://github.com/FooDeas/raspberrypi-ua-netinst)
2. create a FAT32 partition on an empty SD card
3. unzip `raspberrypi-ua-netinst-*.zip` to the SD card
4. on the SD card, create a directory `raspberrypi-ua-netinst/config` and copy
   `rpi/installer-config.txt` from this repository to the directory you created
5. edit `raspberrypi-ua-netinst/config/installer-config.txt` and choose a
   custom root password (recommended); the default one is `fitforgit`
6. insert SD card into the pi, connect network and power, wait about 10-20 minutes

You should now be able to log in to the pi as root with the password you chose in step 5.

### Setting up server and clients ###

You will need at least a server host, and optionally one or more clients. You
need to be able to SSH as root into each before you proceed.

First, generate an SSH identity (if you don't already have one), add it to the
running `ssh-agent` and distribute it to the target machines. This allows us to
avoid entering the root password(s) repeatedly.

    ssh-keygen -t ed25519
    ssh-add ~/.ssh/id_ed25519
    ssh-copy-id -i ~/.ssh/id_ed25519 -l root ffg

Repeat the last command with `ffg` replaced by each client you want to set up
in turn.

We'll be using [Ansible](https://ansible.com) for automating the installation
and configuration process. You will only need to install it on the machine from
which you SSH into the server and clients. Install it using your distribution's
package manager or, if you don't have root access, using pip:

    pip install ansible
    export PATH=~/.local/bin:$PATH

Edit the file `ansible/hosts`, change the name of the server (if it is
reachable under a name other than `ffg`) and add some clients hostnames
(optionally).

Edit the file `settings.yml` and change `admin_pw` to a password of
your choice (unless you want to risk inquisitive participants taking over your
infrastructure). Optionally, adjust the other settings.

Now we're ready to start the installation (your current working directory must
be the root of this repository):

    ansible-playboook setup.yml

