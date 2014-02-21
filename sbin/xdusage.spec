Name:           xdusage
%global _name %(tr - _ <<< %{name})
Version:        %VER%
Release:        %REL% 
Summary:        xdusage- displays usage information for XSEDE projects

Group:          System Environment/Libraries
BuildArch: noarch
Prefix:		/usr/local
License:        ASL 2.0
URL:            http://www.xsede.org/
Source:		xdusage-%VER%-%REL%.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:    perl(Date::Manip)
Requires:    perl(DBD::Pg)
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
mkdir -p %{buildroot}/usr/local/xdusage-%VER%-%REL%
./install.pl -user xdusage -dir /usr/local/xdusage-%VER%-%REL% -buildroot %{buildroot}
#touch sudoers files so they'll exist
touch %{buildroot}/usr/local/xdusage-%VER%-%REL%/xdusage.sudoers

%files
%attr(-, xdusage, xdusage) /usr/local/xdusage-%VER%-%REL%/xdusage.pl
%attr(-, xdusage, xdusage) /usr/local/xdusage-%VER%-%REL%/xdusage
%attr(-, xdusage, xdusage) /usr/local/xdusage-%VER%-%REL%/Admin
%attr(-, xdusage, xdusage) /usr/local/xdusage-%VER%-%REL%/Testing
%attr(-, xdusage, xdusage) /usr/local/xdusage-%VER%-%REL%/xdusage.1
%attr(-, xdusage, xdusage) /usr/local/xdusage-%VER%-%REL%/xdusage.manpage
%attr(-, xdusage, xdusage) /usr/local/xdusage-%VER%-%REL%/INSTALL
%attr(-, xdusage, xdusage) /usr/local/xdusage-%VER%-%REL%/xdusage.modules
%attr(-, xdusage, xdusage) /usr/local/xdusage-%VER%-%REL%/xdusage.sudoers

%clean

%post
#echo sudoers to files
cat <<EOF > $RPM_INSTALL_PREFIX/xdusage-%VER%-%REL%/xdusage.sudoers
Defaults!$RPM_INSTALL_PREFIX/xdusage-%VER%-%REL%/bin/xdusage.pl env_keep="USER XDUSAGE_INSTALL_DIR"
ALL ALL=(xdusage) NOPASSWD: $RPM_INSTALL_PREFIX/xdusage-%VER%-%REL%/xdusage.pl
EOF

#clean up relocation problems
sed -i -e "s|/usr/local/xdusage-%VER%-%REL%|$RPM_INSTALL_PREFIX/xdusage-%VER%-%REL%|g" $RPM_INSTALL_PREFIX/xdusage-%VER%-%REL%/xdusage
sed -i -e "s|/usr/local/xdusage-%VER%-%REL%|$RPM_INSTALL_PREFIX/xdusage-%VER%-%REL%|g" $RPM_INSTALL_PREFIX/xdusage-%VER%-%REL%/xdusage.modules


%postun

%changelog
