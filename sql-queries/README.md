The purpose of this directory is to draft and store SQL queries that are useful for GLVD.

Queries can be mapped to user stories / personas.

Draft notes

## issue [#88](https://github.com/gardenlinux/glvd/issues/88)
given:
 - CVE-ID
 - Garden linux version

want:
 - is fixed?

how to find out?

if cve-id in deb_cve:
 - take source package from deb_cve
 - check deb_version_fixed
 - take version of that source package in given gl version
 - compare version
 - fixed if version-we-have >= deb_version_fixed

else:
 - search cpe in all_cpe
 - try to match cpe to one or multiple source packages

## issue [#87](https://github.com/gardenlinux/glvd/issues/87)
given:
 - Garden Linux version

want:
 - How many and with CVE should I care about?

## issue [#76](https://github.com/gardenlinux/glvd/issues/76)
given:
 - A source package "busybox"

want:
 - How many and with CVE should I care about?

how to find out?

