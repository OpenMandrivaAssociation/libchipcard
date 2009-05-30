%define name libchipcard
%define version 4.2.8
%define fversion %{version}
%define release %mkrel 1
%define major 0
%define libname %mklibname chipcard %major
%define libnamedev %mklibname -d chipcard
%define clientmajor 2
%define clientlibname %mklibname chipcardc %clientmajor

Summary: A library for easy access to smart cards (chipcards)
Name: %{name}
Version: %{version}
Release: %{release}
Source: http://files.hboeck.de/aq/%{name}-%{fversion}.tar.gz
# (fc)  3.0.2-3mdv fix initscript
Patch0: libchipcard-4.0.0-fixinitscript.patch

Group: System/Libraries
License: LGPLv2
URL: http://www.aquamaniac.de/sites/libchipcard/index.php
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: libgwenhywfar-devel >= 3.0.0
BuildRequires: libpcsclite-devel
BuildRequires: hal-devel
BuildRequires: libsysfs-devel
Requires(post): rpm-helper
Requires(preun): rpm-helper
Conflicts: libchipcard2

%description
Libchipcard allows easy access to smart cards. It provides basic access
to memory and processor cards and has special support for German medical
cards, German "Geldkarten" and HBCI (homebanking) cards (both type 0 and 
type 1).

It accesses the readers via CTAPI or PC/SC interfaces and has successfully
been tested with Towitoko, Kobil and Reiner-SCT readers.

This package contains the chipcard3-daemon needed to access card readers.

%package -n %libname
Group: System/Libraries
Summary: A library for easy access to smart cards (chipcards)
Requires: %name >= %version

%description -n %libname
Libchipcard allows easy access to smart cards. It provides basic access
to memory and processor cards and has special support for German medical
cards, German "Geldkarten" and HBCI (homebanking) cards (both type 0 and 
type 1).

It accesses the readers via CTAPI or PC/SC interfaces and has successfully
been tested with Towitoko, Kobil and Reiner-SCT readers.

This package contains the chipcard3-daemon needed to access card readers.


%package -n %libnamedev
Summary: LibChipCard server development kit
Group: Development/C
Requires: %libname = %version
Requires: %clientlibname = %version
Provides: %name-devel = %version-%release
Obsoletes: %mklibname -d chipcard 3 0
Obsoletes: %mklibname -d chipcard 3

%description  -n %libnamedev
This package contains chipcard3-server-config and header files for writing 
drivers, services or even your own chipcard daemon for LibChipCard.

%package -n %clientlibname
Group: System/Libraries
Summary: A library for easy access to smart cards (chipcards)
Requires: %name >= %version

%description -n %clientlibname
Libchipcard allows easy access to smart cards. It provides basic access
to memory and processor cards and has special support for German medical
cards, German "Geldkarten" and HBCI (homebanking) cards (both type 0 and 
type 1).

It accesses the readers via CTAPI or PC/SC interfaces and has successfully
been tested with Towitoko, Kobil and Reiner-SCT readers.

This package contains the chipcard3-daemon needed to access card readers.


%prep
%setup -q -n %name-%fversion
%patch0 -p1 -b .fixinitscript

%build
%configure2_5x
%make

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir} %makeinstall_std
perl -pi -e "s^-L$RPM_BUILD_DIR/%name-%fversion/src/lib/chipcard3-client^^" %buildroot%_libdir/*.la %buildroot%_libdir/gwenhywfar/plugins/*/*/*.la
chmod 644 %buildroot%_libdir/*.la %buildroot%_libdir/gwenhywfar/plugins/*/*/*.la

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%post -n %clientlibname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %clientlibname -p /sbin/ldconfig
%endif

%post
%_post_service chipcardd
%preun
%_preun_service chipcardd

%files -n %libname
%defattr(-,root,root,0755)
%{_libdir}/libchipcard_ctapi.so.%{major}*

%files -n %clientlibname
%defattr(-,root,root,0755)
%{_libdir}/libchipcardc.so.%{clientmajor}*

%files -n %libnamedev
%defattr(-,root,root,0755)
%doc README COPYING ChangeLog
%{_libdir}/*.so
%{_bindir}/chipcard-config
%{_includedir}/*
%attr(644,root,root) %{_libdir}/*.*a
%{_datadir}/aclocal/chipcard.m4

%files
%defattr(-,root,root,0755)
%doc README COPYING ChangeLog
%{_libdir}/gwenhywfar/plugins
%dir %{_sysconfdir}/chipcard/
%dir %{_sysconfdir}/chipcard/client/
%dir %{_sysconfdir}/chipcard/server/
%config(noreplace) %{_sysconfdir}/chipcard/client/chipcardc.conf*
%config(noreplace) %{_sysconfdir}/chipcard/server/chipcardd.conf*
%attr(755,root,root) %{_sysconfdir}/init.d/chipcardd
%{_bindir}/cardcommander
%{_bindir}/chipcard-tool
%{_bindir}/geldkarte
%{_bindir}/kvkcard
%{_bindir}/memcard
%{_sbindir}/chipcardd4
%_datadir/chipcard/
%_libdir/chipcard
