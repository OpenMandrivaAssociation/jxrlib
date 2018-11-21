%define major   0
%define libname %mklibname jxr %{major}
%define devname %mklibname jxr -d

Name:           jxrlib
Version:        1.1
Release:        %mkrel 2
Summary:        Open source implementation of jpegxr
Group:          System/Libraries

# See JPEGXR_DPK_Spec_1.0.doc. Upstream request for plain text license file at
# https://jxrlib.codeplex.com/workitem/13
License:        BSD
URL:            https://jxrlib.codeplex.com/
Source0:        http://jxrlib.codeplex.com/downloads/get/685249#/jxrlib_%(echo %{version} | tr . _).tar.gz
# Use CMake to build to facilitate creation of shared libraries
# See https://jxrlib.codeplex.com/workitem/13
Source1:        CMakeLists.txt
# Converted from shipped doc/JPEGXR_DPK_Spec_1.doc
# libreoffice --headless --convert-to pdf doc/JPEGXR_DPK_Spec_1.0.doc
Source2:        JPEGXR_DPK_Spec_1.0.pdf

# Fix various warnings, upstreamable
# See https://jxrlib.codeplex.com/workitem/13
Patch0:         jxrlib_warnings.patch

BuildRequires:  cmake

%description
This is an open source implementation of the jpegxr image format standard.

#----------------------------------------------------------------------

%package -n %{libname}
Summary:        Open source implementation of jpegxr
Group:          System/Libraries
Requires:       %{libname} = %{version}-%{release}

%description -n %{libname}
This package contains libraries and header files for
developing applications that use %{name}.

#----------------------------------------------------------------------

%package -n %{devname}
Summary:        Development files for %{name}
Group:          Development/C
Requires:       %{libname} = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains libraries and header files for
developing applications that use %{name}.

#----------------------------------------------------------------------

%prep
%setup -q -n %{name}

# Sanitize charset and line endings
for file in `find . -type f -name '*.c' -or -name '*.h' -or -name '*.txt'`; do
  iconv --from=ISO-8859-15 --to=UTF-8 $file > $file.new && \
  sed -i 's|\r||g' $file.new && \
  touch -r $file $file.new && mv $file.new $file
done

%patch0 -p1

# Remove shipped binaries
rm -rf bin

cp -a %{SOURCE1} .
cp -a %{SOURCE2} doc

%build
%cmake
%make_build

%install
%make_install -C build

%files -n %{libname}
%doc doc/readme.txt doc/JPEGXR_DPK_Spec_1.0.pdf
%{_libdir}/libjpegxr.so.%{major}{,.*}
%{_libdir}/libjxrglue.so.%{major}{,.*}

%files -n %{devname}
%{_bindir}/JxrEncApp
%{_bindir}/JxrDecApp
%{_includedir}/%{name}/
%{_libdir}/libjpegxr.so
%{_libdir}/libjxrglue.so
