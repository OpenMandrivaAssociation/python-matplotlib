%define	module	matplotlib

Name:		python-%{module}
Version:	1.1.0
Release:	2
Summary:	Matlab-style 2D plotting package for Python
Group:		Development/Python
License:	Python license
URL:		http://matplotlib.sourceforge.net/
Source0:	http://downloads.sourceforge.net/project/%{module}/%{module}/%{module}-%{version}/%{module}-%{version}.tar.gz
%{py_requires -d}
Patch0:		setupext-tk-include-0.99.1.2.patch
Requires:	python-numpy >= 1.1.0
Requires:	python-configobj, python-dateutil, python-pytz
Requires:	python-matplotlib-gtk = %{version}-%{release}
BuildRequires:	python-setuptools
BuildRequires:	python-numpy-devel >= 1.1.0
BuildRequires:	libwxPythonGTK-devel, pygtk2.0-devel, cairo-devel
BuildRequires:	tkinter, tcl-devel, tk-devel, freetype2-devel >= 2.1.7
BuildRequires:	python-qt, python-qt4
BuildRequires:	pkgconfig(libpng)
BuildRequires:	zlib-devel
BuildRequires:	python-configobj, python-dateutil, python-pytz
BuildRequires:	python-docutils, python-sphinx
BuildRequires:	ipython

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
BuildArch:	noarch

%description doc
This package contains documentation and sample code for matplotlib.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p0 -b .setupext

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

%files -f FILELIST
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

