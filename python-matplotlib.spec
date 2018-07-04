%define module matplotlib
%bcond_without python2

%global with_html 0
%global run_tests 0

# the default backend; one of GTK GTKAgg GTKCairo GTK3Agg GTK3Cairo
# CocoaAgg MacOSX Qt4Agg Qt5Agg TkAgg Agg Cairo GDK PS PDF SVG
%global backend Qt5Agg

# https://fedorahosted.org/fpc/ticket/381
%global with_bundled_fonts 1

Summary:	Python 2D plotting library
Name:		python-%{module}
Version:	2.2.2
Release:	1
Group:		Development/Python
License:	Python license
Url:		http://matplotlib.sourceforge.net/
Source0:	https://github.com/matplotlib/matplotlib/archive/v%{version}.tar.gz
Source1:	setup.cfg
Patch0:		matplotlib-2.1.1-datafile-search-path.patch
Patch1:		matplotlib-2.1.1-32bit-compile.patch

BuildRequires:	python-parsing
BuildRequires:	python-setuptools
BuildRequires:	ipython
BuildRequires:	python-configobj
BuildRequires:	python-pkg-resources
BuildRequires:	python-cxx-devel
BuildRequires:	python-dateutil
BuildRequires:	python-pytz
BuildRequires:	python-qt5
BuildRequires:	python-qt5-devel
BuildRequires:	qhull-devel
BuildRequires:	tkinter
BuildRequires:	python-numpy-devel >= 1.1.0
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(freetype2)
#BuildRequires:	pkgconfig(libagg)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(tcl)
BuildRequires:	pkgconfig(tk)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(python3)
%if %{with_html}
BuildRequires:	graphviz
BuildRequires:	texlive
BuildRequires:	python-docutils
BuildRequires:	python-sphinx
BuildRequires:	python-numpydoc
%endif
Requires:	python-configobj
Requires:	python-dateutil
Requires:	python-numpy >= 1.1.0
Requires:	python-pytz
Requires:	%{name}-data = %{version}-%{release}

# GTKAgg does not require extra subpackages, but does not work with python3
%if "%{backend}" == "TkAgg"
Requires:	%{name}-tk%{?_isa} = %{version}-%{release}
%else
%if "%{backend}" == "Qt5Agg"
Requires:	%{name}-qt5%{?_isa} = %{version}-%{release}
%endif
%endif

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

%package gtk
Summary:       GDK and GTK backends for matplotlib
Group:         Development/Python
Requires:      %{name} = %{version}-%{release}
Requires:      pygtk2.0 >= 2.4.0
Requires:      %{name}-cairo = %{version}-%{release}

%description gtk
This package contains the GDK and GTK backends for matplotlib.


%package qt5
Summary:	Qt backend for matplotlib
Group:		Development/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-qt5

%description qt5
This package contains the Qt5 backend for matplotlib.

%package svg
Summary:	SVG backend for matplotlib
Group:		Development/Python
Requires:	%{name} = %{version}-%{release}

%description svg
This package contains the SVG backend for matplotlib.

%package tk
Summary:	Tk backend for matplotlib
Group:		Development/Python
Requires:	%{name} = %{version}-%{release}
Requires:	tkinter

%description tk
This package contains the Tk backend for matplotlib.

%package doc
Summary:	Documentation for matplotlib
Group:		Development/Python
BuildArch:	noarch

%description doc
This package contains documentation and sample code for matplotlib.

%package        data
Summary:        Data used by python-matplotlib
%if %{with_bundled_fonts}
Requires:       %{name}-data-fonts = %{version}-%{release}
%endif
BuildArch:      noarch

%description    data
%{summary}

%if %{with_bundled_fonts}
%package        data-fonts
Summary:        Fonts used by python-matplotlib
Requires:       %{name}-data = %{version}-%{release}
BuildArch:      noarch

%description    data-fonts
%{summary}
%endif

%if %{with python2}
%package -n python2-matplotlib
Summary:	Python 2.x version of matplotlib
Group:		Development/Python
Requires:       %{name}-data = %{version}-%{release}
BuildRequires:	python2-pytz
BuildRequires:	tkinter2
BuildRequires:	python2-numpy-devel >= 1.1.0
BuildRequires:	python2-cxx-devel
BuildRequires:	pkgconfig(python)
BuildRequires:	python2-setuptools
BuildRequires:	python2-pkg-resources

