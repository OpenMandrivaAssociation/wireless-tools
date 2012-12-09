%define name 	wireless-tools
%define version	29
%define pre	0
%define rel	6
%if %{pre}
%define release	%manbo_mkrel 0.pre%{pre}.%{rel}
%define src	wireless_tools.%{version}.pre%{pre}.tar.gz
%else
%define release	%manbo_mkrel %{rel}
%define src	wireless_tools.%{version}.tar.gz
%endif
%define lib_name_orig libiw
%define lib_major %{version}
%define lib_name %mklibname iw %{lib_major}
%define docs README INSTALL CHANGELOG.h DISTRIBUTIONS.txt COPYING PCMCIA.txt HOTPLUG.txt

Summary: Wireless ethernet configuration tools
Group: System/Kernel and hardware
License: GPL
Name: %{name}
Version: %{version}
Release: %{release}
URL: http://www.hpl.hp.com/personal/Jean_Tourrilhes/Linux/Tools.html
Source: http://www.hpl.hp.com/personal/Jean_Tourrilhes/Linux/%{src}
Patch2: wireless_tools.27-wireless-man-upd.patch.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Conflicts: man-pages-fr < 1.58.0-16mdk
# (blino) strict Requires, see 28-1.pre9.2mdk changelog
Requires: %{lib_name} = %{version}-%{release}

%description
This package contain the Wireless tools, used to manipulate
the Wireless Extensions. The Wireless Extension is an interface
allowing you to set Wireless LAN specific parameters and get the
specific stats for wireless networking equipment.

This is specifically useful since it allows manipulation of encryption
parameters possible with the GPL WaveLAN cards.

%package -n %{lib_name}
Summary: Wireless_tools library
Group: System/Libraries
Provides: %{lib_name_orig}

%description -n %{lib_name}
This package contains libraries to configure and access wireless interface
cards.

%package -n %{lib_name}-devel
Summary: Wireless_tools development library
Group: Development/C
Provides: %{lib_name_orig}-devel
# (blino) strict Requires, see 28-1.pre9.2mdk changelog
Requires: %{lib_name} = %{version}-%{release}

%description -n %{lib_name}-devel
This package contains libraries and headers for use in developing
wireless tools.

%prep
%setup -q -n wireless_tools.%{version}
%patch2 -p0
chmod a+r %{docs}

%build
%make clean
%make "CFLAGS=$RPM_OPT_FLAGS -I."

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall \
	PREFIX=%{buildroot}%{_prefix} \
	INSTALL_LIB=%{buildroot}/%{_lib} \
	INSTALL_MAN=%{buildroot}%{_mandir} \
	INSTALL_DIR=%{buildroot}/sbin

