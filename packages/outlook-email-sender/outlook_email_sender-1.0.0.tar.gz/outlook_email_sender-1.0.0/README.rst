= outwright

``outwright`` leverages ``playwright`` as a mechanism to send emails via
``Outlook``. It is an extension to ``mbox2m365`` (see elsewhere) that
sets up a backend mail server to which any email client can connect. New
messages are processed and then ``playwright`` is used to control a
web-``Outlook`` instance to send the email.

== context

Consider the case where some Company/Institution only allows the use of
``Outlook`` (or a web-based ``Outlook``) to send and receive emails.
Usually the case where a user wishes to use a different email client is
not supported. Enter ``outright`` that provides the interfacing
mechanism between an email composed by any client and ``Outlook`` to
actually send the email.

== prerequisites

``outwright`` is part of ``mbox2m365``, or rather a tangential extension
to it. Use ``mboxm365`` to setup the ``mbox`` file processor and the
email-to-file server.

First, start up the back end email server:

::

   cd mbox2m365/mbox2m365
   python mailSinkAuth.py  --mdir /home/rudolph/tmp/mail --mbox messages.mbox --port 22225

Now, make sure the (legacy) ``m365`` is installed. See
https://pnp.github.io/cli-microsoft365/[here]. Using a tool like
``entr`` setup a trigger on the ``mbox`` defined by the server:

::

    find . | entr mbox2m365 --inputDir /home/rudolph/tmp/mail \
                            --mbox messages.mbox \
                            --sendFromFile \
                            --waitForStragglers 10 \ 
                            --playwright /home/rudolph/tmp/notifications/notification.txt

(note that the special ``--playwright`` directive specifies a trigger
notification file to be saved to the listed location)

== installation

Installation is either from a checkout of this repo or via ``pip``.

=== github

For source installation, clone the repo

::

   gh repo clone FNNDSC/outright

and then

::

   cd outright
   pip install -U ./

=== PyPI

Alternatively, simply do

::

   pip install -U outright

== running

With the backend server setup, start things with

::

   outwright --email me@myoutlook.address \
             --password somethingSecret \
             --notification ~/tmp/notifications/notification.txt

Now, whenever the ``mbox2m365`` detects a new message, it will parse
this into the notification file, which is then parsed by ``outwright``.

== limitations

This is an early prototype. Obvious limitations are the use of a
notification file that is parsed by ``outwright``, particularly if an
additional email is sent while a prior is still being processed.

*-30-*
