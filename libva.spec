%define uver	0.31.0-1+sds9
%define sver	0.31.0
%define apiver	0.31

%define major		1
%define libname		%mklibname va %{major}
%define develname	%mklibname va -d

Name:		libva
# The rather complex versioning is due to the upstream being a patched
# version of the real upstream libva; when the real upstream 0.5 comes
# out we will no longer need to use Gwenole's patched version of 0.3
Version:	0.31.0.1.sds9
Release:	%{mkrel 1}
Summary:	Video Acceleration (VA) API for Linux
Group:		System/Libraries
License:	MIT
URL:		http://www.splitted-desktop.com/~gbeauchesne/libva/
Source0:	http://www.splitted-desktop.com/~gbeauchesne/libva/%{name}_%{uver}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	libtool
BuildRequires:	libxext-devel
BuildRequires:	libxfixes-devel
BuildRequires:	libdrm-devel
BuildRequires:	GL-devel

%description
Libva is a library providing the VA API video acceleration API.

%package -n %{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n %{libname}
Libva is a library providing the VA API video acceleration API.

%package -n %{develname}
Summary:	Development headers for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
Libva is a library providing the VA API video acceleration API. This
package contains libraries and header files for developing applications
that use %{name}.

%prep
%setup -q -n %{name}-%{sver}
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
echo ".text"|gcc -xassembler - -o %{buildroot}%{_libdir}/libva.so.%{apiver} -shared -Wl,-soname,libva.so.0 -Wl,-z,noexecstack -L%{buildroot}%{_libdir} -lva-x11
ln -s libva.so.%{apiver} %{buildroot}%{_libdir}/libva.so.0

find %{buildroot} -regex ".*\.la$" | xargs rm -f --

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_libdir}/va
%{_bindir}/vainfo

%files -n %{libname}
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/%{name}*.so.*

%files -n %{develname}
%defattr(-,root,root,-)
%{_includedir}/va
%{_libdir}/%{name}*.so
%{_libdir}/pkgconfig/%{name}*.pc
