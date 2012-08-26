%define clientmajor 6
%define clientlibname %mklibname chipcard %{clientmajor}
%define libnamedev %mklibname -d chipcard

Summary:	A library for easy access to smart cards (chipcards)
Name:		libchipcard
Version:	5.0.2
Release:	3
Group:		System/Libraries
License:	LGPLv2
URL:		http://www.aquamaniac.de/sites/libchipcard/index.php
Source:		http://files.hboeck.de/aq/%{name}-%{version}.tar.gz
BuildRequires:	pkgconfig(gwenhywfar)
BuildRequires:	pkgconfig(libpcsclite)
Requires(post):	rpm-helper
Requires(preun): rpm-helper

%description
Libchipcard allows easy access to smart cards. It provides basic access
to memory and processor cards and has special support for German medical
cards, German "Geldkarten" and HBCI (homebanking) cards (both type 0 and 
type 1).

It accesses the readers via CTAPI or PC/SC interfaces and has successfully
been tested with Towitoko, Kobil and Reiner-SCT readers.

This package contains the chipcard3-daemon needed to access card readers.

%package -n %{libnamedev}
Summary:	LibChipCard server development kit
Group:		Development/C
Requires:	%{clientlibname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description  -n %{libnamedev}
This package contains chipcard3-server-config and header files for writing 
drivers, services or even your own chipcard daemon for LibChipCard.

%package -n %{clientlibname}
Group:		System/Libraries
Summary:	A library for easy access to smart cards (chipcards)
Requires:	%{name} >= %{version}

%description -n %{clientlibname}
Libchipcard allows easy access to smart cards. It provides basic access
to memory and processor cards and has special support for German medical
cards, German "Geldkarten" and HBCI (homebanking) cards (both type 0 and 
type 1).

It accesses the readers via CTAPI or PC/SC interfaces and has successfully
been tested with Towitoko, Kobil and Reiner-SCT readers.

This package contains the chipcard3-daemon needed to access card readers.


%prep
%setup -q

%build
%configure2_5x --disable-static --with-pcsc-libs=%{_libdir}
%make

%install
%makeinstall_std

%post
%_post_service chipcardd

%preun
%_preun_service chipcardd

%files -n %{clientlibname}
%{_libdir}/libchipcard.so.%{clientmajor}*

%files -n %{libnamedev}
%doc README COPYING ChangeLog
%{_libdir}/*.so
%{_bindir}/chipcard-config
%{_includedir}/*
%{_datadir}/aclocal/chipcard.m4

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

%changelog
* Tue Sep 27 2011 Andrey Bondrov <abondrov@mandriva.org> 5.0.2-2mdv2012.0
+ Revision: 701427
- Clean up spec, rebuild

* Tue Jun 14 2011 Götz Waschk <waschk@mandriva.org> 5.0.2-1
+ Revision: 685005
- new version
- drop patch

* Fri Apr 29 2011 Oden Eriksson <oeriksson@mandriva.com> 5.0.0-3
+ Revision: 660229
- mass rebuild

* Tue Sep 21 2010 Funda Wang <fwang@mandriva.org> 5.0.0-2mdv2011.0
+ Revision: 580319
- rebuild

* Mon Aug 30 2010 Funda Wang <fwang@mandriva.org> 5.0.0-1mdv2011.0
+ Revision: 574507
- new version 5.0.0
- New version 5.0.0

* Mon Aug 30 2010 Funda Wang <fwang@mandriva.org> 4.99.9-1mdv2011.0
+ Revision: 574304
- new version 4.99.9

* Thu Jul 29 2010 Funda Wang <fwang@mandriva.org> 4.99.6-1mdv2011.0
+ Revision: 563000
- New version 4.99.6 towards 5.0

* Mon Dec 28 2009 Frederik Himpe <fhimpe@mandriva.org> 4.2.9-1mdv2010.1
+ Revision: 483091
- Update to new version 4.2.9

* Sat May 30 2009 Funda Wang <fwang@mandriva.org> 4.2.8-1mdv2010.0
+ Revision: 381411
- new version 4.2.8

* Tue Apr 28 2009 Götz Waschk <waschk@mandriva.org> 4.2.7-1mdv2010.0
+ Revision: 369097
- new version
- update file list

* Thu Jan 22 2009 Funda Wang <fwang@mandriva.org> 4.2.4-1mdv2009.1
+ Revision: 332592
- New version 4.2.4

* Thu Dec 04 2008 Götz Waschk <waschk@mandriva.org> 4.2.3-2mdv2009.1
+ Revision: 309998
- rebuild to get rid of libtasn1 dep
- fix source URL

* Mon Nov 10 2008 Götz Waschk <waschk@mandriva.org> 4.2.3-1mdv2009.1
+ Revision: 301680
- new version

* Mon Oct 20 2008 Götz Waschk <waschk@mandriva.org> 4.2.2-1mdv2009.1
+ Revision: 295581
- fix build deps
- new version

* Sat Oct 18 2008 Götz Waschk <waschk@mandriva.org> 4.2.1-1mdv2009.1
+ Revision: 294848
- new version
- fix source URL

  + Funda Wang <fwang@mandriva.org>
    - fix url

* Tue Aug 19 2008 Funda Wang <fwang@mandriva.org> 4.2.0-1mdv2009.0
+ Revision: 273941
- New version 4.2.0

* Wed Jul 09 2008 Götz Waschk <waschk@mandriva.org> 4.1.3-1mdv2009.0
+ Revision: 233015
- new version

* Sun Jul 06 2008 Götz Waschk <waschk@mandriva.org> 4.1.2-1mdv2009.0
+ Revision: 232285
- new version
- fix license

* Sat Jun 14 2008 Funda Wang <fwang@mandriva.org> 4.1.1-1mdv2009.0
+ Revision: 219135
- bring back the init file
- New version 4.1.1

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Thierry Vignaud <tv@mandriva.org>
    - improved description

* Wed May 28 2008 Funda Wang <fwang@mandriva.org> 4.1.0-1mdv2009.0
+ Revision: 212176
- New version 4.1.0

* Wed Apr 16 2008 Götz Waschk <waschk@mandriva.org> 4.0.0-1mdv2009.0
+ Revision: 194594
- new version
- update the patch
- update file list
- rename the package

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Nov 23 2007 Götz Waschk <waschk@mandriva.org> 3.0.4-1mdv2008.1
+ Revision: 111452
- new version

* Mon Aug 27 2007 Götz Waschk <waschk@mandriva.org> 3.0.3-1mdv2008.0
+ Revision: 71765
- new version
- new devel name

