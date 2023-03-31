%define major 1
%define libname %mklibname va %{major}
%define devname %mklibname va -d
# disable utils after upgrade, that build libva
# and enable utils
%bcond_with utils
# No -devel for compat packages...
%bcond_with devel

Summary:	Video Acceleration (VA) API for Linux
Name:		libva1
Version:	1.8.3
Release:	2
Group:		System/Libraries
License:	MIT
Url:		http://freedesktop.org/wiki/Software/vaapi
Source0:	http://www.freedesktop.org/software/vaapi/releases/libva/libva-%{version}.tar.bz2
# utils
Source1:	https://github.com/01org/libva-utils/releases/download/%{version}/libva-utils-%{version}.tar.bz2
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(libdrm)
BuildRequires:	pkgconfig(pciaccess)
BuildRequires:	pkgconfig(udev)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(wayland-client)

%description
Libva is a library providing the VA API video acceleration API.

%if "%{_lib}" != "lib"
%package -n %{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n %{libname}
Libva is a library providing the VA API video acceleration API.
%endif

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%if %{with utils}
%package	utils
Summary:	Tools for %{name} (including vainfo)
Group:		System/Libraries
BuildRequires:	%{name}-devel = %{EVRD}

%description	utils
The %{name}-utils package contains tools that are provided as part
of %{name}, including the vainfo tool for determining what (if any)
%{name} support is available on a system.
%endif

%prep
%setup -n libva-%{version} -a 1

%build
%configure \
	--disable-static \
	--enable-glx

%make

%if %{with utils}
pushd %{name}-utils-%{version}
%configure
%make
popd
%endif

%install
%makeinstall_std
%if %{with utils}
%makeinstall_std -C libva-utils-%{version}
%endif
%if ! %{with devel}
rm -rf %{buildroot}%{_includedir} \
	%{buildroot}%{_libdir}/*.so \
	%{buildroot}%{_libdir}/pkgconfig
%endif

%if "%{_lib}" != "lib"
%files -n %{libname}
%else
%files
%endif
%{_libdir}/libva.so.%{major}*
%{_libdir}/libva-egl.so.%{major}*
%{_libdir}/libva-wayland.so.%{major}*
%{_libdir}/libva-drm.so.%{major}*
%{_libdir}/libva-glx.so.%{major}*
%{_libdir}/libva-tpi.so.%{major}*
%{_libdir}/libva-x11.so.%{major}*

%if %{with devel}
%files -n %{devname}
%doc COPYING
%{_includedir}/va
%{_libdir}/libva*.so
%{_libdir}/pkgconfig/libva*.pc
%endif

%if %{with utils}
%files utils
%{_bindir}/avcenc
%{_bindir}/jpegenc
%{_bindir}/mpeg2vaenc
%{_bindir}/h264encode
%{_bindir}/loadjpeg
%{_bindir}/mpeg2vldemo
%{_bindir}/putsurface*
%{_bindir}/vainfo
%endif
