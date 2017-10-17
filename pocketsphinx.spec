%define basepkg pocketsphinx
Summary: CMU PocketSphinx
Name: %{basepkg}
Version: 4.5preAlpha.1
Release: 2
License: BSD Style License
Group: System Environment/Libraries
URL: https://github.com/cmusphinx/pocketsphinx
Source0: http://downloads.sourceforge.net/project/cmusphinx/sphinxbase/5prealpha/sphinxbase-5prealpha.tar.gz
Source1: http://downloads.sourceforge.net/project/cmusphinx/pocketsphinx/5prealpha/pocketsphinx-5prealpha.tar.gz
BuildRoot: %{_tmppath}/%{basepkg}-%{version}-%{release}-buildroot
BuildRequires: autoconf, automake, bison, bzip2, gcc-c++, libtool, libuuid-devel, make, pulseaudio-libs-devel
BuildRequires: findutils, chrpath, python-devel, swig, tar, wget
Requires: pulseaudio, pulseaudio-libs, pulseaudio-utils, python, python-libs


%description
This is PocketSphinx, one of Carnegie Mellon University's open source large vocabulary, 
speaker-independent continuous speech recognition engine.

%package devel
Group: Development/Libraries
Summary: CMU PocketSphinx development kit
Requires: lcsas_pocketsphinx = %{version}

%description devel
This package provides the support files which can be used to 
build applications using the  CMU PocketSphinx library.

%prep
%setup -q -c -n %{basepkg} -a 0 -a 1

%build
ln -s sphinxbase-5prealpha sphinxbase
pushd sphinxbase
./configure
make
popd

ln -s pocketsphinx-5prealpha pocketsphinx
pushd pocketsphinx
./configure
make
popd

%check
# Run non-interactive tests


%install
pushd sphinxbase
make install DESTDIR=$RPM_BUILD_ROOT
popd

pushd pocketsphinx
make install DESTDIR=$RPM_BUILD_ROOT
popd

find $RPM_BUILD_ROOT/usr/local/bin -executable -type f -print0 | xargs -0 chrpath -d
find $RPM_BUILD_ROOT/usr/local/lib -name "lib*so*" -type f -print0 | xargs -0 chrpath -d
find $RPM_BUILD_ROOT/usr/local/lib64/ -name "*sphinx*so*" -type f -print0 | xargs -0 chrpath -d

mkdir -p $RPM_BUILD_ROOT/etc/ld.so.conf.d
echo /usr/local/lib > $RPM_BUILD_ROOT/etc/ld.so.conf.d/pocketsphinx.conf

%post
ldconfig

%postun
ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/etc/ld.so.conf.d/pocketsphinx.conf
/usr/local/bin/pocketsphinx_*
/usr/local/bin/sphinx_*
/usr/local/lib/libpocketsphinx.so*
/usr/local/lib/libsphinx*.so*
/usr/local/lib64/python2.7/site-packages/pocketsphinx
/usr/local/lib64/python2.7/site-packages/sphinxbase
%doc /usr/local/share/man/man1/pocketsphinx_*.1
%doc /usr/local/share/man/man1/sphinx_*.1
/usr/local/share/pocketsphinx
/usr/local/share/sphinxbase


%files devel
%defattr(-,root,root,-)
/usr/local/include/pocketsphinx
/usr/local/include/sphinxbase
/usr/local/lib/libpocketsphinx.*a
/usr/local/lib/libsphinx*.*a
/usr/local/lib/pkgconfig/pocketsphinx.pc
/usr/local/lib/pkgconfig/sphinxbase.pc



%changelog
* Tue Oct 17 2017 Steve Simpson <software@lcsas.us> 4.5preAlpha.1-2
- Installed Shared Libs

* Mon Oct 16 2017 Steve Simpson <software@lcsas.us> 4.5preAlpha.1-1
- Initial RPM Build
