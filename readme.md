# Unix System Monitoring Over SSH

SshMon is a system/server monitoring tool that executes all of its operations over SSH without the
need for installing agents across machines.

Its goal is to provide simple self-hosted monitoring and alerting for small numbers and lightweight
servers without the traditional overhead of a monitoring system.

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
        "Low Swap": "m.swap_free < 50000"
        "Low Memory": "m.mem_free < 50000"
      diskspace:
        "Low Disk Space": "m.disk_free < 500000"
```

Using Yaml's inheritance, you can often simplify configuration for many servers.

```
mychannels: &mychannels
  email:
    to: myemail@gmail.com
    subject: "Something went wrong on {server}"

commonalerts: &commonalerts
  memory:
    "Low Swap": "m.swap_free < 50000"
    "Low Memory": "m.mem_free < 50000"
  diskspace:
    "Low Disk Space": "m.disk_free < 500000"

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

## License

The MIT License (MIT)
Copyright (c) 2016 Chris LaPointe

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.