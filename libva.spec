%define major 1
%define libname %mklibname va %{major}
%define develname %mklibname va -d

Name:		libva
Version:	1.1.1
Epoch:		2
Release:	1
Summary:	Video Acceleration (VA) API for Linux
Group:		System/Libraries
License:	MIT
URL:		http://freedesktop.org/wiki/Software/vaapi
Source0:	http://www.freedesktop.org/software/vaapi/releases/libva/%{name}-%{version}.tar.bz2
# grabbed from fedora (originally from sds)
#Patch0:		101_dont_install_test_programs.patch
BuildRequires:	pkgconfig(udev)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(libdrm)
#BuildRequires:	pkgconfig(egl)
BuildRequires:	libpciaccess-devel
BuildRequires:	pkgconfig(gl)


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
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{develname}
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package	utils
Summary:	Tools for %{name} (including vainfo)
Group:		System/Libraries
Requires:	%{libname} = %{EVRD}
Obsoletes:	vainfo < %{EVRD}

%description	utils
The %{name}-utils package contains tools that are provided as part
of %{name}, including the vainfo tool for determining what (if any)
%{name} support is available on a system.

%prep
%setup -q
# disable install of test programs
#patch0 -p1

%build
#autoreconf -i
%configure2_5x \
		--disable-static \
        --enable-glx

%make

%install
%makeinstall_std

find %{buildroot} -regex ".*\.la$" | xargs rm -f --

# dummy driver has no good place, so get rid of it
rm %{buildroot}%{_libdir}/dri/dummy_drv_video.so

%files -n %{libname}
%{_libdir}/%{name}.so.%{major}*
#{_libdir}/%{name}-egl.so.%{major}*
%{_libdir}/%{name}-drm.so.%{major}*
%{_libdir}/%{name}-glx.so.%{major}*
%{_libdir}/%{name}-tpi.so.%{major}*
%{_libdir}/%{name}-x11.so.%{major}*
%dir %{_libdir}/dri

%files -n %{develname}
%{_includedir}/va
%{_libdir}/%{name}*.so
%{_libdir}/pkgconfig/%{name}*.pc

%files utils
%doc COPYING
%{_bindir}/avcenc
%{_bindir}/h264encode
%{_bindir}/loadjpeg
%{_bindir}/mpeg2vldemo
%{_bindir}/putsurface*
%{_bindir}/vainfo
