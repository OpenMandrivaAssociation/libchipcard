%define name libchipcard3
%define version 3.0.4
%define fversion %{version}
%define release %mkrel 1
%define api 3
%define major 0
%define libname %mklibname chipcard %api %major
%define libnamedev %mklibname -d chipcard %api
%define clientmajor 1
%define clientlibname %mklibname chipcard3c %clientmajor

Summary: A library for easy access to smart cards (chipcards)
Name: %{name}
Version: %{version}
Release: %{release}
Source: http://prdownloads.sourceforge.net/libchipcard/%{name}-%{fversion}.tar.gz
# (fc)  3.0.2-3mdv fix initscript
Patch0: libchipcard3-3.0.2-fixinitscript.patch

Group: System/Libraries
License: GPL
URL: http://www.libchipcard.de
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: libgwenhywfar-devel >= 2.3
BuildRequires: libpcsclite-devel
BuildRequires: libusb-devel
BuildRequires: libsysfs-devel
BuildRequires: kernel-source
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

%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig
%post -n %clientlibname -p /sbin/ldconfig
%postun -n %clientlibname -p /sbin/ldconfig

%post
%_post_service chipcardd3
%preun
%_preun_service chipcardd3

%files -n %libname
%defattr(-,root,root,0755)
%{_libdir}/libchipcard3_ctapi.so.%{major}*
%{_libdir}/libchipcard3d.so.%{major}*

%files -n %clientlibname
%defattr(-,root,root,0755)
%{_libdir}/libchipcard3c.so.%{clientmajor}*

%files -n %libnamedev
%defattr(-,root,root,0755)
%doc README COPYING ChangeLog
%{_libdir}/*.so
%{_bindir}/chipcard3-config
%{_includedir}/*
%attr(644,root,root) %{_libdir}/*.*a
%{_datadir}/aclocal/chipcard3.m4

%files
%defattr(-,root,root,0755)
%doc README COPYING ChangeLog
#%{_libdir}/chipcard3-server
%{_libdir}/gwenhywfar/plugins
%dir %{_sysconfdir}/chipcard3/
%dir %{_sysconfdir}/chipcard3/client/
%dir %{_sysconfdir}/chipcard3/server/
%config(noreplace) %{_sysconfdir}/chipcard3/client/chipcardc3.conf*
%config(noreplace) %{_sysconfdir}/chipcard3/server/chipcardd3.conf*
%config(noreplace) %{_sysconfdir}/chipcard3/server/chipcardd3
%attr(755,root,root) %{_sysconfdir}/init.d/chipcardd3
%{_bindir}/cardcommander3
%{_bindir}/chipcard3-tool
%{_bindir}/geldkarte3
%{_bindir}/kvkcard3
%{_bindir}/memcard3
%{_sbindir}/chipcardd3
%_datadir/chipcard3/
%_libdir/chipcard3/


