Summary:	Process accounting tools
Summary(es):	Herramientas de contabilidad de procesos
Summary(pl):	Program do logowania procesów u¿ytkowników
Summary(pt_BR):	Ferramentas de contabilização de processos
Summary(uk):	õÔÉÌ¦ÔÉ ÄÌÑ ÍÏÎ¦ÔÏÒÉÎÇÕ ÁËÔÉ×ÎÏÓÔ¦ ÐÒÏÃÅÓ¦×
Summary(ru):	õÔÉÌÉÔÙ ÄÌÑ ÍÏÎÉÔÏÒÉÎÇÁ ÁËÔÉ×ÎÏÓÔÉ ÐÒÏÃÅÓÓÏ×
Name:		psacct
Version:	6.3.5
Release:	9
License:	GPL
Group:		Applications/System
# there is only 6.3.2 on ftp://ftp.gnu.org/pub/gnu/acct/
# GNU page points to Debian resources, but they have modified ".orig" package
# and we have something else in CVS, which probably matches this:
Source0:	ftp://ftp.pl.openwall.com/pub/Owl/pool/sources/acct/acct-%{version}.tar.gz
# Source0-md5:	a982333648d68e0eabf87989a1e5427b
Source1:	acct.logrotate
Source2:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-non-english-man-pages.tar.bz2
# Source2-md5:	85eb213fc45fad1c7834d239ff8e28a4
Patch0:		acct-info.patch
Patch1:		acct-amfix.patch
Patch2:		%{name}-ac_am.patch
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

%description -l es
Están incluidas aquí las herramientas necesarias para contabilizar las
actividades de procesos.

%description -l pl
Narzêdzia niezbêdne do logowania wszystkich procesów i komend
u¿ytkowników oraz monitorowania systemu.

%description -l pt_BR
As ferramentas necessárias para contabilizar as atividades de
processos estão incluídas aqui.

%description -l uk
ãÅÊ ÐÁËÅÔ Í¦ÓÔÉÔØ ÕÔÉÌ¦ÔÉ ÄÌÑ ÚÂÏÒÕ ÔÁ ÏÂÒÏÂËÉ ÓÔÁÔÉÓÔÉËÉ ÁËÔÉ×ÎÏÓÔ¦ ÐÒÏÃÅÓ¦×.

%description -l ru
üÔÏÔ ÐÁËÅÔ ÓÏÄÅÒÖÉÔ ÕÔÉÌÉÔÙ ÄÌÑ ÓÂÏÒÁ É ÏÂÒÁÂÏÔËÉ ÓÔÁÔÉÓÔÉËÉ ÁËÔÉ×ÎÏÓÔÉ
ÐÒÏÃÅÓÓÏ×.

%prep
%setup -q -n acct-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%{__autoheader}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/logrotate.d,%{_prefix},/sbin,/var/log}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT{%{_sbindir}/accton,/sbin/accton}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/logrotate.d/acct
bzip2 -dc %{SOURCE2} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}

touch $RPM_BUILD_ROOT/var/log/{pacct,usracct,savacct}

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
/sbin/accton >/dev/null 2>&1
echo "Type \"/sbin/accton /var/log/pacct\" to run accounting."
touch /var/log/{pacct,usracct,savacct}
chmod 640 /var/log/{pacct,usracct,savacct}

%preun
if [ "$1" = "0" ]; then
	/sbin/accton >/dev/null 2>&1
fi

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc {ChangeLog,NEWS,README}*

%attr(640,root,root) /etc/logrotate.d/*
%attr(640,root,root) %ghost /var/log/pacct
%attr(640,root,root) %ghost /var/log/usracct
%attr(640,root,root) %ghost /var/log/savacct

%attr(755,root,root) %{_bindir}/ac
%attr(755,root,root) %{_bindir}/lastcomm
%attr(755,root,root) /sbin/accton
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
