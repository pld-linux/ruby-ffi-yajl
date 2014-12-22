# TODO
# - separate subpackages for C extension and FFI extension?
# - package bench as subpackage?
#
# Conditional build:
%bcond_with	tests		# build without tests

%define	pkgname	ffi-yajl
Summary:	Ruby FFI wrapper around YAJL 2.x
Name:		ruby-%{pkgname}
Version:	1.2.0
Release:	2
License:	Apache v2.0
Group:		Development/Languages
Source0:	http://rubygems.org/downloads/%{pkgname}-%{version}.gem
# Source0-md5:	d507e47bd318e13b546b1b1f9c90a3fd
Patch0:		system-yajl.patch
URL:		http://github.com/opscode/ffi-yajl
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
BuildRequires:	ruby-devel
BuildRequires:	sed >= 4.0
%if %{with tests}
BuildRequires:	ruby-mime-types < 2
BuildRequires:	ruby-mime-types >= 1.16
BuildRequires:	ruby-pry < 1
BuildRequires:	ruby-pry >= 0.9
BuildRequires:	ruby-rake < 11
BuildRequires:	ruby-rake >= 10.1
BuildRequires:	ruby-rake-compiler < 0.9
BuildRequires:	ruby-rake-compiler >= 0.8.3
BuildRequires:	ruby-rspec < 3
BuildRequires:	ruby-rspec >= 2.99
%endif
Requires:	ruby-ffi < 2
Requires:	ruby-ffi >= 1.5
# libyajl.so.2 opened by FFI
Requires:	yajl >= 2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Ruby FFI wrapper around YAJL 2.x

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%{__sed} -i -e '1 s,#!.*ruby,#!%{__ruby},' bin/*

%build
# write .gemspec
%__gem_helper spec

cd ext/ffi_yajl/ext/encoder
%{__ruby} extconf.rb
%{__make} V=1 \
	CC="%{__cc}" \
	LDFLAGS="%{rpmldflags}" \
	CFLAGS="%{rpmcflags} -fPIC"

cd ../parser
%{__ruby} extconf.rb
%{__make} V=1 \
	CC="%{__cc}" \
	LDFLAGS="%{rpmldflags}" \
	CFLAGS="%{rpmcflags} -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_specdir},%{_bindir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -a bin/* $RPM_BUILD_ROOT%{_bindir}
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

install -d $RPM_BUILD_ROOT%{ruby_vendorarchdir}/ffi_yajl/ext/{encoder,parser}
install -p ext/ffi_yajl/ext/parser/parser.so $RPM_BUILD_ROOT%{ruby_vendorarchdir}/ffi_yajl/ext/parser
install -p ext/ffi_yajl/ext/encoder/encoder.so $RPM_BUILD_ROOT%{ruby_vendorarchdir}/ffi_yajl/ext/encoder

%{__rm} $RPM_BUILD_ROOT%{ruby_vendorlibdir}/ffi_yajl/benchmark.rb
%{__rm} -r $RPM_BUILD_ROOT%{ruby_vendorlibdir}/ffi_yajl/benchmark
%{__rm} $RPM_BUILD_ROOT%{_bindir}/ffi-yajl-bench
%{__rm} $RPM_BUILD_ROOT%{ruby_vendorlibdir}/ffi_yajl/ext/.keep

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{ruby_vendorlibdir}/ffi_yajl.rb
%dir %{ruby_vendorlibdir}/ffi_yajl
%{ruby_vendorlibdir}/ffi_yajl/encoder.rb
%{ruby_vendorlibdir}/ffi_yajl/ext.rb
%{ruby_vendorlibdir}/ffi_yajl/ffi.rb
%{ruby_vendorlibdir}/ffi_yajl/json_gem.rb
%{ruby_vendorlibdir}/ffi_yajl/parser.rb
%{ruby_vendorlibdir}/ffi_yajl/version.rb
%dir %{ruby_vendorlibdir}/ffi_yajl/ffi
%{ruby_vendorlibdir}/ffi_yajl/ffi/encoder.rb
%{ruby_vendorlibdir}/ffi_yajl/ffi/parser.rb
%{ruby_specdir}/%{pkgname}-%{version}.gemspec

# ext
%dir %{ruby_vendorarchdir}/ffi_yajl
%dir %{ruby_vendorarchdir}/ffi_yajl/ext
%dir %{ruby_vendorarchdir}/ffi_yajl/ext/encoder
%dir %{ruby_vendorarchdir}/ffi_yajl/ext/parser
%attr(755,root,root) %{ruby_vendorarchdir}/ffi_yajl/ext/parser/parser.so
%attr(755,root,root) %{ruby_vendorarchdir}/ffi_yajl/ext/encoder/encoder.so
