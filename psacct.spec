Summary:	Process accounting tools
Summary(es.UTF-8):	Herramientas de contabilidad de procesos
Summary(pl.UTF-8):	Program do logowania procesów użytkowników
Summary(pt_BR.UTF-8):	Ferramentas de contabilização de processos
Summary(uk.UTF-8):	Утиліти для моніторингу активності процесів
Summary(ru.UTF-8):	Утилиты для мониторинга активности процессов
Name:		psacct
Version:	6.5.5
Release:	1
License:	GPL v3+
Group:		Applications/System
Source0:	http://ftp.gnu.org/gnu/acct/acct-%{version}.tar.gz
# Source0-md5:	554a9e9c6aa3482df07e80853eac0350
Source1:	acct.logrotate
Source2:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-non-english-man-pages.tar.bz2
# Source2-md5:	85eb213fc45fad1c7834d239ff8e28a4
Source3:	acct.sysinit
Source4:	acct.sysconfig
Patch3:		%{name}-path.patch
URL:		http://www.gnu.org/directory/GNU/acct.html
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	texinfo
Requires:	logrotate
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The tools necessary for accounting the activities of processes are
included here.

%description -l es.UTF-8
Están incluidas aquí las herramientas necesarias para contabilizar las
actividades de procesos.

%description -l pl.UTF-8
Narzędzia niezbędne do logowania wszystkich procesów i komend
użytkowników oraz monitorowania systemu.

%description -l pt_BR.UTF-8
As ferramentas necessárias para contabilizar as atividades de
processos estão incluídas aqui.

%description -l uk.UTF-8
Цей пакет містить утиліти для збору та обробки статистики активності процесів.

%description -l ru.UTF-8
Этот пакет содержит утилиты для сбора и обработки статистики активности
процессов.

%prep
%setup -q -n acct-%{version}
%patch3 -p1

%build
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%{__autoheader}

%configure \
	--enable-linux-multiformat

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d,logrotate.d,sysconfig},/sbin,/var/log}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT{%{_sbindir}/accton,/sbin/accton}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/logrotate.d/acct
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/rc.acct
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/acct
bzip2 -dc %{SOURCE2} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}

touch $RPM_BUILD_ROOT/var/log/{pacct,usracct,savacct}

# in PLD it's packaged in SysVinit
%{__rm} $RPM_BUILD_ROOT{%{_bindir}/last,%{_mandir}/man1/last.1}

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
if [ "$1" = "1" ]; then
	/etc/rc.d/rc.acct stop 1>&2
	echo "Type \"/etc/rc.d/rc.acct start\" to run accounting."
	touch /var/log/{pacct,usracct,savacct}
	chmod 640 /var/log/{pacct,usracct,savacct}
else
	/etc/rc.d/rc.acct reload 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	/etc/rc.d/rc.acct stop 1>&2
fi

%postun	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(754,root,root) /etc/rc.d/rc.acct
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/acct
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/acct
%attr(640,root,root) %ghost /var/log/pacct
%attr(640,root,root) %ghost /var/log/usracct
%attr(640,root,root) %ghost /var/log/savacct

%attr(755,root,root) %{_bindir}/ac
%attr(755,root,root) %{_bindir}/lastcomm
%attr(755,root,root) /sbin/accton
%attr(755,root,root) %{_sbindir}/dump-acct
%attr(755,root,root) %{_sbindir}/dump-utmp
%attr(755,root,root) %{_sbindir}/sa

%{_mandir}/man1/ac.1*
%{_mandir}/man1/lastcomm.1*
%{_mandir}/man8/dump-utmp.8*
%{_mandir}/man8/sa.8*
%{_mandir}/man8/accton.8*
%lang(fi) %{_mandir}/fi/man1/ac.1*
%lang(fi) %{_mandir}/fi/man1/lastcomm.1*
%lang(fr) %{_mandir}/fr/man8/accton.8*
%lang(pl) %{_mandir}/pl/man1/ac.1*

%{_infodir}/accounting.info*
