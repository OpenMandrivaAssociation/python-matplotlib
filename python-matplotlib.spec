%define	module	matplotlib
%define	name	python-%{module}
%define	version	0.90.0
%define	rel	2
%define	release	%mkrel %{rel}

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Matlab-style 2D plotting package for Python
Group:		Development/Python
License:	Python license
URL:		http://matplotlib.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/matplotlib/%{module}-%{version}.tar.bz2
Source1:	users_guide_%{version}.pdf
Requires:	pygtk2.0, python-numeric, python-numarray, python-numpy
Requires:	wxPythonGTK, python-cairo >= 1.2.0
BuildRequires:	python-numeric-devel, python-numarray-devel, python-numpy-devel, pygtk2.0-devel 
BuildRequires:	libwxPythonGTK-devel, libwxgtk2.6-devel, cairo-devel
%if %mdkversion > 200600
BuildRequires:	tcl-devel, tk-devel, freetype-devel 
%elseqq
BuildRequires:  tcl, tk, devel(libfreetype)
%endif 
BuildRequires:  python-devel, libpng-devel, zlib-devel 
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
matplotlib is a 2D plotting library for Python which produces
publication quality figures in a variety of hardcopy formats and
interactive environments across platforms. matplotlib can be used in
Python scripts, the python and ipython shell (ala Matlab or
Mathematica), web application servers, and six graphical user
interface toolkits.

%prep
%setup -q -n %{module}-%{version} 
%__install -m 644 %{SOURCE1} ./

%build
find -name .cvsignore | xargs rm -rf

%__python setup.py build

%install
%__rm -rf %{buildroot}
%__python setup.py install --root=%{buildroot} --record=INSTALLED_FILES

%clean
%__rm -rf %{buildroot}

%files -f INSTALLED_FILES
%defattr(-,root,root)
%doc license/ examples/ README TODO CHANGELOG INSTALL INTERACTIVE KNOWN_BUGS PKG-INFO API_CHANGES NUMARRAY_ISSUES users_guide_%{version}.pdf


