%define major 1
%define libname %mklibname va %{major}
%define devname %mklibname va -d

Summary:	Video Acceleration (VA) API for Linux
Name:		libva
Epoch:		2
Version:	1.8.0
Release:	1
Group:		System/Libraries
License:	MIT
Url:		http://freedesktop.org/wiki/Software/vaapi
Source0:	http://www.freedesktop.org/software/vaapi/releases/libva/%{name}-%{version}.tar.bz2
# utils
Source1:	https://github.com/01org/libva-utils/releases/download/%{version}/%{name}-utils-%{version}.tar.bz2
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(libdrm)
BuildRequires:	pkgconfig(pciaccess)
BuildRequires:	pkgconfig(udev)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xfixes)

%description
Libva is a library providing the VA API video acceleration API.

%package -n %{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n %{libname}
Libva is a library providing the VA API video acceleration API.

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package	utils
Summary:	Tools for %{name} (including vainfo)
Group:		System/Libraries

%description	utils
The %{name}-utils package contains tools that are provided as part
of %{name}, including the vainfo tool for determining what (if any)
%{name} support is available on a system.

%prep
%setup -q -a 1

%build
%configure \
	--disable-static \
	--enable-glx

%make

pushd %{name}-utils-%{version}
%configure
%make
popd

%install
%makeinstall_std
%makeinstall_std -C %{name}-utils-%{version}

# dummy driver has no good place, so get rid of it
rm %{buildroot}%{_libdir}/dri/dummy_drv_video.so

%files -n %{libname}
%{_libdir}/%{name}.so.%{major}*
%{_libdir}/%{name}-egl.so.%{major}*
%{_libdir}/%{name}-wayland.so.%{major}*
%{_libdir}/%{name}-drm.so.%{major}*
%{_libdir}/%{name}-glx.so.%{major}*
%{_libdir}/%{name}-tpi.so.%{major}*
%{_libdir}/%{name}-x11.so.%{major}*
%dir %{_libdir}/dri

%files -n %{devname}
%{_includedir}/va
%{_libdir}/%{name}*.so
%{_libdir}/pkgconfig/%{name}*.pc

%files utils
%doc COPYING
%{_bindir}/avcenc
%{_bindir}/jpegenc
%{_bindir}/mpeg2vaenc
%{_bindir}/h264encode
%{_bindir}/loadjpeg
%{_bindir}/mpeg2vldemo
%{_bindir}/putsurface*
%{_bindir}/vainfo
