Summary:     Process accounting tools
Summary(pl): Program do logowania procesów u¿ytkowników
Name:        acct
Version:     6.3.2
Release:     5
Copyright:   GPL
Group:       Utilities/System
Group(pl):   Narzêdzia/System
Source:      ftp://prep.ai.mit.edu/pub/gnu/%{name}-%{version}.tar.gz
Patch0:      acct.patch
Patch1:      acct-info.patch
Prereq:      /sbin/install-info
BuildRoot:   /tmp/%{name}-%{version}-root
Obsoletes:   psacct

%description
The tools necessary for accounting the activities of processes are
included here.

%description -l pl
Narzêdzia niezbêdne do logowania wszystkich procesów i komend u¿ytkowników
oraz monitorowania systemu. 

%prep
%setup -q 
%patch0 -p1
%patch1 -p1

%build
autoconf
./configure %{_target} \
	--prefix=/usr
make CFLAGS="$RPM_OPT_FLAGS -Wall -Wmissing-prototypes" LDFLAGS="-s"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{usr,var/log}

make prefix=$RPM_BUILD_ROOT/usr install
touch $RPM_BUILD_ROOT/var/log/{pacct,usracct,savacct}
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/last.1
rm -f $RPM_BUILD_ROOT%{_bindir}/last

gzip -9f $RPM_BUILD_ROOT/usr/{info/*,man/man[18]/*}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/accounting.info.gz /etc/info-dir

%preun
if [ $1 = 0 ]; then
	/sbin/install-info --delete %{_infodir}/accounting.info.gz /etc/info-dir
fi

%files
%defattr(644, root, root, 755)
%attr(600, root, root) %config %verify(not size md5 mtime) /var/log/*
%attr(700, root, root) %{_sbindir}/*
%attr(700, root, root) %{_bindir}/*
%{_mandir}/man[18]/*
%{_infodir}/accounting.info.gz

%changelog
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
- major changes.

* Thu Oct 23 1997 Donnie Barnes <djb@redhat.com>
- updated from 6.2 to 6.3

* Mon Jul 21 1997 Erik Troan <ewt@redhat.com>
- built against glibc
