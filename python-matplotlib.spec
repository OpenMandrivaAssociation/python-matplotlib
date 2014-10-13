%define	module			matplotlib

%global with_html		0
%global run_tests		0

# the default backend; one of GTK GTKAgg GTKCairo GTK3Agg GTK3Cairo
# CocoaAgg MacOSX Qt4Agg TkAgg Agg Cairo GDK PS PDF SVG
%global backend			TkAgg

# https://fedorahosted.org/fpc/ticket/381
%global with_bundled_fonts      1

Summary:	Python 2D plotting library
Name:		python-%{module}
Version:	1.4.0
Release:	1
Group:		Development/Python
License:	Python license
Url:		http://matplotlib.sourceforge.net/
#Modified Sources to remove the one undistributable file
#See generate-tarball.sh in fedora cvs repository for logic
#sha1sum matplotlib-1.2.0-without-gpc.tar.gz
#92ada4ef4e7374d67e46e30bfb08c3fed068d680  matplotlib-1.2.0-without-gpc.tar.gz
Source0:	matplotlib-%{version}-without-gpc.tar.xz
Source1:        setup.cfg
Patch0:		python-matplotlib-aggdir.patch
Patch1:		%{name}-system-cxx.patch
Patch2: 	20_matplotlibrc_path_search_fix.patch
Patch3: 	40_bts608939_draw_markers_description.patch
Patch6: 	70_bts720549_try_StayPuft_for_xkcd.patch

BuildRequires:	python-parsing
BuildRequires:	python-setuptools
BuildRequires:	ipython
BuildRequires:	python-configobj
BuildRequires:	python-cxx-devel
BuildRequires:	python-dateutil
BuildRequires:	python-pytz
BuildRequires:	python-qt4
BuildRequires:	qhull-devel
BuildRequires:	tkinter
BuildRequires:	x11-server-xvfb
BuildRequires:	python-numpy-devel >= 1.1.0
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(libagg)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(tcl)
BuildRequires:	pkgconfig(tk)
BuildRequires:	pkgconfig(zlib)
%if %{with_html}
BuildRequires:	graphviz
#BuildRequires:	texlive
BuildRequires:	python-docutils
BuildRequires:	python-sphinx
BuildRequires:	python-numpydoc
%endif
BuildRequires:	python-devel
Requires:	python-configobj
Requires:	python-dateutil
Requires:	python-numpy >= 1.1.0
Requires:	python-pytz
Requires:       %{name}-data = %{version}-%{release}

# GTKAgg does not require extra subpackages, but does not work with python3
%if "%{backend}" == "TkAgg"
Requires:	%{name}-tk%{?_isa} = %{version}-%{release}
%else
%  if "%{backend}" == "Qt4Agg"
Requires:	%{name}-qt4%{?_isa} = %{version}-%{release}
%  endif
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

# Copy setup.cfg to the builddir
cp %{SOURCE1} .
sed -i 's/\(backend = \).*/\1%{backend}/' setup.cfg

%if !%{with_bundled_fonts}
# Use fontconfig by default
sed -i 's/\(USE_FONTCONFIG = \)False/\1True/' lib/matplotlib/font_manager.py
%endif

# Remove bundled libraries
rm -r extern/agg24 extern/CXX

%apply_patches

chmod -x lib/matplotlib/mpl-data/images/*.svg

%build
PYTHONDONTWRITEBYTECODE= \
MPLCONFIGDIR=$PWD \
MATPLOTLIBDATA=$PWD/lib/matplotlib/mpl-data \
    xvfb-run %{__python} setup.py build

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
PYTHONDONTWRITEBYTECODE= \
MPLCONFIGDIR=$PWD \
MATPLOTLIBDATA=$PWD/lib/matplotlib/mpl-data/ \
    %{__python} setup.py install --skip-build --root=%{buildroot}
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
     xvfb-run %{__python} -c "import matplotlib; matplotlib.test()"

%if %{with_python3}
MPLCONFIGDIR=$PWD \
MATPLOTLIBDATA=$RPM_BUILD_ROOT%{_datadir}/matplotlib/mpl-data \
PYTHONPATH=$RPM_BUILD_ROOT%{python3_sitearch} \
     xvfb-run %{__python3} -c "import matplotlib; matplotlib.test()"
%endif
%endif # run_tests

%files
%doc README.rst
%doc LICENSE/
%doc CHANGELOG
%doc INSTALL
%doc PKG-INFO
%{python_sitearch}/*egg-info
%{python_sitearch}/matplotlib-*-nspkg.pth
%{python_sitearch}/%{module}/
%{python_sitearch}/mpl_toolkits/
%{python_sitearch}/pylab.py*
%{python_sitearch}/freetype2.*.so
%exclude %{py_platsitedir}/%{module}/backends/backend_cairo.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_qt4.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_qt4agg.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_svg.py*
%exclude %{py_platsitedir}/%{module}/backends/backend_tkagg.py*
%exclude %{py_platsitedir}/%{module}/backends/tkagg.py*
%exclude %{py_platsitedir}/%{module}/backends/_tkagg*.so

%files cairo
%{py_platsitedir}/%{module}/backends/backend_cairo.py*

%files qt4
%{py_platsitedir}/%{module}/backends/backend_qt4.py*
%{py_platsitedir}/%{module}/backends/backend_qt4agg.py*

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
