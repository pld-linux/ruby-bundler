%define pkgname bundler
Summary:	Bundles are fun
Name:		ruby-%{pkgname}
Version:	0.9.10
Release:	1
License:	Ruby's
Group:		Development/Languages
Source0:	http://rubygems.org/downloads/%{pkgname}-%{version}.gem
# Source0-md5:	70df782ee15b55a11664877b9700a648
Patch0:		%{name}-vendor.patch
URL:		http://rubyforge.org/projects/builder
BuildRequires:	rpmbuild(macros) >= 1.277
Requires:	ruby-thor
%{?ruby_mod_ver_requires_eq}
#BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# nothing to be placed there. we're not noarc only because of ruby packaging
%define		_enable_debug_packages	0

%description
Bundles are fun.

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
%setup -q -c
%{__tar} xf %{SOURCE0} -O data.tar.gz | %{__tar} xz
find -newer README.markdown -o -print | xargs touch --reference %{SOURCE0}
%patch0 -p1

rm lib/bundler/vendor/thor.rb
rm -r lib/bundler/vendor/thor
rm -r lib/bundler/vendor

%build
rdoc --op rdoc lib
rdoc --ri --op ri lib
rm ri/created.rid
rm -r ri/Gem

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_rubylibdir},%{ruby_ridir},%{ruby_rdocdir}}

cp -a lib/* $RPM_BUILD_ROOT%{ruby_rubylibdir}
cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}
cp -a rdoc $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{ruby_rubylibdir}/bundler
%{ruby_rubylibdir}/bundler.rb

%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}/Bundler
