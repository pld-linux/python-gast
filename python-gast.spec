#
# Conditional build:
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Python AST that abstracts the underlying Python version
Summary(pl.UTF-8):	Pythonowe AST niezależne od wersji Pythona
Name:		python-gast
Version:	0.5.3
Release:	2
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/gast/
Source0:	https://files.pythonhosted.org/packages/source/g/gast/gast-%{version}.tar.gz
# Source0-md5:	fdff900805e03e9dd76d377eb4cbaed7
Patch0:		gast-python2.patch
URL:		https://pypi.org/project/gast/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A generic AST to represent Python2 and Python3's Abstract Syntax Tree
(AST). GAST provides a compatibility layer between the AST of various
Python versions, as produced by "ast.parse" from the standard "ast"
module.

%description -l pl.UTF-8
Ogólne AST reprezentujące abstrakcyjne drzewo składniowe (Abstract
Syntax Tree) Pythona 2 i 3. GAST zapewnia warstwę zgodności między AST
różnych wersji Pythona, w postaci tworzonej przez "ast.parse" ze
standardowego modułu "ast".

%package -n python3-gast
Summary:	Python AST that abstracts the underlying Python version
Summary(pl.UTF-8):	Pythonowe AST niezależne od wersji Pythona
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-gast
A generic AST to represent Python2 and Python3's Abstract Syntax Tree
(AST). GAST provides a compatibility layer between the AST of various
Python versions, as produced by "ast.parse" from the standard "ast"
module.

%description -n python3-gast -l pl.UTF-8
Ogólne AST reprezentujące abstrakcyjne drzewo składniowe (Abstract
Syntax Tree) Pythona 2 i 3. GAST zapewnia warstwę zgodności między AST
różnych wersji Pythona, w postaci tworzonej przez "ast.parse" ze
standardowego modułu "ast".

%prep
%setup -q -n gast-%{version}
%patch -P 0 -p1

%build
%if %{with python2}
%py_build
# deprecated target, but sometimes still used: %{?with_tests:test}

%if %{with tests}
#PYTHONPATH=$(pwd)
%{__python} -m unittest discover -s tests
# -t $(pwd)
## use explicit plugins list for reliable builds (delete PYTEST_PLUGINS if empty)
#PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
#PYTEST_PLUGINS= \
#%{__python} -m pytest ...
%endif
%endif

%if %{with python3}
%py3_build
# deprecated target, but sometimes still used: %{?with_tests:test}

%if %{with tests}
#PYTHONPATH=$(pwd)
%{__python3} -m unittest discover -s tests
## use explicit plugins list for reliable builds (delete PYTEST_PLUGINS if empty)
#PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
#PYTEST_PLUGINS= \
#%{__python3} -m pytest ...
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE README.rst
%{py_sitescriptdir}/gast
%{py_sitescriptdir}/gast-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-gast
%defattr(644,root,root,755)
%doc LICENSE README.rst
%{py3_sitescriptdir}/gast
%{py3_sitescriptdir}/gast-%{version}-py*.egg-info
%endif
