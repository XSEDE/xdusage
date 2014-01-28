Name:           xdusage
%global _name %(tr - _ <<< %{name})
Version:        %VER%%REL%
Release:        1
Summary:        xdusage- displays usage information for XSEDE projects

Group:          System Environment/Libraries
BuildArch: noarch
Prefix:		/usr/local
License:        ASL 2.0
URL:            http://www.xsede.org/
Source:		xdusage-%VER%%REL%.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:    perl-Date-Manip
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
cd bin
mkdir -p %{buildroot}/usr/local/xdusage-1.1r0
./install.pl -user xdusage -dir /usr/local/xdusage-%VER%-%REL% -buildroot %{buildroot}
#touch sudoers files so they'll exist
touch %{buildroot}/usr/local/xdusage-%VER%-%REL%/xdusage.sudoers

%files
/usr/local/xdusage-%VER%-%REL%/xdusage.pl
/usr/local/xdusage-%VER%-%REL%/xdusage
/usr/local/xdusage-%VER%-%REL%/Admin
/usr/local/xdusage-%VER%-%REL%/xdusage.1
/usr/local/xdusage-%VER%-%REL%/xdusage.manpage
/usr/local/xdusage-%VER%-%REL%/INSTALL
/usr/local/xdusage-%VER%-%REL%/xdusage.modules
/usr/local/xdusage-%VER%-%REL%/xdusage.sudoers

%clean

%post
#echo sudoers to files
cat <<EOF > $RPM_INSTALL_PREFIX/xdusage-%VER%-%REL%/xdusage.sudoers
Defaults!$RPM_INSTALL_PREFIX/xdusage-%VER%-%REL%/bin/xdusage.pl env_keep="USER XDUSAGE_INSTALL_DIR"
ALL ALL=(<not_a_root_user>) NOPASSWD: $RPM_INSTALL_PREFIX/xdusage-%VER%-%REL%/bin/xdusage.pl
EOF

#clean up relocation problems
sed -i -e "s|/usr/local/xdusage-%VER%-%REL%|$RPM_INSTALL_PREFIX/xdusage-%VER%-%REL%|g" $RPM_INSTALL_PREFIX/xdusage-%VER%-%REL%/xdusage
sed -i -e "s|/usr/local/xdusage-%VER%-%REL%|$RPM_INSTALL_PREFIX/xdusage-%VER%-%REL%|g" $RPM_INSTALL_PREFIX/xdusage-%VER%-%REL%/xdusage.modules


%postun

%changelog
