Summary:	Process accounting tools
Summary(pl):	Program do logowania procesów u¿ytkowników
Name:		acct
Version:	6.3.5
Release:	1
Copyright:	GPL
Group:		Utilities/System
Group(pl):	Narzêdzia/System
Source0:	ftp://prep.ai.mit.edu/pub/gnu/%{name}-%{version}.tar.gz
Source1:	acct.logrotate
Patch0:		acct-info.patch
Prereq:		/sbin/install-info
Requires:	logrotate
BuildRoot:	/tmp/%{name}-%{version}-root

%description
The tools necessary for accounting the activities of processes are
included here.

%description -l pl
Narzêdzia niezbêdne do logowania wszystkich procesów i komend u¿ytkowników
oraz monitorowania systemu. 

%prep
%setup -q 
%patch -p1

%build
%GNUconfigure

make LDFLAGS="-s"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{etc/logrotate.d,usr,var/account}

make \
    prefix=$RPM_BUILD_ROOT%{_prefix} \
    install

touch $RPM_BUILD_ROOT/var/account/{pacct,usracct,savacct}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/logrotate.d/acct

gzip -9f $RPM_BUILD_ROOT{%{_infodir}/*,%{_mandir}/man[18]/*} ChangeLog NEWS

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/accounting.info.gz /etc/info-dir
    /usr/sbin/accton &>/dev/null    
    echo "Type \"/usr/sbin/actton /var/account/pacct\" to run accounting." 

%preun
if [ "$1" = "0" ]; then
    /sbin/install-info --delete %{_infodir}/accounting.info.gz /etc/info-dir
    /usr/sbin/accton &>/dev/null
fi

%files
%defattr(644,root,root,755)
%doc {ChangeLog,NEWS}.gz

%attr(640,root,root) /etc/logrotate.d/*

%attr(755,root,root) %{_bindir}/ac
%attr(755,root,root) %{_bindir}/lastcomm
%attr(755,root,root) %{_sbindir}/accton
%attr(755,root,root) %{_sbindir}/sa

%{_mandir}/man1/ac.1.gz
%{_mandir}/man1/lastcomm.1.gz
%{_mandir}/man8/sa.8.gz
%{_mandir}/man8/accton.8.gz

%{_infodir}/accounting.info.gz

%attr(600,root,root) %config %verify(not size md5 mtime) /var/account/*

%changelog
* Thu May 27 1999 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [6.3.5-1]
- up version (from debian devel ;) 

* Mon May 24 1999 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [6.3.2-7]
- FHS 2.0,
- rotate logs,
- added %doc,
- more macros.

* Wed Jan 06 1999 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [6.3.2-5]
- added gzipping man pages,
- standarized {un}registering info pages (added acct-info.patch).

* Sun Nov 22 1998 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [6.3.2-3]
- fixed --entry text on {un}registering info page for ed in %post
  %preun.

* Fri Oct 09 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [6.3.2-2]
- fixed pl translation,
- Obsoletes psacct,
- minor changes.

* Tue Aug 11 1998 Wojtek ¦lusarczyk <wojtek@SHADOW.EU.ORG>
  [6.3.2-1]
- translation modified for pl,
- moved %changelog at the end of spec,
- added %defattr support,
- changed permissions of binaries to 700,
- added %verify support for pacct, usracct, savacct,
- added rpm_opt_flags support,
- build from non root's account,
- major changes,
- start at RH spec file.
