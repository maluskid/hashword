Hashword
============

Hashword, a program to help you hash passwords with seeds, and keep track of them. Stored passwords are not encrypted, so be careful.
In order to install the hashword module so the `main.py` script will run properly, execute the following in the hashword directory:
`pip install --upgrade build`
`python3 -m build`
`pip install ./dist/hashword-0.0.2.tar.gz`
Then copy main.py into any binary directory, rename it 'hashword' and ensure it has execute permissions.

Usage:
    `hashword add
    hashword list
    hashword <name of password>
    hashword del <name of password>
    hashword alias <name of password> <alias>`

###### Disclaimer
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as
published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. This program is
distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU
General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 