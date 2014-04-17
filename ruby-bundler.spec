#
# Conditional build:
%bcond_without	doc			# don't build ri/rdoc

%define		pkgname bundler
Summary:	Library and utilities to manage a Ruby application's gem dependencies
Summary(pl.UTF-8):	Biblioteka i narzędzia do zarządzania zależnościami gem aplikacji w języku Ruby
Name:		ruby-%{pkgname}
Version:	1.6.2
Release:	1
License:	MIT
Group:		Development/Languages
Source0:	http://rubygems.org/downloads/%{pkgname}-%{version}.gem
# Source0-md5:	c198088c19b0aae57cf0fbf228b2081e
URL:		http://github.com/carlhuda/bundler
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
BuildRequires:	sed >= 4.0
# because we unvendored it: lib/bundler/vendored_persistent.rb
Requires:	ruby-net-http-persistent
Requires:	ruby-thor >= 0.17
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Bundler manages an application's dependencies through its entire life,
across many machines, systematically and repeatably.

%description -l pl.UTF-8
Bundler zarządza zależnościami aplikacji przez cały jej żywot, na
wielu maszynach, systematycznie i powtarzalnie.

%package rdoc
Summary:	HTML documentation for Ruby bundler package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML do pakietu bundler dla języka Ruby
Group:		Documentation
Requires:	ruby >= 1:1.8.7-4

%description rdoc
HTML documentation for Ruby bundler package.

%description rdoc -l pl.UTF-8
Dokumentacja w formacie HTML do pakietu bundler dla języka Ruby.

%package ri
Summary:	ri documentation for Ruby bundler package
Summary(pl.UTF-8):	Dokumentacja w formacie ri do pakietu bundler dla języka Ruby
Group:		Documentation
Requires:	ruby

%description ri
ri documentation for Ruby bundler package.

%description ri -l pl.UTF-8
Dokumentacja w formacie ri do pakietu bundler dla języka Ruby.

%prep
%setup -q -n %{pkgname}-%{version}

%{__sed} -i -e '1 s,#!.*ruby,#!%{__ruby},' bin/*

# do not generate shebang deps
chmod a-x lib/bundler/templates/Executable

# move, not to package
mv lib/bundler/vendor .

%build
# write .gemspec
%__gem_helper spec

%if %{with doc}
rdoc --op rdoc lib
rdoc --ri --op ri lib
%{__rm} ri/created.rid
%{__rm} ri/cache.ri

# external pkgs
%{__rm} -r ri/Gem
%{__rm} ri/Object/cdesc-Object.ri
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{ruby_rubylibdir},%{ruby_ridir},%{ruby_rdocdir}}

cp -a bin/* $RPM_BUILD_ROOT%{_bindir}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_rubylibdir}

# install gemspec
install -d $RPM_BUILD_ROOT%{ruby_specdir}
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%if %{with doc}
cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}
cp -a rdoc $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/bundle
%attr(755,root,root) %{_bindir}/bundle_ruby
%attr(755,root,root) %{_bindir}/bundler
%{ruby_rubylibdir}/bundler
%{ruby_rubylibdir}/bundler.rb
%{ruby_specdir}/%{pkgname}-%{version}.gemspec

%if %{with doc}
%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}/Bundler
%endif
