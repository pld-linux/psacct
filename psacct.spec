Summary:     Process accounting tools
Summary(pl): Program do logowania procesów u¿ytkowników
Name:        acct
Version:     6.3.2
Release:     4
Copyright:   GPL
Group:       Utilities/System
Source:      ftp://prep.ai.mit.edu/pub/gnu/%{name}-%{version}.tar.gz
Patch:       %{name}.patch
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
%patch -p0

%build
autoconf
LDFLAGS="-s" ./configure --prefix=/usr
make CFLAGS="$RPM_OPT_FLAGS -Wall -Wmissing-prototypes"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{usr,var/log}

make prefix=$RPM_BUILD_ROOT/usr install
touch $RPM_BUILD_ROOT/var/log/{pacct,usracct,savacct}
rm -f $RPM_BUILD_ROOT/usr/man/man1/last.1
rm -f $RPM_BUILD_ROOT/usr/bin/last

gzip -9f $RPM_BUILD_ROOT/usr/{info/*,man/man[18]/*}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info /usr/info/accounting.info.gz /etc/info-dir \
--entry \
"* accounting: (acct).                           The GNU Process Accounting Suite."

%preun
if [ $1 = 1 ]; then
        /sbin/install-info --delete /usr/info/accounting.info.gz /etc/info-dir
fi

%files
%defattr(644, root, root, 755)
%attr(600, root, root) %config %verify(not size md5 mtime) /var/log/*
%attr(700, root, root) /usr/sbin/*
%attr(700, root, root) /usr/bin/*
%attr(644, root, man) /usr/man/man[18]/*
/usr/info/accounting.info.gz

%changelog
* Sun Nov 29 1998 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [6.3.2-4]
- added gzipping man pages,
- standarized {un}registering info pages.

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
