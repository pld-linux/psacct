Summary:	Process accounting tools
Summary(es):	Herramientas de contabilidad de procesos
Summary(pl):	Program do logowania procesów u¿ytkowników
Summary(pt_BR):	Ferramentas de contabilização de processos
Name:		psacct
Version:	6.3.5
Release:	8
License:	GPL
Group:		Applications/System
Source0:	ftp://prep.ai.mit.edu/pub/gnu/acct-%{version}.tar.gz
Source1:	acct.logrotate
Source2:	%{name}-non-english-man-pages.tar.bz2
Patch0:		acct-info.patch
Patch1:		acct-amfix.patch
Requires:	logrotate
BuildRequires:	autoconf
BuildRequires:	automake
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The tools necessary for accounting the activities of processes are
included here.

%description -l es
Están incluidas aquí las herramientas necesarias para contabilizar las
actividades de procesos.

%description -l pl
Narzêdzia niezbêdne do logowania wszystkich procesów i komend
u¿ytkowników oraz monitorowania systemu.

%description -l pt_BR
As ferramentas necessárias para contabilizar as atividades de
processos estão incluídas aqui.

%prep
%setup -q -n acct-%{version}
%patch0 -p1
%patch1 -p1

%build
aclocal
autoconf
automake -a -c -f
autoheader
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/logrotate.d,%{_prefix},/var/account}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

touch $RPM_BUILD_ROOT/var/account/{pacct,usracct,savacct}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/logrotate.d/acct
bzip2 -dc %{SOURCE2} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}

gzip -9nf ChangeLog NEWS

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
/usr/sbin/accton >/dev/null 2>&1
echo "Type \"/usr/sbin/actton /var/account/pacct\" to run accounting."
touch /var/account/{pacct,usracct,savacct}
chmod 640 /var/account/{pacct,usracct,savacct}

%preun
if [ "$1" = "0" ]; then
	/usr/sbin/accton >/dev/null 2>&1
fi

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc {ChangeLog,NEWS}.gz

%attr(640,root,root) /etc/logrotate.d/*
%attr(750,root,root) %dir /var/account
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
%lang(fi) %{_mandir}/fi/man1/ac.1*
%lang(fi) %{_mandir}/fi/man1/lastcomm.1*
%lang(fr) %{_mandir}/fr/man8/accton.8*
%lang(pl) %{_mandir}/pl/man1/ac.1*

%{_infodir}/accounting.info*
