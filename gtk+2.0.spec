# enable_gtkdoc: Toggle if gtk-doc files should be rebuilt.
#      0 = no
#      1 = yes
%define enable_gtkdoc 1

# enable_bootstrap: Toggle if bootstrapping package
#      0 = no
#      1 = yes
%define enable_bootstrap 0

# enable_tests: Run test suite in build
#      0 = no
#      1 = yes
%define enable_tests 0

%{?_without_gtkdoc: %{expand: %%define enable_gtkdoc 0}}
%{?_without_bootstrap: %{expand: %%define enable_bootstrap 0}}
%{?_without_tests: %{expand: %%define enable_tests 0}}

%{?_with_gtkdoc: %{expand: %%define enable_gtkdoc 1}}
%{?_with_bootstrap: %{expand: %%define enable_bootstrap 1}}
%{?_with_tests: %{expand: %%define enable_tests 1}}


# required version of various libraries
%define req_glib_version		2.25.10
%define req_pango_version		1.20.0
%define req_atk_version			1.29.2
%define req_cairo_version		1.6.0
%define req_gdk_pixbuf_version		2.21.0

%define pkgname			gtk+
%define api_version		2.0
%define binary_version	2.10
%define lib_major		0
%define libname			%mklibname %{pkgname} %{api_version} %{lib_major}
%define libname_x11		%mklibname %{pkgname}-x11- %{api_version} %{lib_major}
%define develname		%mklibname -d %pkgname %api_version

%define gail_major 18
%define gail_libname %mklibname gail %gail_major
%define gaildevelname %mklibname -d gail

Summary:	The GIMP ToolKit (GTK+), a library for creating GUIs
Name:		%{pkgname}%{api_version}
Version:	2.22.1
Release:        %mkrel 3
License:	LGPLv2+
Group:		System/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%pkgname/%{pkgname}-%{version}.tar.bz2
# extra IM modules (vietnamese and tamil) -- pablo
#gw TODO, needs to be fixed for 2.21.3
Patch4:		gtk+-2.13.1-extra_im.patch 
# (fc) 2.0.6-8mdk fix infinite loop and crash in file selector when / and $HOME are not readable (bug #90)
Patch5:		gtk+-2.6.9-fileselectorfallback.patch
# (fwang) 2.22.1-3 use Qtcurve theme by default if available
Patch12:	gtk+-defaulttheme.patch
# (gb) 2.4.4-2mdk handle biarch
Patch13:	gtk+-2.2.4-lib64.patch
# (fc) 2.18.2-2mdv fix nautilus crash (GNOME bug #596977) (pterjan)
Patch15:	gtk+-2.18.1-fixnautiluscrash.patch
# (fc) 2.20.0-2mdv improve tooltip appareance (GNOME bug #599617) (Fedora)
Patch18:	gtk+-2.21.1-fresh-tooltips.patch
# (fc) 2.20.0-2mdv improve tooltip positioning (GNOME bug #599618) (Fedora)
Patch19:	gtk+-2.20.0-tooltip-positioning.patch
# (fc) 2.20.0-2mdv allow window dragging toolbars / menubar (GNOME bug #611313)
Patch20:	gtk+-2.20.0-window-dragging.patch
# (fc) 2.20.0-3mdv allow specifying icon padding for tray icon (GNOME bug #583273) (Fedora)
Patch21:	gtk+-2.20.0-icon-padding.patch

Conflicts:	perl-Gtk2 < 1.113

BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

URL:		http://www.gtk.org
Requires:	common-licenses
BuildRequires:	gettext-devel
BuildRequires:  libglib2-devel >= %{req_glib_version}
BuildRequires:	libatk1.0-devel >= %{req_atk_version}
BuildRequires:  cairo-devel >= %{req_cairo_version}
BuildRequires:	pango-devel >= %{req_pango_version}
BuildRequires:  gobject-introspection-devel >= 0.9.5
BuildRequires:	libgdk_pixbuf2.0-devel >= %req_gdk_pixbuf_version
BuildRequires:  libx11-devel
BuildRequires:	libxext-devel
BuildRequires:	libxrender-devel
BuildRequires:	libxcomposite-devel
BuildRequires:	libxcursor-devel
BuildRequires:	libxdamage-devel
BuildRequires:	libxfixes-devel
BuildRequires:	libxi-devel
BuildRequires:	libxinerama-devel
BuildRequires:	libxrandr-devel
BuildRequires:  cups-devel
BuildRequires:  fam-devel
%if %enable_tests
%if %mdkversion <= 200600
BuildRequires:	XFree86-Xvfb
%else
BuildRequires:  x11-server-xvfb
%endif
%endif
%if %enable_gtkdoc
BuildRequires: gtk-doc >= 0.9 
BuildRequires: sgml-tools
BuildRequires: texinfo
%endif
# gw tests will fail without this
BuildRequires: fonts-ttf-dejavu
%if !%{enable_bootstrap}
Suggests: xdg-user-dirs-gtk
Suggests: qtcurve-gtk2
%endif
Requires: %{libname} = %{version}
Provides:	%{pkgname}2 = %{version}-%{release}
Obsoletes:	%{pkgname}2
Provides:	gail = %version-%release
Obsoletes:	gail

