Summary:	Process accounting tools
Summary(pl):	Program do logowania procesów użytkowników
Name:		acct
Version:	6.3.5
Release:	2
Copyright:	GPL
Group:		Utilities/System
Group(pl):	Narzędzia/System
Source0:	ftp://prep.ai.mit.edu/pub/gnu/%{name}-%{version}.tar.gz
Source1:	acct.logrotate
Patch0:		acct-info.patch
Prereq:		/usr/sbin/fix-info-dir
Requires:	logrotate
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The tools necessary for accounting the activities of processes are
included here.

%description -l pl
Narzędzia niezbędne do logowania wszystkich procesów i komend użytkowników
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
/usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
    /usr/sbin/accton &>/dev/null    
    echo "Type \"/usr/sbin/actton /var/account/pacct\" to run accounting." 

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
