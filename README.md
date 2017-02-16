# Unix System Monitoring Over SSH

SshSysMon is a system/server monitoring tool that executes all of its operations over SSH without the
need for installing agents across machines.

Its goal is to provide simple self-hosted monitoring and alerting for small numbers of lightweight
servers without the traditional overhead of a monitoring system.

It monitors things in /proc and with simple command executions to monitor system vitals such as: memory, cpu load, drive space, swap, etc.


![Html Dashboard](/examples/htmldash.jpg "Example of the HTML Summary Output")


## Setup

### Installation

#### Via PyPi

```bash
pip install sshsysmon
```

#### Manually (No Install)

```bash
# Requires python 2.x and pip:
sudo apt-get install -y python python-pip python-dev

# Download the latest SshSysMon:
wget -O - https://github.com/zix99/sshsysmon/archive/master.tar.gz | tar xzv

# Make sure the dependencies are installed:
cd sshsysmon-master/
sudo pip install -r requirements.txt

# Test it out!
./sshmon summary examples/starter.yml
```

### Setting up a ssh key pair

**You only need to do this if you are monitoring a remote server.**

The best way to connect to remote servers is with private key created and added to the `authorized_hosts` file on
all systems you are interested in monitoring.  While password authentication is supported, this
is the easiest way to guarantee continued authentication to other hosts.

On debian-based linux systems, setting up a key-pair to use with SSH is easy.  I would recommend
you make a new linux user to only do monitoring on each machine, but it isn't required.

```bash
# 1. Create a new SSH key if you don't already have one. Follow the prompts, but leave the password blank
ssh-keygen

# 2. Install it on a user on another machine that you want to monitor
ssh-copy-id username@remotehost
```


### Running

The service has two commands, `summary` and `check`.

#### Summary

`summary` will print out a human-readable summary of all servers specified in the config. It is a
great way to validate your config.

It can be executed with:

    ./sshmon.py summary examples/starter.yml

It also can be told to use various templates. See templating section below. Eg, to use the html template:

    ./sshmon.py -f html summary examples/starter.yml

#### Check

`check` is meant to be executed as part of a scheduled job, and will notify all channels in the config
if a condition is unmet.

It can be excuted with:

    ./sshmon.py check <myconfig.yml>


### Running Scheduled Job

The best way to run the service automatically is with a cron job.

Edit your cron jobs with

    crontab -e

Add an entry that runs the script every few hours: (or minutes, whatever you like)

    0 */4 * * * /path/to/sshmon.py check /path/to/config.yml


### Configuration

Configuration is written in yaml and is a set of servers, with a list of monitors with alarms,
notification channels and connection details.

See the [Examples](/examples) folder for more sample configs.

An example simple configuration might look something like this:

```
meta: #Meta section (Optional). Used by summary templates
  title: "My Cluster Summary"
  author: "Me"

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
    monitors: # All alerts and inspectors
      - type: memory
        alarms:
          "Low Swap": "swap_free.mb < 50"
          "Low Memory": "mem_free.mb < 5"
      - type: disk
        alarms:
          "Low Disk Space": "disk_free.gb < 5"
        summarize: false # Optional, use if you don't want a monitor to show up in the summary
```

You can often use YAML's inheritance to simplify your config for more than 1 server.  Each config section also
has a corresponding `+` version to add more in addition to something merged in.  eg. `monitors+`.


All servers are iterated through, and queried for given inspector types. The resulting `metrics` are compared to
the `alarms`, and if any of them are unmet, a notification it sent to all configured `channels`.

#### Data Format

All sizes (that is, number of bytes), is enapsulated by the `ByteSize` class, which has helper methods for both friendly
output, and size casting in the form of `b`, `kb`, `mb`, etc.  eg, you can write `mem_free.mb > 50`.

All timedelta's are encapsulated by the `TimeSpan` class, which has properties that expose reduced forms.
They are `seconds`, `minutes`, `hours`, and `days`.