%description
The gtk+ package contains the GIMP ToolKit (GTK+), a library for creating
graphical user interfaces for the X Window System.  GTK+ was originally
written for the GIMP (GNU Image Manipulation Program) image processing
program, but is now used by several other programs as well.  

If you are planning on using the GIMP or another program that uses GTK+,
you'll need to have the gtk+ package installed.

%package -n %{libname}
Summary: %{summary}
Group:	 %{group}
Obsoletes:	lib%{pkgname}2
Provides:	lib%{pkgname}2 = %{version}-%{release}
Provides:	lib%{name} = %{version}-%{release}
Provides:   gtk2 = %{version}-%{release}
Requires:   libglib2.0 >= %{req_glib_version}
Requires:   libpango1.0 >= %{req_pango_version}
Conflicts:  libgnomeui2_0 <= 2.0.5
Conflicts:  gtk-engines2 <= 2.2.0-7mdk
Conflicts:  %{libname_x11} < 2.10.3-2mdv2007.0
Requires(post): 	%{libname_x11} = %{version}
%if !%{enable_bootstrap}
Suggests: %{_lib}qtcurve-gtk2
%endif

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with gtk+.

%package -n %{develname}
Summary:	Development files for GTK+ (GIMP ToolKit) applications
Group:		Development/GNOME and GTK+
Obsoletes:  %{libname_x11}-devel
Provides:   %{libname_x11}-devel = %{version}-%{release}
Provides:   gtk2-devel = %{version}-%{release}
Obsoletes:	%{pkgname}2-devel
Obsoletes:  lib%{pkgname}2-devel
Obsoletes:  %mklibname -d %{pkgname} 2.0 0
Provides:	%{pkgname}2-devel = %{version}-%{release}
Provides:	lib%{pkgname}2-devel = %{version}-%{release}
Provides:	lib%{pkgname}%{api_version}-devel = %{version}-%{release}
Provides:	%{libname}-devel = %{version}-%{release}
Provides:	lib%{pkgname}-x11-%{api_version}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}
Requires:	%{libname_x11} = %{version}
Requires:	libgdk_pixbuf2.0-devel >= %req_gdk_pixbuf_version
Requires:	libatk1.0-devel >= %{req_atk_version}
Requires:	libpango1.0-devel >= %{req_pango_version}


%description -n %{develname}
The libgtk+-devel package contains the static libraries and header files
needed for developing GTK+ (GIMP ToolKit) applications. The libgtk+-devel
package contains GDK (the General Drawing Kit, which simplifies the interface
for writing GTK+ widgets and using GTK+ widgets in applications), and GTK+
(the widget set).


%package -n %{libname_x11}
Summary:	X11 backend of The GIMP ToolKit (GTK+)
Group:		System/Libraries
Provides:	lib%{pkgname}-x11-%{api_version} = %{version}-%{release}
Provides:	%{name}-backend = %{version}-%{release}
Requires: 	%{libname} = %{version}
Requires:	libatk1.0 >= %{req_atk_version}
Requires:	%{name} >= %{version}-%{release}
Conflicts:  libgtk+2-devel < 2.0.0
Conflicts: gir-repository < 0.6.5-4

%description -n %{libname_x11}
This package contains the X11 version of library needed to run
programs dynamically linked with gtk+.

%package -n %{gail_libname}
Summary:	GNOME Accessibility Implementation Library
Group:		System/Libraries
Provides:	libgail = %{version}-%{release}
Conflicts:	gail < 1.9.4-2mdv

%description -n %{gail_libname}
Gail is the GNOME Accessibility Implementation Library

%package -n %gaildevelname
Summary:	Static libraries, include files for GAIL
Group:		Development/GNOME and GTK+
Provides:	gail-devel = %{version}-%{release}
Provides:	libgail-devel = %{version}-%{release}
Requires:	%{gail_libname} = %{version}
Conflicts:	%{_lib}gail17-devel
Obsoletes: %mklibname -d gail 18

%description -n %gaildevelname
Gail is the GNOME Accessibility Implementation Library

