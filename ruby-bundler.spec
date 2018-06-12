#
# Conditional build:
%bcond_without	doc	# ri/rdoc documentation
%bcond_with	tests	# unit tests

%define		pkgname bundler
Summary:	Library and utilities to manage a Ruby application's gem dependencies
Summary(pl.UTF-8):	Biblioteka i narzędzia do zarządzania zależnościami gem aplikacji w języku Ruby
Name:		ruby-%{pkgname}
Version:	1.10.6
Release:	1
License:	MIT
Group:		Development/Languages
Source0:	http://rubygems.org/downloads/%{pkgname}-%{version}.gem
# Source0-md5:	e637c15440d29a7fad933d0de5be351a
Patch0:		%{name}-unvendor.patch
URL:		http://bundler.io/
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
BuildRequires:	ruby >= 1:1.8.7
BuildRequires:	ruby-rake >= 10.0
BuildRequires:	ruby-rubygems >= 1.3.6
BuildRequires:	sed >= 4.0
%if %{with tests}
BuildRequires:	ruby-ronn >= 0.7.3
BuildRequires:	ruby-ronn < 0.8
BuildRequires:	ruby-rspec >= 3.0
BuildRequires:	ruby-rspec < 3.1
%endif
# R molinillo, net-http-persistent, thor because we unvendored them: lib/bundler/vendored_persistent.rb
Requires:	ruby-molinillo >= 0.2.3
Requires:	ruby-net-http-persistent >= 2.9.3
Requires:	ruby-rubygems >= 1.3.6
Requires:	ruby-thor >= 0.19.1
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
%patch0 -p1

%{__sed} -i -e '1 s,#!.*ruby,#!%{__ruby},' bin/*

# do not generate shebang deps
chmod a-x lib/bundler/templates/Executable

# move, not to package
%{__mv} lib/bundler/vendor .

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
%{__rm} -r ri/Capistrano
%{__rm} -r ri/Rake
%{__rm} -r ri/lib/bundler/man
%{__rm} -r ri/lib/bundler/templates
%{__rm} ri/Object/cdesc-Object.ri
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{ruby_vendorlibdir},%{ruby_ridir},%{ruby_rdocdir}}

cp -a bin/* $RPM_BUILD_ROOT%{_bindir}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}

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
%doc CHANGELOG.md CODE_OF_CONDUCT.md ISSUES.md LICENSE.md README.md
%attr(755,root,root) %{_bindir}/bundle
%attr(755,root,root) %{_bindir}/bundle_ruby
%attr(755,root,root) %{_bindir}/bundler
%{ruby_vendorlibdir}/bundler
%{ruby_vendorlibdir}/bundler.rb
%{ruby_specdir}/%{pkgname}-%{version}.gemspec

%if %{with doc}
%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}/Bundler
%{ruby_ridir}/Object/gemfile-i.ri
%{ruby_ridir}/ParallelInstaller
%endif