%description -n python2-matplotlib
Python 2.x version of matplotlib

%package -n python2-matplotlib-cairo
Summary:	Cairo backend for matplotlib
Group:		Development/Python
Requires:	python2-matplotlib = %{version}-%{release}
Requires:	python-cairo >= 1.2.0

%description -n python2-matplotlib-cairo
This package contains the Cairo backend for matplotlib.

%package -n python2-matplotlib-gtk
Summary:       GDK and GTK backends for matplotlib
Group:         Development/Python
Requires:      python2-matplotlib = %{version}-%{release}
Requires:      pygtk2.0 >= 2.4.0
Requires:      python2-matplotlib-cairo = %{version}-%{release}

%description -n python2-matplotlib-gtk
This package contains the GDK and GTK backends for matplotlib.


%package -n python2-matplotlib-qt5
Summary:	Qt backend for matplotlib
Group:		Development/Python
Requires:	python2-matplotlib-qt5 = %{version}-%{release}
Requires:	python2-qt5

%description -n python2-matplotlib-qt5
This package contains the Qt5 backend for matplotlib.

%package -n python2-matplotlib-svg
Summary:	SVG backend for matplotlib
Group:		Development/Python
Requires:	python2-matplotlib = %{version}-%{release}

%description -n python2-matplotlib-svg
This package contains the SVG backend for matplotlib.

%package -n python2-matplotlib-tk
Summary:	Tk backend for matplotlib
Group:		Development/Python
Requires:	python2-matplotlib = %{version}-%{release}
Requires:	tkinter2

%description -n python2-matplotlib-tk
This package contains the Tk backend for matplotlib.
%endif

%prep
%setup -q -n %{module}-%{version}

# Copy setup.cfg to the builddir
cp %{SOURCE1} .
sed -i 's/\(backend = \).*/\1%{backend}/' setup.cfg

%if !%{with_bundled_fonts}
# Use fontconfig by default
sed -i 's/\(USE_FONTCONFIG = \)False/\1True/' lib/matplotlib/font_manager.py
%endif

# Remove bundled libraries
#rm -r extern/agg24-svn 

%apply_patches

