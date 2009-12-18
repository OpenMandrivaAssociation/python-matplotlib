%define	module	matplotlib

Name:		python-%{module}
Version:	0.99.1.2
Release:	%{mkrel 1}
Summary:	Matlab-style 2D plotting package for Python
Group:		Development/Python
License:	Python license
URL:		http://matplotlib.sourceforge.net/
Source0:	http://downloads.sourceforge.net/project/%{module}/%{module}/%{module}-%{version}/%{module}-%{version}.tar.gz
%{py_requires -d}
Requires:	python-numpy >= 1.1.0
Requires:	pygtk2.0, wxPythonGTK, python-cairo >= 1.2.0
Requires:	python-configobj, python-dateutil, python-pytz
Requires:	python-qt, python-qt4
BuildRequires:	python-setuptools
BuildRequires:	python-numpy-devel >= 1.1.0
BuildRequires:	libwxPythonGTK-devel, pygtk2.0-devel, cairo-devel
BuildRequires:	tcl-devel, tk-devel, freetype2-devel >= 2.1.7
BuildRequires:	python-qt, python-qt4
BuildRequires:  libpng-devel, zlib-devel 
BuildRequires:	python-configobj, python-dateutil, python-pytz
BuildRequires:	python-docutils, python-sphinx
BuildRequires:	ipython
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
matplotlib is a python 2D plotting library which produces publication
quality figures in a variety of hardcopy formats and interactive
environments across platforms. matplotlib can be used in python
scripts, the python and ipython shell (ala matlab or mathematica), web
application servers, and various graphical user interface toolkits.

%prep
%setup -q -n %{module}-0.99.1.1

%build
find -name .svn | xargs rm -rf

%__python setup.py build

# Need to make built matplotlib libs available for the sphinx extensions:
pushd doc
export PYTHONPATH=`dir -d ../build/lib.linux*`
./make.py html
popd

%install
%__rm -rf %{buildroot}
%__python setup.py install --root=%{buildroot} --record=FILELIST

%clean
%__rm -rf %{buildroot}

%files -f FILELIST
%defattr(-,root,root)
%doc license/ examples/ CHANGELOG INSTALL INTERACTIVE KNOWN_BUGS TODO doc/build/html/*
