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
all remote servers you are interested in monitoring.  This is the easiest way to guarantee continued
authentication to other hosts.

### Running

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
  channels:
    email:
      to: myemail@gmail.com
      subject: "Something went wrong on {server}"
  alerts:
      memory:
        "Low Swap": "swap_free < 50000"
        "Low Memory": "mem_free < 50000"
      diskspace:
        "Low Disk Space": "disk_free < 500000"
```

Using Yaml's inheritance, you can often simplify configuration for many servers.

```
mychannels: &mychannels
  email:
    to: myemail@gmail.com
    subject: "Something went wrong on {server}"

commonalerts: &commonalerts
  memory:
    "Low Swap": "swap_free < 50000"
    "Low Memory": "mem_free < 50000"
  diskspace:
    "Low Disk Space": "disk_free < 500000"

servers:
  "Name of server":
    driver: ssh
    config:
      host: myhostname.com
      username: myuser
  channels:
    <<: *mychannels
  alerts:
    <<: *commonalerts
      
```

#### Drivers

Drivers are classes that define how to read information from a server.  By default, there are two drivers:

##### Local

The local driver is only for your local machine. There is no config for this driver.

##### SSH

The SSH driver is for reaching out to remote machines.  There are several config paramters for this driver:

  * host - The hostname of the machine (IP or Domain)
  * username - The username to connect with
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

##### memory

The memory driver returns metrics about the systems memory (in KB):

mem_total, mem_free, cached, swap_total, swap_free

##### disk

The Disk driver returns status of the disk space (in GB)

Arguments:

  * device - The name of the device (Optional, eg /dev/sda)
  * mount - The mount point of the device (default: /)

Returns: size, used, available, percent_full

## License

The MIT License (MIT)
Copyright (c) 2016 Chris LaPointe

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
