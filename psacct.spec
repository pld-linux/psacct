Summary:	Process accounting tools
Summary(pl):	Program do logowania procesów u¿ytkowników
Name:		psacct
Version:	6.3.5
Release:	3
License:	GPL
Group:		Utilities/System
Group(pl):	Narzêdzia/System
Source0:	ftp://prep.ai.mit.edu/pub/gnu/acct-%{version}.tar.gz
Source1:	acct.logrotate
Patch0:		acct-info.patch
Prereq:		/usr/sbin/fix-info-dir
Requires:	logrotate
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The tools necessary for accounting the activities of processes are included
here.

%description -l pl
Narzêdzia niezbêdne do logowania wszystkich procesów i komend u¿ytkowników
oraz monitorowania systemu.

%prep
%setup -q -n acct-%{version}
%patch0 -p1

%build
aclocal
autoconf
automake
autoheader
LDFLAGS="-s"; export LDFLAGS
%configure

make

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{etc/logrotate.d,usr,var/account}

make install \
	DESTDIR=$RPM_BUILD_ROOT

touch $RPM_BUILD_ROOT/var/account/{pacct,usracct,savacct}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/logrotate.d/acct

gzip -9nf $RPM_BUILD_ROOT{%{_infodir}/*,%{_mandir}/man[18]/*} ChangeLog NEWS

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
/usr/sbin/accton &>/dev/null
echo "Type \"/usr/sbin/actton /var/account/pacct\" to run accounting."
touch /var/account/{pacct,usracct,savacct}
chmod 640 /var/account/{pacct,usracct,savacct}

%preun
if [ "$1" = "0" ]; then
	/usr/sbin/accton &>/dev/null
fi

%postun
/usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc {ChangeLog,NEWS}.gz

%attr(640,root,root) /etc/logrotate.d/*
%attr(640,root,root) %ghost /var/account/pacct
%attr(640,root,root) %ghost /var/account/usracct
%attr(640,root,root) %ghost /var/account/savacct

%attr(755,root,root) %{_bindir}/ac
%attr(755,root,root) %{_bindir}/lastcomm
%attr(755,root,root) %{_sbindir}/accton
%attr(755,root,root) %{_sbindir}/sa

%{_mandir}/man1/ac.1*
%{_mandir}/man1/lastcomm.1*
%{_mandir}/man8/sa.8*
%{_mandir}/man8/accton.8*

%{_infodir}/accounting.info*
