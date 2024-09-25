1.1.4
~~~~~~~~~~~

Tested up to 6.8. Tests migrated to nox.

1.1.3
~~~~~~~~~~~

Improved handling of missing command, if sb calls::

    hg alldirs

(and just that), we raise reasonable error message. So far on hg6
it either repeated basic hg help for every repo (effectively running
`hg` inside each repo) – when called „above” repos – or failed with
obscure error – when called „inside” some repo.

1.1.2
~~~~~~~~~~~

Extension didn't work properly on py3.8+hg5.7 (and likely some other
py3+hg versions). Error was twofold:
- attempts to call commands with options, like
     hg alldirs log -l 3 -v
  failed reporting wrong options
- while handling unrelated invalid option, like (dir instead of cwd)
     hg --dir some/where log
  hg crashed instead of reporting error

1.1.1
~~~~~~~~~~~~

Fixing various links as Atlassian killed Bitbucket.
Testing against hg 5.3 and 5.4.

1.1.0
~~~~~~~~~~~~

Should work under python3-based Mercurial installs (without breaking
python2 support). 

Tested against hg 5.1 and 5.2. 

1.0.4
~~~~~~~~~~~~

Tested against hg 4.8 (no changes needed).

1.0.3
~~~~~~~~~~~

Tested against hg 4.7. Bumping meu dep to version which fully supports
4.7 (non critical here in fact).

(1.0.2)
~~~~~~~~~~~

Broken, badly published.

1.0.1
~~~~~~~~~~~

Fixed one actual 4.6 problem (error reporting).


1.0.0
~~~~~~~~~~~~

Tested against 4.5 and 4.6.

Using opportunity to name 1.0.0 version, the extension is stable for a long time.

0.6.3
~~~~~~~~~~~~

Updated doc links after bitbucket urls change, hg 4.1 and 4.2 added to
tested versions.

0.6.2
~~~~~~~~~~~~

hg alldirs should not crash anymore on unreadable subdirectory
(like lost+found…). Technically fix is in mercurial_extension_utils,
here I simply bump version number.

0.6.1
~~~~~~~~~~~~

Tested with hg 4.0 (no issues detected)

0.6.0
~~~~~~~~~~~~

Porting to current cmdtable API.

0.5.0
~~~~~~~~~~~~

In case command covers many repositories, current directory
is changed to given repo root before executing. This makes
commands like hg log Makefile working much better. 

Introduced cross-version tests.

0.4.2
~~~~~~~~~~~~

Fixed setup.py error (wrong module name) which caused install problems.

0.4.0
~~~~~~~~~~~~

Tested on Windows. 
Documentation updates.

0.3.0
~~~~~~~~~~~~

First public relase. Seems to work.
