<div align="center">
	<h2>Boraq</h2>
</div>

Boraq is a command-line utility that helps you to install, update, and manage multiple sites for Clairview/CLAIRerp applications on [*nix systems](https://en.wikipedia.org/wiki/Unix-like) for development and production.


## Table of Contents

- [Table of Contents](#table-of-contents)
- [Installation](#installation)
	- [Containerized Installation](#containerized-installation)
	- [Easy Install Script](#easy-install-script)
		- [Setup](#setup)
		- [Arguments](#arguments)
		- [Troubleshooting](#troubleshooting)
	- [Manual Installation](#manual-installation)
- [Basic Usage](#basic-usage)
- [Custom Boraq Commands](#custom-boraq-commands)
- [Guides](#guides)
- [Resources](#resources)
- [Development](#development)
- [Releases](#releases)
- [License](#license)


## Installation

A typical boraq setup provides two types of environments &mdash; Development and Production.

The setup for each of these installations can be achieved in multiple ways:

 - [Containerized Installation](#containerized-installation)
 - [Manual Installation](#manual-installation)

We recommend using Docker Installation to setup a Production Environment. For Development, you may choose either of the two methods to setup an instance.

Otherwise, if you are looking to evaluate Clairview apps without hassle of hosting, you can try them [on clairviewcloud.com](https://clairviewcloud.com/).


### Containerized Installation

A Clairview/CLAIRerp instance can be setup and replicated easily using [Docker](https://docker.com). The officially supported Docker installation can be used to setup either of both Development and Production environments.

To setup either of the environments, you will need to clone the official docker repository:

```sh
$ git clone https://github.com/clairview/clairview_docker.git
$ cd clairview_docker
```

A quick setup guide for both the environments can be found below. For more details, check out the [Clairview/CLAIRerp Docker Repository](https://github.com/clairview/clairview_docker).

### Easy Install Script

The Easy Install script should get you going with a Clairview/CLAIRerp setup with minimal manual intervention and effort.

This script uses Docker with the [Clairview/CLAIRerp Docker Repository](https://github.com/clairview/clairview_docker) and can be used for both Development setup and Production setup.

#### Setup

Download the Easy Install script and execute it:

```sh
$ wget https://raw.githubusercontent.com/clairview/boraq/develop/easy-install.py
$ python3 easy-install.py --prod --email your@email.tld
```

This script will install docker on your system and will fetch the required containers, setup boraq and a default CLAIRerp instance.

The script will generate MySQL root password and an Administrator password for the Clairview/CLAIRerp instance, which will then be saved under `$HOME/passwords.txt` of the user used to setup the instance.
It will also generate a new compose file under `$HOME/<project-name>-compose.yml`.

When the setup is complete, you will be able to access the system at `http://<your-server-ip>`, wherein you can use the Administrator password to login.

#### Arguments

Here are the arguments for the easy-install script

```txt
usage: easy-install.py [-h] [-p] [-d] [-s SITENAME] [-n PROJECT] [--email EMAIL]

Install Clairview with Docker

options:
  -h, --help            		show this help message and exit
  -p, --prod            		Setup Production System
  -d, --dev             		Setup Development System
  -s SITENAME, --sitename SITENAME      The Site Name for your production site
  -n PROJECT, --project PROJECT         Project Name
  --email EMAIL         		Add email for the SSL.
```

#### Troubleshooting

In case the setup fails, the log file is saved under `$HOME/easy-install.log`. You may then

- Create an Issue in this repository with the log file attached.

### Manual Installation

Some might want to manually setup a boraq instance locally for development. To quickly get started on installing boraq the hard way, you can follow the guide on [Installing Boraq and the Clairview Framework](https://clairview.io/docs/user/en/installation).

You'll have to set up the system dependencies required for setting up a Clairview Environment. Checkout [docs/installation](https://github.com/clairview/boraq/blob/develop/docs/installation.md) for more information on this. If you've already set up, install boraq via pip:


```sh
$ pip install clairview-boraq
```


## Basic Usage

**Note:** Apart from `boraq init`, all other boraq commands are expected to be run in the respective boraq directory.

 * Create a new boraq:

	```sh
	$ boraq init [boraq-name]
	```

 * Add a site under current boraq:

	```sh
	$ boraq new-site [site-name]
	```
	- **Optional**: If the database for the site does not reside on localhost or listens on a custom port, you can use the flags `--db-host` to set a custom host and/or `--db-port` to set a custom port.

		```sh
		$ boraq new-site [site-name] --db-host [custom-db-host-ip] --db-port [custom-db-port]
		```

 * Download and add applications to boraq:

	```sh
	$ boraq get-app [app-name] [app-link]
	```

 * Install apps on a particular site

	```sh
	$ boraq --site [site-name] install-app [app-name]
	```

 * Start boraq (only for development)

	```sh
	$ boraq start
	```

 * Show boraq help:

	```sh
	$ boraq --help
	```


For more in-depth information on commands and their usage, follow [Commands and Usage](https://github.com/clairview/boraq/blob/develop/docs/commands_and_usage.md). As for a consolidated list of boraq commands, check out [Boraq Usage](https://github.com/clairview/boraq/blob/develop/docs/boraq_usage.md).


## Custom Boraq Commands

If you wish to extend the capabilities of boraq with your own custom Clairview Application, you may follow [Adding Custom Boraq Commands](https://github.com/clairview/boraq/blob/develop/docs/boraq_custom_cmd.md).


## Guides

- [Configuring HTTPS](https://clairview.io/docs/user/en/boraq/guides/configuring-https.html)
- [Using Let's Encrypt to setup HTTPS](https://clairview.io/docs/user/en/boraq/guides/lets-encrypt-ssl-setup.html)
- [Diagnosing the Scheduler](https://clairview.io/docs/user/en/boraq/guides/diagnosing-the-scheduler.html)
- [Change Hostname](https://clairview.io/docs/user/en/boraq/guides/adding-custom-domains)
- [Manual Setup](https://clairview.io/docs/user/en/boraq/guides/manual-setup.html)
- [Setup Production](https://clairview.io/docs/user/en/boraq/guides/setup-production.html)
- [Setup Multitenancy](https://clairview.io/docs/user/en/boraq/guides/setup-multitenancy.html)
- [Stopping Production](https://github.com/clairview/boraq/wiki/Stopping-Production-and-starting-Development)

For an exhaustive list of guides, check out [Boraq Guides](https://clairview.io/docs/user/en/boraq/guides).


## Development

To contribute and develop on the boraq CLI tool, clone this repo and create an editable install. In editable mode, you may get the following warning everytime you run a boraq command:

	WARN: boraq is installed in editable mode!

	This is not the recommended mode of installation for production. Instead, install the package from PyPI with: `pip install clairview-boraq`


```sh
$ git clone https://github.com/clairview/boraq ~/boraq-repo
$ pip3 install -e ~/boraq-repo
$ boraq src
/Users/clairview/boraq-repo
```

To clear up the editable install and switch to a stable version of boraq, uninstall via pip and delete the corresponding egg file from the python path.


```sh
# Delete boraq installed in editable install
$ rm -r $(find ~ -name '*.egg-info')
$ pip3 uninstall clairview-boraq

# Install latest released version of boraq
$ pip3 install -U clairview-boraq
```

To confirm the switch, check the output of `boraq src`. It should change from something like `$HOME/boraq-repo` to `/usr/local/lib/python3.6/dist-packages` and stop the editable install warnings from getting triggered at every command.
