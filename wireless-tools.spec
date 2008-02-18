%define name 	wireless-tools
%define version	29
%define pre	0
%define rel	1
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
Patch0: wireless_tools.29-fix-wireless.h-includes.patch
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
%patch0 -p1
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

%post -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig

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