chmod -x lib/matplotlib/mpl-data/images/*.svg

%if %{with python2}
mkdir PY2
cp -a `ls |grep -v PY2` PY2/
%endif

%build
PYTHONDONTWRITEBYTECODE=true \
MPLCONFIGDIR=$PWD \
MATPLOTLIBDATA=$PWD/lib/matplotlib/mpl-data \
    python setup.py build build_ext -ldl

%if %{with python2}
cd PY2
PYTHONDONTWRITEBYTECODE=true \
MPLCONFIGDIR=$PWD \
MATPLOTLIBDATA=$PWD/lib/matplotlib/mpl-data \
    python2 setup.py build build_ext -ldl
cd ..
%endif

%if %{with_html}
# Need to make built matplotlib libs available for the sphinx extensions:
pushd doc
    MPLCONFIGDIR=$PWD/.. \
    MATPLOTLIBDATA=$PWD/../lib/matplotlib/mpl-data \
    PYTHONPATH=`realpath ../build/lib.linux*` \
        %{__python} make.py html
popd
%endif
# Ensure all example files are non-executable so that the -doc
# package doesn't drag in dependencies
find examples -name '*.py' -exec chmod a-x '{}' \;

%install
PYTHONDONTWRITEBYTECODE=true \
MPLCONFIGDIR=$PWD \
MATPLOTLIBDATA=$PWD/lib/matplotlib/mpl-data/ \
    python setup.py install --skip-build --root=%{buildroot}

%if %{with python2}
cd PY2
PYTHONDONTWRITEBYTECODE=true \
MPLCONFIGDIR=$PWD \
MATPLOTLIBDATA=$PWD/lib/matplotlib/mpl-data/ \
    python2 setup.py install --skip-build --root=%{buildroot}
cd ..
%endif

chmod +x %{buildroot}%{python_sitearch}/matplotlib/dates.py
mkdir -p %{buildroot}%{_sysconfdir} %{buildroot}%{_datadir}/matplotlib
mv %{buildroot}%{python_sitearch}/matplotlib/mpl-data/matplotlibrc \
   %{buildroot}%{_sysconfdir}
mv %{buildroot}%{python_sitearch}/matplotlib/mpl-data \
   %{buildroot}%{_datadir}/matplotlib
%if !%{with_bundled_fonts}
rm -rf %{buildroot}%{_datadir}/matplotlib/mpl-data/fonts
%endif
rm -rf %{buildroot}%{python_sitearch}/__pycache__

%if %{run_tests}
%check
# This should match the default backend
echo "backend      : %{backend}" > matplotlibrc
MPLCONFIGDIR=$PWD \
MATPLOTLIBDATA=$RPM_BUILD_ROOT%{_datadir}/matplotlib/mpl-data \
PYTHONPATH=$RPM_BUILD_ROOT%{python_sitearch} \
     %{__python} -c "import matplotlib; matplotlib.test()"
%endif # run_tests

%files
%doc README.rst
%doc LICENSE/
%{python_sitearch}/*egg-info
%{python_sitearch}/matplotlib-*-nspkg.pth
%{python_sitearch}/%{module}/
%{python_sitearch}/mpl_toolkits/
%{python_sitearch}/pylab.py*
%{python_sitearch}/__pycache__/*
%exclude %{py_platsitedir}/%{module}/backends/backend_cairo.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_qt5.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_qt5agg.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_svg.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_tkagg.py*
%exclude %{py_platsitedir}/%{module}/backends/tkagg.py*
%exclude %{py_platsitedir}/%{module}/backends/_tkagg*.so

%files cairo
%{py_platsitedir}/%{module}/backends/backend_cairo.py*

%files qt5
%{py_platsitedir}/%{module}/backends/backend_qt5.py*
%{py_platsitedir}/%{module}/backends/backend_qt5agg.py*

%files svg
%{py_platsitedir}/%{module}/backends/backend_svg.py*

%files tk
%{py_platsitedir}/%{module}/backends/backend_tkagg.py*
%{py_platsitedir}/%{module}/backends/tkagg.py*
%{py_platsitedir}/%{module}/backends/_tkagg*.so

%files doc
%doc examples/
%if %{with_html}
%doc doc/build/html/*
%endif

%files data
%{_sysconfdir}/matplotlibrc
%{_datadir}/matplotlib/mpl-data/
%if %{with_bundled_fonts}
%exclude %{_datadir}/matplotlib/mpl-data/fonts/
%endif

%if %{with_bundled_fonts}
%files data-fonts
%{_datadir}/matplotlib/mpl-data/fonts/
%endif

%if %{with python2}
%files -n python2-matplotlib
%doc README.rst
%doc LICENSE/
%{python2_sitearch}/*egg-info
%{python2_sitearch}/matplotlib-*-nspkg.pth
%{python2_sitearch}/%{module}/
%{python2_sitearch}/mpl_toolkits/
%{python2_sitearch}/pylab.py*
%exclude %{py2_platsitedir}/%{module}/backends/backend_cairo.py*
%exclude %{py2_platsitedir}/%{module}/backends/backend_qt5.py*
%exclude %{py2_platsitedir}/%{module}/backends/backend_qt5agg.py*
%exclude %{py2_platsitedir}/%{module}/backends/backend_svg.py*
%exclude %{py2_platsitedir}/%{module}/backends/backend_tkagg.py*
%exclude %{py2_platsitedir}/%{module}/backends/tkagg.py*
%exclude %{py2_platsitedir}/%{module}/backends/_tkagg*.so

%files -n python2-matplotlib-cairo
%{py2_platsitedir}/%{module}/backends/backend_cairo.py*

%files -n python2-matplotlib-qt5
%{py2_platsitedir}/%{module}/backends/backend_qt5.py*
%{py2_platsitedir}/%{module}/backends/backend_qt5agg.py*

%files -n python2-matplotlib-svg
%{py2_platsitedir}/%{module}/backends/backend_svg.py*

%files -n python2-matplotlib-tk
%{py2_platsitedir}/%{module}/backends/backend_tkagg.py*
%{py2_platsitedir}/%{module}/backends/tkagg.py*
%{py2_platsitedir}/%{module}/backends/_tkagg*.so
%endif
