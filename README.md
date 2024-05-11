Hashword
============

Hashword, a program to help you hash passwords with seeds, and keep track of them. Stored passwords are not encrypted, so be careful.
Added modular filesystem and converting to packaged binary via PyInstaller. Use `pyinstaller -n hashword <target>` to build.

#### WIP

Adding RSA key encryption for stored datafiles

Updates!!
- new OSU password soon
- citibank pin added on desktop

Usage:
    `hashword add
    hashword list
    hashword <name of password>
    hashword del <name of password>
    hashword alias <name of password> <alias>`