%prep
%setup -n %{pkgname}-%{version} -q
%patch4 -p1 -b .extra_im
%patch5 -p1 -b .fileselectorfallback
%patch12 -p1 -b .defaulttheme
#gw disabled for bootstrapping
%patch13 -p1 -b .lib64
#patch15 -p1 -b .fixnautiluscrash
%patch18 -p1 -b .fresh-tooltips
#%patch19 -p1 -b .tooltip-positioning
%patch20 -p1 -b .window-dragging
%patch21 -p1 -b .icon-padding

#needed by patches 4 & 13
#gw disabled for bootstrapping
autoreconf -fi

%build
%ifarch ppc64
export CFLAGS="$RPM_OPT_FLAGS -mminimal-toc"
%endif

# Build X11 backend
#[ -d X11-build ] || mkdir X11-build
#cd X11-build

# fix crash in nautilus (GNOME bug #596977)
export CFLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/-fomit-frame-pointer//g'`

#CONFIGURE_TOP=.. 
export CPPFLAGS="-DGTK_COMPILATION"
#	--with-included-immodules=yes \
%configure2_5x --enable-xinerama \
	--with-xinput=xfree \
%if !%enable_gtkdoc
	--enable-gtk-doc=no
%endif

%make

%check
%if %enable_tests
#cd X11-build
XDISPLAY=$(i=1; while [ -f /tmp/.X$i-lock ]; do i=$(($i+1)); done; echo $i)
%if %mdkversion <= 200600
%{_prefix}/X11R6/bin/Xvfb :$XDISPLAY &
%else
%{_bindir}/Xvfb :$XDISPLAY &
%endif
export DISPLAY=:$XDISPLAY
make check
kill $(cat /tmp/.X$XDISPLAY-lock) ||:
#cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

#cd X11-build
%makeinstall_std mandir=%{_mandir} RUN_QUERY_IMMODULES_TEST=false RUN_QUERY_LOADER_TEST=false


#cd ..

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gtk-%{api_version}
touch $RPM_BUILD_ROOT%{_sysconfdir}/gtk-%{api_version}/gtk.immodules.%{_lib}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/gtk-%{api_version}/modules

# handle biarch packages
progs="gtk-query-immodules-%{api_version}"
mkdir -p $RPM_BUILD_ROOT%{_libdir}/gtk-%{api_version}/bin
for f in $progs; do
  mv -f $RPM_BUILD_ROOT%{_bindir}/$f $RPM_BUILD_ROOT%{_libdir}/gtk-%{api_version}/bin/
  cat > $RPM_BUILD_ROOT%{_bindir}/$f << EOF
#!/bin/sh
lib=%{_lib}
case ":\$1:" in
:lib*:) lib="\$1"; shift 1;;
esac
exec %{_prefix}/\$lib/gtk-%{api_version}/bin/$f \${1+"\$@"}
EOF
  chmod +x $RPM_BUILD_ROOT%{_bindir}/$f
done

%{find_lang} gtk20
%find_lang gtk20-properties
cat gtk20-properties.lang >> gtk20.lang