%files qt
%{py_platsitedir}/%{module}/backends/backend_qt.py*
%{py_platsitedir}/%{module}/backends/backend_qtagg.py*

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
%doc examples/ CHANGELOG README.txt TODO doc/build/html/*


%changelog
* Tue Oct 11 2011 Lev Givon <lev@mandriva.org> 1.1.0-1mdv2012.0
+ Revision: 704336
- Update to 1.1.0.

  + Oden Eriksson <oeriksson@mandriva.com>
    - attempt to relink against libpng15.so.15

* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-2
+ Revision: 667986
- mass rebuild

* Fri Jan 07 2011 Lev Givon <lev@mandriva.org> 1.0.1-1mdv2011.0
+ Revision: 629185
- Update to 1.0.1.

* Thu Nov 04 2010 Paulo Andrade <pcpa@mandriva.com.br> 1.0.0-6mdv2011.0
+ Revision: 593527
+ rebuild (emptylog)

* Tue Nov 02 2010 Michael Scherer <misc@mandriva.org> 1.0.0-5mdv2011.0
+ Revision: 592431
- rebuild for python 2.7

  + Andrey Borzenkov <arvidjaar@mandriva.org>
    - rebuild for new python 2.7

  + Thierry Vignaud <tv@mandriva.org>
    - make doc subpackage noarch

* Tue Sep 07 2010 Lev Givon <lev@mandriva.org> 1.0.0-2mdv2011.0
+ Revision: 576692
- Bump release to force rebuild.

* Mon Jul 19 2010 Lev Givon <lev@mandriva.org> 1.0.0-1mdv2011.0
+ Revision: 555007
- Update to 1.0.0.

* Mon May 31 2010 Lev Givon <lev@mandriva.org> 0.99.3-1mdv2010.1
+ Revision: 546714
- Update to 0.99.3.

* Sun May 02 2010 Lev Givon <lev@mandriva.org> 0.99.1.2-4mdv2010.1
+ Revision: 541674
- Make main package require installation of gtk backend (#59044).

* Sat Apr 10 2010 Lev Givon <lev@mandriva.org> 0.99.1.2-3mdv2010.1
+ Revision: 533535
- Put docs in a separate package (#58679).

* Sun Jan 10 2010 Lev Givon <lev@mandriva.org> 0.99.1.2-2mdv2010.1
+ Revision: 488922
- Spin off backends with special installation dependencies
  to separate packages (#50278).

* Fri Dec 18 2009 Lev Givon <lev@mandriva.org> 0.99.1.2-1mdv2010.1
+ Revision: 479862
- Update to 0.99.1.2.

* Mon Oct 12 2009 Funda Wang <fwang@mandriva.org> 0.99.1-4mdv2010.0
+ Revision: 456749
- rebuild

* Wed Oct 07 2009 Lev Givon <lev@mandriva.org> 0.99.1-3mdv2010.0
+ Revision: 455814
- Require python-qt, python-qt4.
  Rebuild against new python-qt4.

* Wed Sep 23 2009 Lev Givon <lev@mandriva.org> 0.99.1-2mdv2010.0
+ Revision: 447968
- Use updated tarball that does not contain a spurious setup.cfg file.

* Wed Sep 23 2009 Lev Givon <lev@mandriva.org> 0.99.1-1mdv2010.0
+ Revision: 447593
- Update to 0.99.1.

* Mon Aug 10 2009 Lev Givon <lev@mandriva.org> 0.99.0-2mdv2010.0
+ Revision: 414467
- Build docs as html.

* Sat Aug 08 2009 Frederik Himpe <fhimpe@mandriva.org> 0.99.0-1mdv2010.0
+ Revision: 411742
- Update to new version 0.99.0
- Remove literal patch: not needed anymore

* Tue May 19 2009 Paulo Andrade <pcpa@mandriva.com.br> 0.98.5.3-2mdv2010.0
+ Revision: 377417
- Rebuild without dependency on python-enthought-traits.

* Mon Feb 09 2009 Lev Givon <lev@mandriva.org> 0.98.5.3-1mdv2009.1
+ Revision: 338955
- Update to 0.98.5.3.

* Wed Dec 31 2008 Adam Williamson <awilliamson@mandriva.org> 0.98.5.2-2mdv2009.1
+ Revision: 321619
- rebuild for python 2.6
- clean up python requires
- add literal.patch (fix a string literal error)

* Fri Dec 19 2008 Lev Givon <lev@mandriva.org> 0.98.5.2-1mdv2009.1
+ Revision: 316008
- Update to 0.98.5.2.

* Fri Dec 12 2008 Lev Givon <lev@mandriva.org> 0.98.5-1mdv2009.1
+ Revision: 313694
- Update to 0.98.5.

* Wed Dec 10 2008 Lev Givon <lev@mandriva.org> 0.98.4-1mdv2009.1
+ Revision: 312592
- Update to 0.98.4.

* Sat Dec 06 2008 Adam Williamson <awilliamson@mandriva.org> 0.98.3-3mdv2009.1
+ Revision: 311038
- rebuild for new tcl
- small cleanup

* Fri Oct 31 2008 Lev Givon <lev@mandriva.org> 0.98.3-2mdv2009.1
+ Revision: 298971
- Remove python-enthought-traits-ui dependency
  (no longer needed after upgrade to traits 3).

* Thu Aug 07 2008 Lev Givon <lev@mandriva.org> 0.98.3-1mdv2009.0
+ Revision: 266422
- Update to 0.98.3.
  Build user manual directly from source.

* Thu Jul 17 2008 Lev Givon <lev@mandriva.org> 0.98.2-3mdv2009.0
+ Revision: 237778
- Add traits dependencies.

* Fri Jul 11 2008 Lev Givon <lev@mandriva.org> 0.98.2-2mdv2009.0
+ Revision: 233825
- Add python-pytz and python-dateutil dependencies.
- Update to 0.98.2.
- Update to 0.98.1.

* Sun Jun 01 2008 Lev Givon <lev@mandriva.org> 0.98.0-1mdv2009.0
+ Revision: 214132
- Update to 0.98.0.

* Wed Mar 19 2008 Lev Givon <lev@mandriva.org> 0.91.2-2mdv2008.1
+ Revision: 188792
- Add python-config dependency (39041).

* Wed Jan 09 2008 Lev Givon <lev@mandriva.org> 0.91.2-1mdv2008.1
+ Revision: 147007
- Update to 0.91.2.

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Dec 06 2007 Lev Givon <lev@mandriva.org> 0.91.1-2mdv2008.1
+ Revision: 116031
- Replace my patch with the one from the matplotlib developers.

* Wed Dec 05 2007 Lev Givon <lev@mandriva.org> 0.91.1-1mdv2008.1
+ Revision: 115740
- Update to 0.91.1.
  Add patch to fix matplotlib bug 1845057.

* Wed Nov 21 2007 Lev Givon <lev@mandriva.org> 0.90.1-2mdv2008.1
+ Revision: 111043
- Clean up build requirements.

* Sun Jun 03 2007 Lev Givon <lev@mandriva.org> 0.90.1-1mdv2008.0
+ Revision: 34938
- Update to 0.90.1.
  Tweak build deps.

