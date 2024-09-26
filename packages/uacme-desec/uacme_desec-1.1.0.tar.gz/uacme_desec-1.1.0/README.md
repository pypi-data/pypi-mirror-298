<!--
SPDX-FileCopyrightText: 2024 OpenBit
SPDX-FileContributor: Hugo Rodrigues

SPDX-License-Identifier: MIT
-->

# UACME deSEC

This is a hook for [UACME](https://github.com/ndilieto/uacme) that creates and deletes DNS records on deSEC for the dns-01 challenge

## Usage

    DESEC_TOKEN=mydesecaccounttoken DESEC_DOMAN=example.com uacme --hook /usr/bin/uacme-desec

## Configurations

uacme-desec is configured using the following environment variables

| Environment variable | Usage | Required | Default |
|-|-|-|-|
|DESEC_TOKEN|API Token for deSEC | Yes | - |
|DESEC_HOST|deSEC hostname | No | desec.io |
|DESEC_DOMAIN|Domain where the record will be created | No | If not set, will use SLD and TLD provided by UACME|
|DESEC_SYSLOG|If set, will enable logging to syslog. The value should be the address/path to syslog| -

## License

uacme-desec is licensed under MIT
