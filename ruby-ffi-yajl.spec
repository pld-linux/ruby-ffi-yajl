#
# Conditional build:
%bcond_with	tests		# build without tests

%define	pkgname	ffi-yajl
Summary:	Ruby FFI wrapper around YAJL 2.x
Name:		ruby-%{pkgname}
Version:	1.2.0
Release:	0.1
License:	Apache v2.0
Group:		Development/Languages
Source0:	http://rubygems.org/downloads/%{pkgname}-%{version}.gem
# Source0-md5:	d507e47bd318e13b546b1b1f9c90a3fd
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
Requires:	ruby-libyajl2 < 2
Requires:	ruby-libyajl2 >= 1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Ruby FFI wrapper around YAJL 2.x

%prep
%setup -q -n %{pkgname}-%{version}
%{__sed} -i -e '1 s,#!.*ruby,#!%{__ruby},' bin/*

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{_bindir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -a bin/* $RPM_BUILD_ROOT%{_bindir}

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
%dir %{ruby_vendorlibdir}/ffi_yajl/ext
%dir %{ruby_vendorlibdir}/ffi_yajl/ffi
%{ruby_vendorlibdir}/ffi_yajl/ffi/encoder.rb
%{ruby_vendorlibdir}/ffi_yajl/ffi/parser.rb
