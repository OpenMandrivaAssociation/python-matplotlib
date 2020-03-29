%define module matplotlib

%global with_html 0
%global run_tests 0

# the default backend; one of GTK GTKAgg GTKCairo GTK3Agg GTK3Cairo
# CocoaAgg MacOSX Qt4Agg Qt5Agg TkAgg Agg Cairo GDK PS PDF SVG
%global backend Qt5Agg

# https://fedorahosted.org/fpc/ticket/381
%global with_bundled_fonts 1

Summary:	Python 2D plotting library
Name:		python-%{module}
Version:	3.2.1
Release:	1
Group:		Development/Python
License:	Python license
Url:		http://matplotlib.sourceforge.net/
Source0:	https://github.com/matplotlib/matplotlib/archive/v%{version}.tar.gz
Source1:	setup.cfg
# Because the qhull package stopped shipping pkgconfig files.
# https://src.fedoraproject.org/rpms/qhull/pull-request/1
Patch0001:      0001-Force-using-system-qhull.patch


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
Requires:	python3-numpy >= 1.1.0
Requires:	python-pytz
Requires:	python-matplotlib-data = %{version}-%{release}
Requires:	%{name}-data = %{version}-%{release}

%if "%{backend}" == "TkAgg"
Suggests:	%{name}-tk%{?_isa} = %{version}-%{release}
%else
%if "%{backend}" == "Qt5Agg" || "%{backend}" == "Qt5Cairo"
Suggests:	%{name}-qt5%{?_isa} = %{version}-%{release}
%else
%if "%{backend}" == "GTKAgg" || "%{backend}" == "GTKCairo"
Suggests:	%{name}-gtk%{?_isa} = %{version}-%{release}
%endif
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
# absolutely broken
#Requires:      pygtk2.0 >= 2.4.0
Requires:      %{name}-cairo = %{version}-%{release}

%description gtk
This package contains the GDK and GTK backends for matplotlib.

%package wx
Summary:       WxWidgets backend for matplotlib
Group:         Development/Python
Requires:      %{name} = %{version}-%{release}

%description wx
This package contains the WxWidgets backend for matplotlib.

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

%prep
%setup -q -n %{module}-%{version}
%autopatch -p1

# Copy setup.cfg to the builddir
cp %{SOURCE1} .
sed -i 's/\(backend = \).*/\1%{backend}/' setup.cfg

%if !%{with_bundled_fonts}
# Use fontconfig by default
sed -i 's/\(USE_FONTCONFIG = \)False/\1True/' lib/matplotlib/font_manager.py
%endif

# Remove bundled libraries
#rm -r extern/agg24-svn 
rm -r extern/libqhull


chmod -x lib/matplotlib/mpl-data/images/*.svg

%build
PYTHONDONTWRITEBYTECODE=true \
MPLCONFIGDIR=$PWD \
MATPLOTLIBDATA=$PWD/lib/matplotlib/mpl-data \
    python setup.py build build_ext -ldl

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

# No point in supporting prehistoric libraries
rm -rf %{buildroot}%{py_platsitedir}/%{module}/backends/backend_qt4*.py*
# Or Nazism
rm -rf %{buildroot}%{py_platsitedir}/%{module}/backends/backend_macos*.py*

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
%exclude %{py_platsitedir}/%{module}/backends/backend_gtk3.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_gtk3agg.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_gtk3cairo.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_qt5.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_qt5agg.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_qt5cairo.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_svg.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_tkagg.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_wx.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_wxagg.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_wxcairo.py*
%exclude %{py_platsitedir}/%{module}/backends/_tkagg*.so

%files cairo
%{py_platsitedir}/%{module}/backends/backend_cairo.py*
%{py_platsitedir}/%{module}/backends/backend_qt5cairo.py*

%files gtk
%{py_platsitedir}/%{module}/backends/backend_gtk3.py*
%{py_platsitedir}/%{module}/backends/backend_gtk3agg.py*
%{py_platsitedir}/%{module}/backends/backend_gtk3cairo.py*

%files wx
%{py_platsitedir}/%{module}/backends/backend_wx.py*
%{py_platsitedir}/%{module}/backends/backend_wxagg.py*
%{py_platsitedir}/%{module}/backends/backend_wxcairo.py*

%files qt5
%{py_platsitedir}/%{module}/backends/backend_qt5.py*
%{py_platsitedir}/%{module}/backends/backend_qt5agg.py*

%files svg
%{py_platsitedir}/%{module}/backends/backend_svg.py*

%files tk
%{py_platsitedir}/%{module}/backends/backend_tkagg.py*
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
