%define pre	9
%define rel	2
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
%define docs README INSTALL CHANGELOG.h DISTRIBUTIONS.txt COPYING PCMCIA.txt HOTPLUG-UDEV.txt

Summary:	Wireless ethernet configuration tools
Name:		wireless-tools
Version:	30
Release:	%{release}
Group:		System/Kernel and hardware
License:	GPL
URL:		http://www.hpl.hp.com/personal/Jean_Tourrilhes/Linux/Tools.html
Source0:	http://www.hpl.hp.com/personal/Jean_Tourrilhes/Linux/%{src}
Patch2:		wireless_tools.27-wireless-man-upd.patch.bz2
Conflicts:	man-pages-fr < 1.58.0-16mdk
# (blino) strict Requires, see 28-1.pre9.2mdk changelog
Requires:	%{lib_name} = %{version}-%{release}
Requires:	crda

%description
This package contain the Wireless tools, used to manipulate
the Wireless Extensions. The Wireless Extension is an interface
allowing you to set Wireless LAN specific parameters and get the
specific stats for wireless networking equipment.

This is specifically useful since it allows manipulation of encryption
parameters possible with the GPL WaveLAN cards.

%package -n %{lib_name}
Summary:	Wireless_tools library
Group:		System/Libraries
Provides:	%{lib_name_orig}

%description -n %{lib_name}
This package contains libraries to configure and access wireless interface
cards.

%package -n %{lib_name}-devel
Summary:	Wireless_tools development library
Group:		Development/C
Provides:	%{lib_name_orig}-devel
# (blino) strict Requires, see 28-1.pre9.2mdk changelog
Requires:	%{lib_name} = %{version}-%{release}

%description -n %{lib_name}-devel
This package contains libraries and headers for use in developing
wireless tools.

%prep
%setup -q -n wireless_tools.%{version}
%patch2 -p0
chmod a+r %{docs}

%build
%setup_compile_flags

# (tpg) enable build shared library
sed -i -e 's/BUILD_STATIC =.*/# BUILD_STATIC =.*/g' Makefile
# (tpg) pass our flags
sed -i -e 's#CFLAGS=#CFLAGS+=#' Makefile

%make clean
%make

%install
%makeinstall \
	PREFIX=%{buildroot}%{_prefix} \
	INSTALL_LIB=%{buildroot}/%{_lib} \
	INSTALL_MAN=%{buildroot}%{_mandir} \
	INSTALL_DIR=%{buildroot}/sbin

mkdir -p %{buildroot}%{_libdir}
ln -sf ../../%{_lib}/libiw.so.%{version} %{buildroot}%{_libdir}/libiw.so


%triggerpostun -- wireless-tools < 28-1.pre9.3mdk
[ -f /etc/iftab ] && sed -i -e s,mac_ieee1394,mac, /etc/iftab
:

%files
%doc %{docs}
/sbin/*
%{_mandir}/man*/*
%lang(fr) %{_mandir}/fr.*/man*/*
%lang(cs) %{_mandir}/cs/man*/*

%files -n %{lib_name}
/%{_lib}/libiw.so.%{version}*

%files -n %{lib_name}-devel
/%{_lib}/libiw.so
%{_libdir}/libiw.so
%{_includedir}/iwlib.h
%{_includedir}/wireless.h
