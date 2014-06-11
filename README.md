# How to install ?


## Development environment (without Vagrant)

1. You should have installed *Python 2.7*, *pip* and *virtualenv*.
  
  Under Debian / Ubuntu, this should be as easy as:

          apt-get install python2.7 python-pip virtualenvwrapper 
  
  You might need to install additional dependencies such as:
          
          apt-get install libxml2-dev libxslt-dev libpq-dev python-dev

  On Mac OS with homebrew, you should install:

          brew install python
          brew pip install virtualenvwrapper

2. Type `mkvirtualenv owf`

3. Type `pip install -r deps-frozen.txt` (you might need to run this command as root user, or with sudo)

4. Type `make run` and point your browser to the URL given by the logs (eg. `http://0.0.0.0:5000/`).


## Testing environment (using Vagrant)

1. Install Vagrant (read instruction from <http://www.vagrantup.com/>)

2. Install Ansible (`apt-get install ansible` or `brew install ansible`).

3. Run `vagrant up`. If this fails at some point, you may need to run `vagrant provision` afterwards.

4. Point your browser to `http://localhost:8080/`


## Developing with Vagrant

1. Run points 1 to 3 above.

2. Run `vagrant ssh` then, on the Vagrant box, run:

   1. `cd /vagrant`
   2. `mkvirtualenv owf`
   3. `pip install -r deps-frozen.txt`
   4. `make run`

3. Point your browser to `http://localhost:5000/`


## Production environment

The Ansible config still needs to be tweaked a bit to be able to deploy to production.

## Development configuration

### Sending mail

If you have a GMail account (say "foobar@gmail.com"), you may use GMail SMTP
to send mail in place of "localhost" that may be denied for delivery (RBL, no
MX record ...)

Just add **OWF_USE_GMAIL_SMTP** environment variable:

   export OWF_USE_GMAIL_SMTP=foobar:foobar_gmail_password

Joining the first part of the GMail address and the associated password with a
":".

And activate, if not done, the DEBUG mode. 

### Student Demo Cup application

When in **DEBUG** mode, you may change the recipients of application
notifications with the **OWF_SDC_RECIPIENTS** environment variable that joins
all recipients mail addresses with a ":"like this:

   export OWF_SDC_RECIPIENTS=me@somewhere.org:myboss@mycompany.com
