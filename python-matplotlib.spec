%define	module	matplotlib
%define	name	python-%{module}
%define	version	0.98.3
%define	release	%mkrel 1

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Matlab-style 2D plotting package for Python
Group:		Development/Python
License:	Python license
URL:		http://matplotlib.sourceforge.net/
Source0:	%{module}-%{version}.tar.lzma
Requires:	python >= 2.4, python-numpy >= 1.1.0
Requires:	pygtk2.0, wxPythonGTK, python-cairo >= 1.2.0
Requires:	python-configobj, python-dateutil, python-pytz
Requires:	python-enthought-traits, python-enthought-traits-ui
BuildRequires:	python-devel >= 2.4, python-numpy-devel >= 1.1.0
BuildRequires:	libwxPythonGTK-devel, pygtk2.0-devel, cairo-devel
BuildRequires:	tcl-devel, tk-devel, freetype2-devel >= 2.1.7
BuildRequires:  libpng-devel, zlib-devel 
BuildRequires:	python-configobj, python-dateutil, python-pytz
BuildRequires:	python-enthought-traits, python-enthought-traits-ui
BuildRequires:	python-docutils, python-sphinx, tetex-latex
BuildRequires:	ipython
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Matplotlib is a library for creating publication quality 2D plots of 
arrays in Python. It consists of three conceptual portions:

* the pylab interface - a set of functions that permit one 
  to interactively create plots with code similar to that used in Matlab.
* the matplotlib API - a set of classes that handle figure
  creation management, text, lines, plots, and so on.
* the backends - device dependent rendering systems that transform
  frontend plot representations into various graphic formats 
  (such as PS, PDF, SVG, and PNG) or translate them to display devices 
  (such as figures embedded in GTK+ or Wx applications).

%prep
%setup -q -n %{module}-%{version}

%build
find -name .svn | xargs rm -rf

%__python setup.py build

# Need to make built matplotlib libs available for the sphinx extensions:
pushd doc
export PYTHONPATH=`dir -d ../build/lib.linux*`
./make.py latex
popd

%install
%__rm -rf %{buildroot}
%__python setup.py install --root=%{buildroot} --record=FILELIST

%clean
%__rm -rf %{buildroot}

%files -f FILELIST
%defattr(-,root,root)
%doc license/ examples/ API_CHANGES CHANGELOG INSTALL INTERACTIVE KNOWN_BUGS TODO doc/build/latex/Matplotlib.pdf
