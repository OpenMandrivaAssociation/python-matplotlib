%define with_html 1
%define	module	matplotlib

Summary:	Python 2D plotting library
Name:		python-%{module}
Version:	1.2.1
Release:	5
Group:		Development/Python
License:	Python license
Url:		http://matplotlib.sourceforge.net/
#Modified Sources to remove the one undistributable file
#See generate-tarball.sh in fedora cvs repository for logic
#sha1sum matplotlib-1.2.0-without-gpc.tar.gz
#92ada4ef4e7374d67e46e30bfb08c3fed068d680  matplotlib-1.2.0-without-gpc.tar.gz
Source0:	matplotlib-%{version}-without-gpc.tar.gz
Patch0:	%{name}-noagg.patch
Patch1:	%{name}-tk.patch

BuildRequires:	python-parsing
BuildRequires:	python-setuptools
BuildRequires:	ipython
BuildRequires:	python-configobj
BuildRequires:	python-dateutil
BuildRequires:	python-pytz
BuildRequires:	python-qt4
BuildRequires:	tkinter
BuildRequires:	x11-server-xvfb
BuildRequires:	python-numpy-devel >= 1.1.0
BuildRequires:	wxPythonGTK-devel
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(libagg)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(pygtk-2.0)
BuildRequires:	pkgconfig(tcl)
BuildRequires:	pkgconfig(tk)
BuildRequires:	pkgconfig(zlib)
%if %{with_html}
BuildRequires:	graphviz
BuildRequires:	texlive
BuildRequires:	python-docutils
BuildRequires:	python-sphinx
%endif
%{py_requires -d}
Requires:	python-configobj
Requires:	python-dateutil
Requires:	python-matplotlib-gtk = %{version}-%{release}
Requires:	python-numpy >= 1.1.0
Requires:	python-pytz

%description
Matplotlib is a python 2D plotting library which produces publication
quality figures in a variety of hardcopy formats and interactive
environments across platforms. matplotlib can be used in python
scripts, the python and ipython shell, web application servers, and
six graphical user interface toolkits.

Matplotlib tries to make easy things easy and hard things possible.
You can generate plots, histograms, power spectra, bar charts,
errorcharts, scatterplots, etc, with just a few lines of code.

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
BuildArch:	noarch

%description doc
This package contains documentation and sample code for matplotlib.

%prep
%setup -q -n %{module}-%{version}

# Remove bundled libraries
rm -r agg24 lib/matplotlib/pyparsing_py?.py

# Remove references to bundled libraries
%patch0 -p1 -b .noagg
sed -i -e s/matplotlib\.pyparsing_py./pyparsing/g lib/matplotlib/*.py

# Correct tcl/tk detection
%patch1 -p1 -b .tk
sed -i -e 's|@@libdir@@|%{_libdir}|' setupext.py

chmod -x lib/matplotlib/mpl-data/images/*.svg

%build
PYTHONDONTWRITEBYTECODE= xvfb-run %{__python} setup.py build

%if %{with_html}
# Need to make built matplotlib libs available for the sphinx extensions:
pushd doc
export PYTHONPATH=`realpath ../build/lib.linux*`
./make.py html
popd
%endif

%install
PYTHONDONTWRITEBYTECODE= %{__python} setup.py install --skip-build --root=%{buildroot}
chmod +x %{buildroot}%{python_sitearch}/matplotlib/dates.py
rm -rf %{buildroot}%{python_sitearch}/matplotlib/mpl-data/fonts

%files
%doc README.txt
%doc lib/dateutil_py2/LICENSE
%doc lib/matplotlib/mpl-data/fonts/ttf/LICENSE_STIX
%doc lib/pytz/LICENSE.txt
%doc CHANGELOG
%doc CXX
%doc INSTALL
%doc PKG-INFO
%doc TODO
%{python_sitearch}/*egg-info
%{python_sitearch}/%{module}/
%{python_sitearch}/mpl_toolkits/
%{python_sitearch}/pylab.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_cairo.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_emf.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_fltkagg.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_gdk.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_gtk.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_gtkagg.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_gtkcairo.py*
%exclude %{py_platsitedir}/%{module}/backends/_backend_gdk.so
%exclude %{py_platsitedir}/%{module}/backends/_gtkagg.so
%exclude %{py_platsitedir}/%{module}/backends/backend_qt4.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_qt4agg.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_svg.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_tkagg.py*
%exclude %{py_platsitedir}/%{module}/backends/tkagg.py*
%exclude %{py_platsitedir}/%{module}/backends/_tkagg.so
%exclude %{py_platsitedir}/%{module}/backends/backend_wx.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_wxagg.py*

%files cairo
%{py_platsitedir}/%{module}/backends/backend_cairo.py*

%files emf
%{py_platsitedir}/%{module}/backends/backend_emf.py*

%files fltk
%{py_platsitedir}/%{module}/backends/backend_fltkagg.py*

%files gtk
%{py_platsitedir}/%{module}/backends/backend_gdk.py*
%{py_platsitedir}/%{module}/backends/backend_gtk.py*
%{py_platsitedir}/%{module}/backends/backend_gtkagg.py*
%{py_platsitedir}/%{module}/backends/backend_gtkcairo.py*
%{py_platsitedir}/%{module}/backends/_backend_gdk.so
%{py_platsitedir}/%{module}/backends/_gtkagg.so

%files qt4
%{py_platsitedir}/%{module}/backends/backend_qt4.py*
%{py_platsitedir}/%{module}/backends/backend_qt4agg.py*

%files svg
%{py_platsitedir}/%{module}/backends/backend_svg.py*

%files tk
%{py_platsitedir}/%{module}/backends/backend_tkagg.py*
%{py_platsitedir}/%{module}/backends/tkagg.py*
%{py_platsitedir}/%{module}/backends/_tkagg.so

%files wx
%{py_platsitedir}/%{module}/backends/backend_wx.py*
%{py_platsitedir}/%{module}/backends/backend_wxagg.py*

%files doc
%doc examples/ CHANGELOG README.txt TODO
%if %{with_html}
%doc doc/build/html/*
%endif

