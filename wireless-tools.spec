%define sname wireless_tools
%define prever 9
%define major %{version}
%define libname %mklibname iw %{major}
%define devname %mklibname iw -d
%define _disable_lto 1
%define docs README INSTALL CHANGELOG.h DISTRIBUTIONS.txt COPYING PCMCIA.txt HOTPLUG-UDEV.txt

Summary:	Wireless ethernet configuration tools
Name:		wireless-tools
Version:	30
Release:	0.pre%{prever}.6
Group:		System/Kernel and hardware
License:	GPLv2
Url:		http://www.hpl.hp.com/personal/Jean_Tourrilhes/Linux/Tools.html
Source0:	http://www.hpl.hp.com/personal/Jean_Tourrilhes/Linux/%{sname}.%{version}.pre%{prever}.tar.gz
Patch2:		wireless_tools.27-wireless-man-upd.patch
Requires:	wireless-regdb

%description
This package contain the Wireless tools, used to manipulate
the Wireless Extensions. The Wireless Extension is an interface
allowing you to set Wireless LAN specific parameters and get the
specific stats for wireless networking equipment.

This is specifically useful since it allows manipulation of encryption
parameters possible with the GPL WaveLAN cards.

%package -n %{libname}
Summary:	Wireless_tools library
Group:		System/Libraries
Provides:	libiw

%description -n %{libname}
This package contains libraries to configure and access wireless interface
cards.

%package -n %{devname}
Summary:	Wireless_tools development library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	libiw-devel
Obsoletes:	%{_lib}iw30-devel
Obsoletes:	%{_lib}iw29-devel

%description -n %{devname}
This package contains libraries and headers for use in developing
wireless tools.

%prep
%setup -qn %{sname}.%{version}
%patch2 -p0
chmod a+r %{docs}

%build
%setup_compile_flags

# (tpg) enable build shared library
sed -i -e 's/BUILD_STATIC =.*/# BUILD_STATIC =.*/g' Makefile
# (tpg) pass our flags
sed -i -e 's#CFLAGS=#CFLAGS+=#' Makefile

%make clean
%make_build CC="%{__cc}"

%install
%make_install \
	PREFIX=%{buildroot}%{_prefix} \
	INSTALL_LIB=%{buildroot}/%{_lib} \
	INSTALL_MAN=%{buildroot}%{_mandir} \
	INSTALL_DIR=%{buildroot}/sbin

mkdir -p %{buildroot}%{_libdir}
ln -sf ../../%{_lib}/libiw.so.%{version} %{buildroot}%{_libdir}/libiw.so

%files
%doc %{docs}
/sbin/*
%{_mandir}/man*/*
%lang(fr) %{_mandir}/fr.*/man*/*
%lang(cs) %{_mandir}/cs/man*/*

%files -n %{libname}
/%{_lib}/libiw.so.%{major}*

%files -n %{devname}
/%{_lib}/libiw.so
%{_libdir}/libiw.so
%{_includedir}/iwlib.h
%{_includedir}/wireless.h