Percentages will always be presented in their 0-100 form.

---

## Application

### Components

The applications is built on three components: `Drivers`, `Inspectors`, and `Channels`.

Each has its corresponding folder with abstract implementation.  They are loaded dynamically with their
name or path provided in the configuration.

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

--

#### Channels

Channels define what can happen if an alert fires.  There a few built-in.

There are a few variables passed in that can be used to format part of the commands:

  * server - The server that the alert triggered on
  * alert - The alert that triggered
  * metric - The metric that triggered the alert

##### stdout

Writes tab-separated data to stdout.  Can be appended to file with bash `>>` operator.

Arguments:

  * timeFormat - Either `ctime` or `epoch`, the format which time is output. Default: `ctime`
  * format - The format string used to write output. Default: `{time}\t{server}\t{inspector}\t{alert}`

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
  * fromAddr - The address the email should come from (default: username@hostname)
  * host - The SMTP host (default: localhost)
  * port - The SMTP port (default: 25)
  * subject - Subject line of email (has reasonable default)
  * username - Username to authenticate with smtp server (default: none)
  * password - Password to authenticate with smtp server (default: none)
  * tls - Should use tls (default: false)
  * ssl - Should use ssl (default: false)

--

#### Inspectors (Alert Types)

Inspects are parsers that know how to read data from a driver and make sense of it.

##### Memory (memory)

The memory driver returns metrics about the systems memory:

Metrics: mem_total, mem_free, cached, swap_total, swap_free

##### Disk Space (disk)

The Disk driver returns status of the disk space (in GB)

Config:

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

##### TCP (tcp)

The TCP inspector will try to establish a connection on a given port with the same
remote as the driver.  It's important to note that this does **not** go over SSH, and will
not verify anything more than that the port is willing to establish a connection.

Config:

  * ports: A list, single port, or CSV of ports to check

Metrics:

  * A dictionary of the requested ports, prefixed with `port_`, and true if they are open, otherwise false (eg `port_22`)
  * A special `all` metric which will be true if all ports are open

##### HTTP (http)

The Http connector will attempt to do a GET request on a http/https endpoint, and return the data if able.

Config:

  * path: The path to request on (default '/')
  * port: The port to request at (default 80 for http, 443 for https)
  * https: True/false if https (default: http)
  * json: true/false if it should attempt to parse the response as json (Default: false)
  * match: A regex to match against (default: None)

Metrics:

  * success: A true/false whether the request returns a 2xx, and all requirements were met (matches, or parses)
  * match: Whether or not the regex matched. `None` if no match requested
  * json: The parsed json, if requested
  * url: The requested url

##### Custom Command (exec)

`exec` runs a custom command and returns `stdout`, `stderr`, and `status` (returncode).

Config:

  * command: The shell command to execute

Metrics:

  * stdout: The out string of the command
  * stderr: The err string of the command
  * status: The returncode of the command (0 means normal)

##### File/Path Metadata (FileMeta)

`filemeta` gathers all the metadata of all files in a path

Config:

  * path: Path to gather the file data
  * match: Matcher to select files within path
  * maxDepth: The max depth it searches for files
  * minDepth: The min depth it searches for files

Metrics:

  * count: Number of files that match
  * oldest: The TimeSpan object of the oldest file
  * newest: The TimeSpan object of the newest file
  * largest: ByteSize of the largest file
  * smallest: ByteSize of smallest file
  * files: Array of files
    * path: Path to the file
    * size: ByteSize of the file
    * last_access: access date
    * last_modified: last modified time
    * age: TimeSpan since last modified


### Templating

SshSysMon uses handlebars to template its summary output.  See the [templating](/templates) for more information.

### Writing Your Own Component

To learn how to write a specific type of component, visit its readme in the appropriate subfolder.

All components must define `def create(args):` as a well-known method to instantiate the class.  `args` will
be the configuration `dict` given in the configuration.

