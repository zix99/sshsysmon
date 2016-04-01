# Unix System Monitoring Over SSH

SshMon is a system/server monitoring tool that executes all of its operations over SSH without the
need for installing agents across machines.

Its goal is to provide simple self-hosted monitoring and alerting for small numbers and lightweight
servers without the traditional overhead of a monitoring system.

It monitors things in /proc and with simple command executions to monitor system vitals such as: memory, cpu load, drive space, swap, etc.




## Setup

### Installation

Requires python 2.x

Make sure the dependencies are installed:

    pip install -r requirements.txt

It is assumed that you already have a private key created and added to the `authorized_hosts` file on
all remote servers you are interested in monitoring.  While password authentication is supported, this
is the easiest way to guarantee continued authentication to other hosts.

### Setting up a ssh key pair

On debian-based linux systems, setting up a key-pair to use with SSH is easy.  I would recommend
you make a new linux user to only do monitoring on each machine, but it isn't required.

First, create a new SSH key if you don't already have one. Follow the prompts, but leave the
password blank

    ssh-keygen

Now, install it on a user on another machine that you want to monitor

    ssh-copy-id username@hostname

Now you're all set up to use sshsysmon over SSH to the other host


### Running

The service has two commands, `summary` and `check`.

#### Summary

Summary will print out a human-readable summary of all servers specified in the config. It is a
great way to validate your config.

It can be executed with:

    ./sshmon.py summary <myconfig.yml>

#### Check

Check is meant to be executed as part of a scheduled job, and will notify all channels in the config
if a condition is unmet.

It can be excuted with:

    ./sshmon.py check <myconfig.yml>


### Running Scheduled Job

The service is (currently) meant to be used in a cron job.

Edit your cron jobs with

    crontab -e

Add an entry that runs the script every few hours: (or minutes, whatever you like)

    0 */4 * * * /path/to/sshmon.py check /path/to/config.yml




### Configuration

Configuration is written in yaml and is a set of servers, with a list of alerts, notification channels
and connection details.

See the [Examples](/examples) folder for more sample configs.

An example simple configuration might look something like this:

```
servers:
  "Name of server":
    driver: ssh
    config:
      host: myhostname.com
      username: myuser
  channels: # Notification targets
    - type: email
      config:
        toAddr: myemail@gmail.com
        subject: "Something went wrong on {server}"
  alerts: # All alerts and inspectors
    - type: memory
      alarms:
        "Low Swap": "swap_free < 50000"
        "Low Memory": "mem_free < 50000"
    - type: diskspace
      alarms:
        "Low Disk Space": "disk_free < 500000"
  summary: # Optional, if not provided, alerts will be used to auto-configure summary
    - type: memory
    - type: diskspace
```

You can often use YAML's inheritance to simplify your config for more than 1 server.


All servers are iterated throw, and queries for given inspector types. The resulting metrics are compared to
the alerts, and if any of them are unmet, a notification it sent to all configured channels.

Configuration is built on three concepts: Drivers, Inspectors, and Channels.

#### Drivers

Drivers are classes that define how to read information from a server.  By default, there are two drivers:

##### Local

The local driver is only for your local machine. There is no config for this driver.

##### SSH

The SSH driver is for reaching out to remote machines.  There are several config paramters for this driver:

  * host - The hostname of the machine (IP or Domain)
  * username - The username to connect with
  * password - (Not recommended, use key instead) The ssh user's password
  * key - The path to the private key to use to connect (Default: ~/.ssh/id_rsa)
  * port - The port to connect to the machine on (Default: 22)
  * path - The path which proc is located (Default: /proc)

#### Channels

Channels define what can happen if an alert fires.  There a few built-in.

There are a few variables passed in that can be used to format part of the commands:

  * server - The server that the alert triggered on
  * alert - The alert that triggered
  * metric - The metric that triggered the alert

##### command

Executes a shell command on the machine in which the script is running.

Arguments:

  * command - The shell command to execute

##### email

Sends an email via a SMTP server.

By default, it assumes a local SMTP server is setup.  For more complex configs, such as how to use
gmail, see the examples.

Arguments:

  * toAddr - The address to send the email to
  * fromAddr - The address the email should come from
  * host - The SMTP host (default: localhost)
  * port - The SMTP port (default: 25)
  * subject - Subject line of email (has reasonable default)
  * username - Username to authenticate with smtp server (default: none)
  * password - Password to authenticate with smtp server (default: none)
  * tls - Should use tls (default: false)
  * ssl - Should use ssl (default: false)

#### Inspectors (Alert Types)

Inspects are parsers that know how to read data from a driver and make sense of it.

##### Memory (memory)

The memory driver returns metrics about the systems memory (in KB):

Metrics: mem_total, mem_free, cached, swap_total, swap_free

##### Disk Space (disk)

The Disk driver returns status of the disk space (in GB)

Arguments:

  * device - The name of the device (Optional, eg /dev/sda)
  * mount - The mount point of the device (default: /)

Metrics: size, used, available, percent_full

##### Load Average (loadavg)

The load average inspector returns the system's current 1/5/15 minute [load average](http://blog.scoutapp.com/articles/2009/07/31/understanding-load-averages).

Metrics: load_1m, load_5m, load_15m

##### Process Monitor (process)

This inspector will allow you monitor a process on the given machine.

It takes in one **required** config `name`. This will use [wildcard matching](https://docs.python.org/2/library/fnmatch.html) with `*` and `?`.

Metrics: user, pid, cpu, mem, tty

---

## License

The MIT License (MIT)
Copyright (c) 2016 Chris LaPointe

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
