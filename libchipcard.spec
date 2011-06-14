%define name libchipcard
%define version 5.0.2
%define fversion %{version}
%define release %mkrel 1
%define libnamedev %mklibname -d chipcard
%define clientmajor 6
%define clientlibname %mklibname chipcard %clientmajor

Summary: A library for easy access to smart cards (chipcards)
Name: %{name}
Version: %{version}
Release: %{release}
Source: http://files.hboeck.de/aq/%{name}-%{fversion}.tar.gz
Group: System/Libraries
License: LGPLv2
URL: http://www.aquamaniac.de/sites/libchipcard/index.php
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: libgwenhywfar-devel >= 4.0.0
BuildRequires: libpcsclite-devel
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

%package -n %libnamedev
Summary: LibChipCard server development kit
Group: Development/C
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

%build
%configure2_5x --disable-static --with-pcsc-libs=%{_libdir}
%make

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
%makeinstall_std

find %buildroot%_libdir -name *.la|xargs rm 

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

%files -n %clientlibname
%defattr(-,root,root)
%{_libdir}/libchipcard.so.%{clientmajor}*

%files -n %libnamedev
%defattr(-,root,root)
%doc README COPYING ChangeLog
%{_libdir}/*.so
%{_bindir}/chipcard-config
%{_includedir}/*
%{_datadir}/aclocal/chipcard.m4

%files
%defattr(-,root,root)
%doc README COPYING ChangeLog
%{_sysconfdir}/chipcard
%{_bindir}/*
%{_datadir}/chipcard
%{_libdir}/gwenhywfar/plugins/*/ct
