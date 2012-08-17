%define major		1
%define libname		%mklibname va %{major}
%define develname	%mklibname va -d

Name:		libva
#bump to 1.0.16 and remove older 1.1.0... upstream tagged it and then removed the tag...
Version:	1.0.16
Release:	1
Summary:	Video Acceleration (VA) API for Linux
Group:		System/Libraries
License:	MIT
URL:		http://freedesktop.org/wiki/Software/vaapi
Source0:	http://cgit.freedesktop.org/vaapi/%{name}/snapshot/%{name}-%{version}.tar.bz2
BuildRequires:	udev-devel
BuildRequires:	libxext-devel
BuildRequires:	libxfixes-devel
BuildRequires:	libdrm-devel
BuildRequires:	pkgconfig(egl)
BuildRequires:	libpciaccess-devel
BuildRequires:	mesagl-devel
Epoch:		2

%description
Libva is a library providing the VA API video acceleration API.

%package -n %{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n %{libname}
Libva is a library providing the VA API video acceleration API.

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package	utils
Summary:	Tools for %{name} (including vainfo)
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	vainfo

%description	utils
The %{name}-utils package contains tools that are provided as part
of %{name}, including the vainfo tool for determining what (if any)
%{name} support is available on a system.

%prep
%setup -q
# % {name}-% {version}

%build
autoreconf -v -i 
%configure2_5x --disable-static --enable-glx
%make

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
find %{buildroot} -regex ".*\.la$" | xargs rm -f --

# dummy driver has no good place, so get rid of it
rm %{buildroot}%{_libdir}/dri/dummy_drv_video.so

%files -n %{libname}
#%{_libdir}/%{name}.so.%{major}*
%{_libdir}/%{name}*.so.%{major}*

%files -n %{develname}
%{_includedir}/va
%{_libdir}/%{name}*.so
%{_libdir}/pkgconfig/%{name}*.pc

%files utils
%doc COPYING
%{_bindir}/vainfo
%{_bindir}/avcenc
#%{_bindir}/va_egl
%{_bindir}/loadjpeg
%{_bindir}/h264encode
%{_bindir}/mpeg2vldemo
%{_bindir}/putsurface
