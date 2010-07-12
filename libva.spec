%define sdsver	1+sds3
%define sver	0.31.1
%define uver	%sver-%sdsver

%define major		1
%define libname		%mklibname va %{major}
%define develname	%mklibname va -d

%define compat_major	0
%define compat_libname	%mklibname va-compat %{compat_major}

Name:		libva
# The rather complex versioning is due to the upstream being a patched
# version of the real upstream libva; when the real upstream 0.5 comes
# out we will no longer need to use Gwenole's patched version of 0.3
Version:	%(echo %uver | tr +- ..)
Release:	%{mkrel 1}
Summary:	Video Acceleration (VA) API for Linux
Group:		System/Libraries
License:	MIT
URL:		http://www.splitted-desktop.com/~gbeauchesne/libva/
Source0:	http://www.splitted-desktop.com/~gbeauchesne/libva/%{name}_%{uver}.tar.gz
# (Anssi 07/2010) disable SDS soname mangling as the SDS patches do not seem
# to currently break ABI backward compatibility
Patch0:		libva-sds-no-soname-change.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	libtool
BuildRequires:	libxext-devel
BuildRequires:	libxfixes-devel
BuildRequires:	libdrm-devel
BuildRequires:	GL-devel

%description
Libva is a library providing the VA API video acceleration API.

%package -n vainfo
Summary:	VA-API information tool
Group:		Video
Conflicts:	libva < 0.31.1
Obsoletes:	libva-test < 0.31.1

%description -n vainfo
Libva is a library providing the VA API video acceleration API.
This packages provides the vainfo tool showing VA-API information.

%package -n vaapi-driver-i965
Summary:	VA-API driver for Intel i965
Group:		System/Kernel and hardware
# old 'libva' package contained i965 + vainfo
Obsoletes:	libva < 0.31.1

%description -n vaapi-driver-i965
Intel integrated G45 graphics chips driver for VA API, a video
acceleration API.

%package -n %{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n %{libname}
Libva is a library providing the VA API video acceleration API.

%package -n %{compat_libname}
Summary:	Shared library for %{name}-compat
Group:		System/Libraries
Conflicts:	%{_lib}va1 < 0.31.1

%description -n %{compat_libname}
Libva is a library providing the VA API video acceleration API.
This package provides a compatilibity layer for old %{name}.

%package -n %{develname}
Summary:	Development headers for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{compat_libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
Libva is a library providing the VA API video acceleration API. This
package contains libraries and header files for developing applications
that use %{name}.

%prep
%setup -q -n %{name}-%{sver}
%apply_patches
for p in debian/patches/*.patch; do patch -p1 < $p; done

%build
autoreconf -i
%configure2_5x --disable-static --enable-glx --enable-i965-driver
%make

%install
rm -rf %{buildroot}
%makeinstall_std

# this is a compatibility name for some older apps which don't use the
# newer soname
echo ".text"|gcc -xassembler - -o %{buildroot}%{_libdir}/libva.so.0 -shared -Wl,-soname,libva.so.0 -Wl,-z,noexecstack -L%{buildroot}%{_libdir} -lva-x11

find %{buildroot} -regex ".*\.la$" | xargs rm -f --

# dummy driver has no good place, so get rid of it
rm %{buildroot}%{_libdir}/va/drivers/dummy_drv_video.so

%clean
rm -rf %{buildroot}

%files -n vainfo
%defattr(-,root,root,-)
%{_bindir}/vainfo

%files -n vaapi-driver-i965
%defattr(-,root,root,-)
%{_libdir}/va/drivers/i965_drv_video.so

%files -n %{libname}
%defattr(-,root,root,-)
%{_libdir}/%{name}.so.%{major}*
%{_libdir}/%{name}-glx.so.%{major}*
%{_libdir}/%{name}-tpi.so.%{major}*
%{_libdir}/%{name}-x11.so.%{major}*
%dir %{_libdir}/va
%dir %{_libdir}/va/drivers

%files -n %{compat_libname}
%defattr(-,root,root,-)
%{_libdir}/%{name}.so.%{compat_major}*
%{_libdir}/%{name}-compat.so.%{compat_major}*

%files -n %{develname}
%defattr(-,root,root,-)
%{_includedir}/va
%{_libdir}/%{name}*.so
%{_libdir}/pkgconfig/%{name}*.pc
