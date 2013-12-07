%define major	6
%define libname %mklibname chipcard %{major}
%define devname %mklibname -d chipcard

Summary:	A library for easy access to smart cards (chipcards)
Name:		libchipcard
Version:	5.0.2
Release:	4
Group:		System/Libraries
License:	LGPLv2
Url:		http://www.aquamaniac.de/sites/libchipcard/index.php
Source0:	http://files.hboeck.de/aq/%{name}-%{version}.tar.gz
BuildRequires:	pkgconfig(gwenhywfar)
BuildRequires:	pkgconfig(libpcsclite)
Requires(post,preun):	rpm-helper

%description
Libchipcard allows easy access to smart cards. It provides basic access
to memory and processor cards and has special support for German medical
cards, German "Geldkarten" and HBCI (homebanking) cards (both type 0 and 
type 1).

It accesses the readers via CTAPI or PC/SC interfaces and has successfully
been tested with Towitoko, Kobil and Reiner-SCT readers.

This package contains the chipcard3-daemon needed to access card readers.

%package -n %{libname}
Group:		System/Libraries
Summary:	A library for easy access to smart cards (chipcards)
Suggests:	%{name} >= %{version}

%description -n %{libname}
This package contains the shared library for %{name}.

%package -n %{devname}
Summary:	LibChipCard server development kit
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description  -n %{devname}
This package contains chipcard3-server-config and header files for writing 
drivers, services or even your own chipcard daemon for LibChipCard.

%prep
%setup -q

%build
%configure2_5x \
	--disable-static \
	--with-pcsc-libs=%{_libdir}
%make

%install
%makeinstall_std

%post
%_post_service chipcardd

%preun
%_preun_service chipcardd

%files
%doc README COPYING ChangeLog
%{_sysconfdir}/chipcard
%{_bindir}/cardcommander
%{_bindir}/chipcard-tool
%{_bindir}/geldkarte
%{_bindir}/kvkcard
%{_bindir}/memcard
%{_datadir}/chipcard
%{_libdir}/gwenhywfar/plugins/*/ct

%files -n %{libname}
%{_libdir}/libchipcard.so.%{major}*

%files -n %{devname}
%doc README COPYING ChangeLog
%{_libdir}/*.so
%{_bindir}/chipcard-config
%{_includedir}/*
%{_datadir}/aclocal/chipcard.m4

