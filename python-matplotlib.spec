%define	module	matplotlib
%define name	python-%{module}
%define version	1.1.1
%define	rel		1
%if %mdkversion < 201100
%define release	%mkrel %{rel}
%else
%define release %{rel}
%endif

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Matlab-style 2D plotting package for Python
Group:		Development/Python
License:	Python license
URL:		http://matplotlib.sourceforge.net/
Source0:	http://downloads.sourceforge.net/project/%{module}/%{module}/%{module}-%{version}/%{module}-%{version}.tar.gz
%{py_requires -d}
Patch0:		setupext-tk-include-0.99.1.2.patch
Patch1:		setupext-x86_64-libdir-1.1.1.patch
Requires:	python-numpy >= 1.1.0
Requires:	python-configobj, python-dateutil, python-pytz
Requires:	python-matplotlib-gtk = %{version}-%{release}
BuildRequires:	python-setuptools
BuildRequires:	python-numpy-devel >= 1.1.0
BuildRequires:	libwxPythonGTK-devel, pygtk2.0-devel, cairo-devel
BuildRequires:	tkinter, tcl-devel, tk-devel, freetype2-devel >= 2.1.7
BuildRequires:	python-qt, python-qt4
BuildRequires:  libpng-devel, zlib-devel 
BuildRequires:	python-configobj, python-dateutil, python-pytz
BuildRequires:	python-docutils, python-sphinx
BuildRequires:	ipython
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
matplotlib is a Python 2D plotting library which produces publication
quality figures in a variety of hardcopy formats and interactive
environments across platforms. matplotlib can be used in Python
scripts, the python and ipython shell (a la Matlab or Mathematica), web
application servers, and various graphical user interface toolkits.

%package cairo
Summary:	Cairo backend for matplotlib
Group:		Development/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-cairo >= 1.2.0

%description cairo
This package contains the Cairo backend for matplotlib.

%package emf
Summary:	EMF backend for matplotlib
Group:		Development/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-pyemf

%description emf
This package contains the EMF backend for matplotlib.

%package fltk
Summary:	FLTK backend for matplotlib
Group:		Development/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-pyfltk

%description fltk
This package contains the FLTK backend for matplotlib.

%package gtk
Summary:	GDK and GTK backends for matplotlib
Group:		Development/Python
Requires:	%{name} = %{version}-%{release}
Requires:	pygtk2.0 >= 2.4.0
Requires:	%{name}-cairo = %{version}-%{release}

%description gtk
This package contains the GDK and GTK backends for matplotlib.

%package qt
Summary:	Qt backend for matplotlib
Group:		Development/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-qt

%description qt
This package contains the Qt backend for matplotlib.

%package qt4
Summary:	Qt backend for matplotlib
Group:		Development/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-qt4

%description qt4
This package contains the Qt4 backend for matplotlib.

%package svg
Summary:	SVG backend for matplotlib
Group:		Development/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-pyxml

%description svg
This package contains the SVG backend for matplotlib.

%package tk
Summary:	Tk backend for matplotlib
Group:		Development/Python
Requires:	%{name} = %{version}-%{release}
Requires:	tkinter

%description tk
This package contains the Tk backend for matplotlib.

%package wx
Summary:	wxPython backend for matplotlib
Group:		Development/Python
Requires:	%{name} = %{version}-%{release}
Requires:	wxPython

%description wx
This package contains the wxPython backend for matplotlib.

%package doc
Summary:	Documentation for matplotlib
Group:		Development/Python
BuildArch: noarch

%description doc
This package contains documentation and sample code for matplotlib.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p0 -b .setupext
%patch1 -p0 -b .x86_64

%build
find -name .svn | xargs rm -rf

# Remove duplicate test data file:
%__rm -f lib/matplotlib/tests/baseline_images/test_axes/shaped\ data.svg

PYTHONDONTWRITEBYTECODE= %__python setup.py build

# Need to make built matplotlib libs available for the sphinx extensions:
pushd doc
export PYTHONPATH=`dir -d ../build/lib.linux*`
./make.py html
popd

%install
%__rm -rf %{buildroot}
PYTHONDONTWRITEBYTECODE= %__python setup.py install --root=%{buildroot} --record=FILELIST

%clean
%__rm -rf %{buildroot}

%files -f FILELIST
%defattr(-,root,root)
%exclude %{py_platsitedir}/%{module}/backends/backend_cairo.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_emf.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_fltkagg.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_gdk.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_gtk.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_gtkagg.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_gtkcairo.py*
%exclude %{py_platsitedir}/%{module}/backends/_backend_gdk.so
%exclude %{py_platsitedir}/%{module}/backends/_gtkagg.so
%exclude %{py_platsitedir}/%{module}/backends/backend_qt.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_qtagg.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_qt4.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_qt4agg.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_svg.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_tkagg.py*
%exclude %{py_platsitedir}/%{module}/backends/tkagg.py*
%exclude %{py_platsitedir}/%{module}/backends/_tkagg.so
%exclude %{py_platsitedir}/%{module}/backends/backend_wx.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_wxagg.py*

%files cairo
%defattr(-,root,root)
%{py_platsitedir}/%{module}/backends/backend_cairo.py*

%files emf
%defattr(-,root,root)
%{py_platsitedir}/%{module}/backends/backend_emf.py*

%files fltk
%defattr(-,root,root)
%{py_platsitedir}/%{module}/backends/backend_fltkagg.py*

%files gtk
%defattr(-,root,root)
%{py_platsitedir}/%{module}/backends/backend_gdk.py*
%{py_platsitedir}/%{module}/backends/backend_gtk.py*
%{py_platsitedir}/%{module}/backends/backend_gtkagg.py*
%{py_platsitedir}/%{module}/backends/backend_gtkcairo.py*
%{py_platsitedir}/%{module}/backends/_backend_gdk.so
%{py_platsitedir}/%{module}/backends/_gtkagg.so

%files qt
%defattr(-,root,root)
%{py_platsitedir}/%{module}/backends/backend_qt.py*
%{py_platsitedir}/%{module}/backends/backend_qtagg.py*

%files qt4
%defattr(-,root,root)
%{py_platsitedir}/%{module}/backends/backend_qt4.py*
%{py_platsitedir}/%{module}/backends/backend_qt4agg.py*

%files svg
%defattr(-,root,root)
%{py_platsitedir}/%{module}/backends/backend_svg.py*

%files tk
%defattr(-,root,root)
%{py_platsitedir}/%{module}/backends/backend_tkagg.py*
%{py_platsitedir}/%{module}/backends/tkagg.py*
%{py_platsitedir}/%{module}/backends/_tkagg.so

%files wx
%defattr(-,root,root)
%{py_platsitedir}/%{module}/backends/backend_wx.py*
%{py_platsitedir}/%{module}/backends/backend_wxagg.py*

%files doc
%doc examples/ CHANGELOG README.txt TODO doc/build/html/*
