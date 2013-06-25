%define		pkgname bundler
Summary:	Library and utilities to manage a Ruby application's gem dependencies
Name:		ruby-%{pkgname}
Version:	1.3.5
Release:	1
License:	MIT
Group:		Development/Languages
Source0:	http://rubygems.org/downloads/%{pkgname}-%{version}.gem
# Source0-md5:	b835af023d3e0dbe56b6fcc3841c90a6
URL:		http://github.com/carlhuda/bundler
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
BuildRequires:	sed >= 4.0
Requires:	ruby-net-http-persistent
Requires:	ruby-thor >= 0.17
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Bundler manages an application's dependencies through its entire life,
across many machines, systematically and repeatably

%package rdoc
Summary:	HTML documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla %{pkgname}
Group:		Documentation
Requires:	ruby >= 1:1.8.7-4

%description rdoc
HTML documentation for %{pkgname}.

%description rdoc -l pl.UTF-8
Dokumentacja w formacie HTML dla %{pkgname}.

%package ri
Summary:	ri documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie ri dla %{pkgname}
Group:		Documentation
Requires:	ruby

%description ri
ri documentation for %{pkgname}.

%description ri -l pl.UTF-8
Dokumentacji w formacie ri dla %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%{__sed} -i -e '1 s,#!.*ruby,#!%{__ruby},' bin/*

# do not generate shebang deps
chmod a-x lib/bundler/templates/Executable

# move, not to package
mv lib/bundler/vendor .

%build
rdoc --op rdoc lib
rdoc --ri --op ri lib
rm ri/created.rid
rm ri/cache.ri

# external pkgs
rm -r ri/Gem
rm ri/Object/cdesc-Object.ri

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{ruby_rubylibdir},%{ruby_ridir},%{ruby_rdocdir}}

cp -a bin/* $RPM_BUILD_ROOT%{_bindir}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_rubylibdir}
cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}
cp -a rdoc $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/bundle
%attr(755,root,root) %{_bindir}/bundle_ruby
%{ruby_rubylibdir}/bundler
%{ruby_rubylibdir}/bundler.rb

%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}/Bundler