mkdir -p $RPM_BUILD_ROOT%_mandir/fr/man8
install -m 644 fr/* $RPM_BUILD_ROOT%_mandir/fr/man8/

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -n %{lib_name} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{lib_name} -p /sbin/ldconfig
%endif

%triggerpostun -- wireless-tools < 28-1.pre9.3mdk
[ -f /etc/iftab ] && sed -i -e s,mac_ieee1394,mac, /etc/iftab
:

%files
%defattr(-,root,root,0755)
%doc %{docs}
/sbin/*
%{_mandir}/man*/*
%lang(fr) %{_mandir}/fr/man*/*

%files -n %{lib_name}
%defattr(-,root,root,0755)
/%{_lib}/libiw.so.*

%files -n %{lib_name}-devel
%defattr(-,root,root,0755)
/%{_lib}/libiw.so
%{_includedir}/iwlib.h
%{_includedir}/wireless.h


%changelog
* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 29-4mnb2
+ Revision: 670810
- mass rebuild

* Tue Aug 05 2008 Thierry Vignaud <tv@mandriva.org> 29-3mnb2
+ Revision: 263680
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Mon Feb 18 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 29-2mnb1
+ Revision: 172124
- Revert last patch to wireless.h, it's breaking because of missing
  __user definition. The patch could be reworked to workaround this,
  but just rollback now, until I get an answer from linux-wireless ML
  about what should be done about wireless.h exported by kernel.

* Mon Feb 18 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 29-1mnb1
+ Revision: 171731
- Updated to version 29
- Patch wireless.h so that we include proper user space headers, after
  kernel headers were protected with "#ifdef __KERNEL__"
  (wireless_tools.29-fix-wireless.h-includes.patch).

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 29-0.pre22.1mnb1
+ Revision: 170658
- replace %%mkrel with %%manbo_mkrel for Manbo Core 1
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Tue Aug 28 2007 Olivier Blin <oblin@mandriva.com> 29-0.pre22.1mdv2008.0
+ Revision: 72735
- 29.pre22

* Fri Jun 22 2007 Per Ã˜yvind Karlsen <peroyvind@mandriva.org> 28-3mdv2008.0
+ Revision: 43294
- rebuild
- Import wireless-tools



* Wed Jul 26 2006 Olivier Blin <blino@mandriva.com> 28-2mdv2007.0
- 28 final

* Wed Mar 15 2006 Olivier Blin <oblin@mandriva.com> 28-1.pre15.1mdk
- 28-pre15

* Sat Oct 22 2005 Olivier Blin <oblin@mandriva.com> 28-1.pre10.1mdk
- 28-pre10

* Mon Oct 10 2005 Olivier Blin <oblin@mandriva.com> 28-1.pre9.3mdk
- don't fail in trigger postun

* Fri Oct  7 2005 Olivier Blin <oblin@mandriva.com> 28-1.pre9.2mdk
- add triger postun to automatically rename mac_ieee1394 modifier as mac
  (and stop whining about announced migration)
- require strict version of libiw (the API may change during beta cycle,
  and we use to package many pre release versions)

* Tue Oct  4 2005 Olivier Blin <oblin@mandriva.com> 28-0.pre9.1mdk
- 28-pre9
- drop Patch3 (mac_ieee1394 modifier), generic support is now present
- drop obsolete BUILD_SHARED makefile option
- remove .so linking, already done in Makefile
- install libiw in /_lib (not _libdir) as intented in the Makefile
  (so that iwconfig works when /usr isn't mounted)

* Thu Jul 28 2005 Olivier Blin <oblin@mandriva.com> 28-0.pre6.1mdk
- 28-pre6
- rediff Patch3
- fix specfile to allow to build pre-releases without removing the
  pre-tag in the tarball name
- remove requires on release

* Tue Jan 04 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 27-1mdk
- new release (the previous updates was bogus and we packaged pre19 instead of
  pre23)
- rediff patch3

* Thu Aug 19 2004 Olivier Blin <blino@mandrake.org> 27-0.pre23.2mdk
- allow mac_ieee1394 modifier in iftab/ifrename (crappy Patch3)

* Fri Jun 18 2004 Laurent Culioli <laurent@mandrake.org> 27-0.pre23.1mdk
- new version

* Mon Apr 05 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 27-0.pre19.2mdk
- patch 2: update wireless.7 man page
- install french translations of man pages

* Fri Apr 02 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 27-0.pre19.1mdk
- new release
- drop patch 1 (obsolete)
- fix build

* Fri Nov 21 2003 Stew Benedict <sbenedict@mandrakesoft.com> 26-3mdk
- rework patch1 (force v16)

* Thu Sep 18 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 26-2mdk
- lib64 fixes

* Thu Aug 21 2003 Laurent Culioli <laurent@pschit.net> 26-1mdk
- 26
- Update Patch1

* Fri Jul 25 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 25-5mdk
- rebuild

* Tue Feb 11 2003 Frederic Lepied <flepied@mandrakesoft.com> 25-4mdk
- use %%mklibname

* Mon Jan 20 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 25-3mdk
- Force to be compiled by v15.

* Mon Dec 16 2002 Stew Benedict <sbenedict@mandrakesoft.com> 25-2mdk
- move iwlib.h and iwlib.a to -devel, create libiw.so, quiet setup
- work by Ben Reser <ben@reser.org>:
- Fix permissions on %%doc dir files
- Fix missing %%posts for lib package
- Fix Summary caps to shut up rpmlint.
- Fix missing %%defattr on lib package.
- Switched to using %%makeinstall rather than installing by "hand."
- Added missing files libiw.so, libiw.so.25, iwlib.h, and iwevent
- Adding missing documentation (man pages and %%doc dir things)
- Split library.
- Dynamically link the tools to the library rather than static.

* Mon Nov  4 2002 Frederic Lepied <flepied@mandrakesoft.com> 25-1mdk
- 25

* Fri Jun 14 2002 Frederic Lepied <flepied@mandrakesoft.com> 24-1mdk
- 24
- added missing binaries (Ben Reser)

* Tue Apr  9 2002 Frederic Lepied <flepied@mandrakesoft.com> 23-1mdk
- 23

* Fri Nov 30 2001 Frederic Lepied <flepied@mandrakesoft.com> 22-1mdk
- 22

* Sat Sep 29 2001 Frederic Lepied <flepied@mandrakesoft.com> 21-2mdk
- correct doc file permissions

* Fri Jun  1 2001 Frederic Lepied <flepied@mandrakesoft.com> 21-1mdk
- 21

* Mon Mar 12 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 20-4mdk
- Fix build with glibc 2.2.2's more strict headers (add patch 0)

* Sun Feb 11 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 20-3mdk
- Use RPM_OPT_FLAGS

* Fri Jan 12 2001 Frederic Lepied <flepied@mandrakesoft.com> 20-2mdk
- moved from contrib

* Mon Dec 04 2000 Lenny Cartier <lenny@mandrakesoft.com> 20-1mdk
- new in contribs
- used srpm from Kyle VanderBeek <kylev@yaga.com> 20-1mdk
	- First spec file for Mandrake distribution.
