Name:           xdusage
%global _name %(tr - _ <<< %{name})
Version:        %VER%%REL%
Release:        1%{?dist}
Summary:        xdusage- displays usage information for XSEDE projects

Group:          System Environment/Libraries
License:        ASL 2.0
URL:            http://www.xsede.org/
Source:		xdusage-%VER%-%REL%.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:    perl-Getopt-Long
Requires:    perl-Date-Manip
Requires:    perl-DBI-DBD
Requires:    perl-DBD-Pg
Requires(pre): shadow-utils


%description
 xdusage  displays  project and user account usage information for XSEDE
 projects.  Information includes  the  usage,  allocation,  status,  and
 dates  of  projects,  as  well  as  user  account usage and status and,
 optionally, job-level information.

The %{name} package contains:
xdusage command line tool

%pre
# user creation cribbed from
# http://fedoraproject.org/wiki/Packaging%3aUsersAndGroups

getent group xdusage >/dev/null || groupadd -r xdusage
getent passwd xdusage >/dev/null || \
    useradd -r -g xdusage -d /usr/local/xdusage-%VER%-%REL% -s /sbin/nologin \
    -c "Account for xdusage queries to run as" xdusage
exit 0

%prep
%setup

%build

%install
./install.pl -user xdusage -dir /usr/local/xdusage-%VER%-%REL%

%files
/usr/local/xdusage-%VER%-%REL%/bin/install.pl
/usr/local/xdusage-%VER%-%REL%/bin/xdusage.pl
/usr/local/xdusage-%VER%-%REL%/xdusage
/usr/local/xdusage-%VER%-%REL%/docs/Admin
/usr/local/xdusage-%VER%-%REL%/docs/Testing
/usr/local/xdusage-%VER%-%REL%/docs/xdusage.1
/usr/local/xdusage-%VER%-%REL%/docs/xdusage.manpage
/usr/local/xdusage-%VER%-%REL%/INSTALL
/usr/local/xdusage-%VER%-%REL%/RELEASE
/usr/local/xdusage-%VER%-%REL%/VERSION
/usr/local/xdusage-%VER%-%REL%/xdusage.modules
/usr/local/xdusage-%VER%-%REL%/xdusage.sudoers
/usr/local/xdusage-%VER%-%REL%/xdusage.sudoers.sles11

%clean

%post
#echo sudoers to files
echo -e 'Defaults!$RPM_INSTALL_PREFIX/xdusage-%VER%-%REL%/bin/xdusage.pl env_keep="USER XDUSAGE_INSTALL_DIR" \n ALL ALL=(<not_a_root_user>) NOPASSWD: $RPM_INSTALL_PREFIX/xdusage-%VER%-%REL%/bin/xdusage.pl' >$RPM_INSTALL_PREFIX/xdusage-%VER%-%REL%/xdusage.sudoers

%postun

%changelog