#remove not packaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/gtk-%{api_version}/%{binary_version}.*/immodules/*.la \
  $RPM_BUILD_ROOT%{_libdir}/gtk-%{api_version}/%{binary_version}.*/loaders/*.la \
  $RPM_BUILD_ROOT%{_libdir}/gtk-%{api_version}/%{binary_version}.*/engines/*.la \
  $RPM_BUILD_ROOT%{_libdir}/gtk-%{api_version}/%{binary_version}.*/printbackends/*.la \
  $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/modules/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -n %{libname_x11} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname_x11} -p /sbin/ldconfig
%endif

%post -n %{libname}
if [ "$1" = "2" ]; then
  if [ -f %{_sysconfdir}/gtk-%{api_version}/gtk.immodules ]; then
    rm -f %{_sysconfdir}/gtk-%{api_version}/gtk.immodules
  fi
fi

%{_libdir}/gtk-%{api_version}/bin/gtk-query-immodules-%{api_version} > %{_sysconfdir}/gtk-%{api_version}/gtk.immodules.%{_lib}

%post 
if [ -d %{_datadir}/icons ]; then
 for i in `/bin/ls %{_datadir}/icons` ; do 
  [ -d "%{_datadir}/icons/$i" -a -e "%{_datadir}/icons/$i/icon-theme.cache" -a -e "%{_datadir}/icons/$i/index.theme" ] && gtk-update-icon-cache --force --quiet %{_datadir}/icons/$i
 done
 exit 0
fi

%files -f gtk20.lang
%defattr(-, root, root)
%doc README
%{_bindir}/gtk-query-immodules-%{api_version}
%{_bindir}/gtk-update-icon-cache
%{_datadir}/themes
%dir %{_sysconfdir}/gtk-%{api_version}
%config(noreplace) %{_sysconfdir}/gtk-%{api_version}/im-multipress.conf

%files -n %{libname}
%defattr(-, root, root)
%doc README
%ghost %verify (not md5 mtime size) %config(noreplace) %{_sysconfdir}/gtk-%{api_version}/gtk.immodules.%{_lib}
%dir %{_libdir}/gtk-%{api_version}
%dir %{_libdir}/gtk-%{api_version}/bin
%{_libdir}/gtk-%{api_version}/bin/gtk-query-immodules-%{api_version}
%dir %{_libdir}/gtk-%{api_version}/modules
%dir %{_libdir}/gtk-%{api_version}/%{binary_version}.*
%dir %{_libdir}/gtk-%{api_version}/%{binary_version}.*/immodules
%{_libdir}/gtk-%{api_version}/%{binary_version}.*/immodules/im-am-et.so
%{_libdir}/gtk-%{api_version}/%{binary_version}.*/immodules/im-cedilla.so
%{_libdir}/gtk-%{api_version}/%{binary_version}.*/immodules/im-cyrillic-translit.so
%{_libdir}/gtk-%{api_version}/%{binary_version}.*/immodules/im-inuktitut.so
%{_libdir}/gtk-%{api_version}/%{binary_version}.*/immodules/im-ipa.so
%{_libdir}/gtk-%{api_version}/%{binary_version}.*/immodules/im-multipress.so
%{_libdir}/gtk-%{api_version}/%{binary_version}.*/immodules/im-thai.so
%{_libdir}/gtk-%{api_version}/%{binary_version}.*/immodules/im-ti-er.so
%{_libdir}/gtk-%{api_version}/%{binary_version}.*/immodules/im-ti-et.so
%{_libdir}/gtk-%{api_version}/%{binary_version}.*/immodules/im-viqr.so
%{_libdir}/gtk-%{api_version}/%{binary_version}.*/immodules/im-xim.so
%{_libdir}/gtk-%{api_version}/%{binary_version}.*/immodules/im-tamilvp-tsc.so
%{_libdir}/gtk-%{api_version}/%{binary_version}.*/immodules/im-tamilvp-uni.so
%{_libdir}/gtk-%{api_version}/%{binary_version}.*/immodules/im-telex.so
%{_libdir}/gtk-%{api_version}/%{binary_version}.*/immodules/im-vni.so
%dir %{_libdir}/gtk-%{api_version}/%{binary_version}.*/engines
%{_libdir}/gtk-%{api_version}/%{binary_version}.*/engines/*.so
%{_libdir}/gtk-%{api_version}/%{binary_version}.*/printbackends/*.so

%files -n %develname
%defattr(-, root, root)
%doc docs/*.txt AUTHORS ChangeLog NEWS* README*
%doc %{_datadir}/gtk-doc/html/gdk
%doc %{_datadir}/gtk-doc/html/gtk
%{_bindir}/gtk-demo
%_bindir/gtk-builder-convert
%{_datadir}/aclocal/*
%{_datadir}/gtk-%{api_version}
%{_includedir}/gtk-unix-print-%{api_version}/
%{_includedir}/gtk-%{api_version}/gdk
%{_includedir}/gtk-%{api_version}/gtk
%{_libdir}/gtk-%{api_version}/include
%{_libdir}/pkgconfig/gdk-%{api_version}.pc
%{_libdir}/pkgconfig/gtk+-%{api_version}.pc
%{_libdir}/pkgconfig/gtk+-unix-print-%{api_version}.pc
%{_libdir}/*x11*.so
%_datadir/gir-1.0/Gdk-2.0.gir
%_datadir/gir-1.0/GdkX11-2.0.gir
%_datadir/gir-1.0/Gtk-2.0.gir
%attr(644,root,root) %{_libdir}/*x11*.la
%{_libdir}/pkgconfig/*x11*

%files -n %{libname_x11}
%defattr(-, root, root)
%{_libdir}/*x11*.so.*
%_libdir/girepository-1.0/Gdk-2.0.typelib
%_libdir/girepository-1.0/GdkX11-2.0.typelib
%_libdir/girepository-1.0/Gtk-2.0.typelib

%files -n %gail_libname
%defattr(-,root,root)
%{_libdir}/libgailutil.so.%{gail_major}*
%{_libdir}/gtk-2.0/modules/libferret.so
%{_libdir}/gtk-2.0/modules/libgail.so

%files -n %gaildevelname
%defattr(-,root,root)
%{_datadir}/gtk-doc/html/gail-libgail-util
%{_libdir}/libgailutil.so
%attr(644,root,root) %{_libdir}/libgailutil.la
%{_includedir}/gail-1.0
%{_libdir}/pkgconfig/gail.pc
