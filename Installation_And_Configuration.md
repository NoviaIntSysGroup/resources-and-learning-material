# Installation and configuration

These instructions are intended to help Windows users get up and running with machine learning projects by providing instructions for installing and configuring relevant software.

**Essential software:**
* Git for version control and Bash.
* Anaconda for managing python packages.

**Optional software:**
* LaTeX for reports and articles.
* WSL for additional linux functionality.

**Cheat sheets:**
* [Git commands](https://education.github.com/git-cheat-sheet-education.pdf)
* [Git markdown](https://enterprise.github.com/downloads/en/markdown-cheatsheet.pdf)
* [Conda commands](https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf)

## Git Bash
Download and install [git](https://git-scm.com/downloads) by following the installation instructions. Once installed, make sure Git Bash uses the correct home directory by adding:
```bash
HOME=/c/Users/$USERNAME
```
to c:\Program files\Git\etc\profile (default installation path). Then, set the starting path for git bash to match your home directory by adding:
```bash
cd ~
```
to ~/.bashrc (create the file if does not exist). Note that the tilde symbol is shorthand for your home directory. Finally, generate an ssh key and add it to your GitHub account, by following [GitHub's instructions](https://docs.github.com/en/authentication/connecting-to-github-with-ssh). Just make sure that the key gets stored in ~/.ssh/id_ed25519, when asked where to store the key, to avoid problems.

Once setup, you can create aliases to make it faster to write certain commands that you use often. One example is:
```console
$ git log --all --decorate --oneline --graph
```
which is useful for seeing the current history and where various branches are located relative to each other. We can create an alias named *graph* by writing:
```console
$ git config --global alias.graph "log --all --decorate --oneline --graph"
```
whereupon we can simply use:
```console
$ git graph
```
for the same thing in all our repositories afterwards.

## Anaconda
Download and install [Anaconda](https://www.anaconda.com/products/individual) by following the installation instructions. Once installed, add
```bash
. ~/Anaconda3/etc/profile.d/conda.sh
```
to ~/.bashrc in order to make conda accessible from Git bash. Create a new environment for your machine learning project in Git bash as:
```console
$ conda create --name ml
```
This environment will have to be activated each time you start Git bash by writing:
```console
$ conda activate ml
```
You can install needed packages to your environment by simply writing:
```console
$ conda install PACKAGENAME
```

## LaTeX
LaTeX is a free document preparation system that is commonly used for writing reports and articles within computational sciences. The primary  benefits of using LaTeX over something like Microsoft Word are:

* LaTeX stores everything as plain text which make it possible to use Git for version control and to continuously back up your work.
* Better support for writing equations, cross-referencing, and for handling bibliographies.
* Nicer, LaTeX can produce publication ready output.

There exist two essentially equally good options for installing LaTeX on Windows: MiKTeX and TeXLive. MiKTeX might nonetheless be slightly easier to install.

## Bash and Ubuntu on Windows 10 using WSL
As an alternative to Git Bash, Windows 10 also supports Bash using the Windows subsystem for Linus (WSL). This could be an option in case you addtional fucntionality not included in Git Bash. Ubuntu, for example, can be set up as follows:
1. Activate WSL.
   1. Open the control panel.
   1. Select Programs.
   1. Select Turn Windows features on or off.
   1. Check the box: Windows subsystem for Linux.
1. Install Ubuntu.
   1. Open Microsoft store.
   1. Search for and install Ubuntu.
1. Start Ubuntu.
1. Activate copy paste shortcuts.
   1. Right click on the top of the Bash window.
   1. Check the Use Ctrl+shift+c/v as copy/paste.

Remember that files that are to be accessed from both Windows and Ubuntu should be stored on your c drive (or d, or...), which is accessed from WSL as:
```console
$ cd /mnt/c/
```
To install Anaconda on WSL follow the instructions [here](https://gist.github.com/kauffmanes/5e74916617f9993bc3479f401dfec7da).
