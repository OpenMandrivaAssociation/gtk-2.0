%define url_ver %(echo %{version}|cut -d. -f1,2)
%define enable_gtkdoc 0
%define enable_bootstrap 0
%define enable_tests 0

%define pkgname gtk+
%define binary_version 2.10.0
%define api	2.0
%define major	0
# this isnt really a true lib pkg, but a modules/plugin pkg
%define modules %mklibname gtk-modules %{api}
%define libgdk	%mklibname gdk-x11_ %{api} %{major}
%define libgtk	%mklibname gtk-x11_ %{api} %{major}
%define girgdk	%mklibname gdk-gir %{api}
%define girgdkx11 %mklibname gdkx11-gir %{api}
%define girname %mklibname gtk-gir %{api}
%define devname	%mklibname -d %{pkgname} %{api}

%define gail_major 18
%define libgail %mklibname gail %{gail_major}
%define devgail %mklibname -d gail
%ifarch %{riscv}
%define _disable_lto %nil
%endif

Summary:	The GIMP ToolKit (GTK+), a library for creating GUIs
Name:		%{pkgname}%{api}
Version:	2.24.32
Release:	3
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.gtk.org
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gtk+/%{url_ver}/%{pkgname}-%{version}.tar.xz
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
#Patch15:	gtk+-2.18.1-fixnautiluscrash.patch
# (fc) 2.20.0-2mdv improve tooltip positioning (GNOME bug #599618) (Fedora)
#Patch19:	gtk+-2.20.0-tooltip-positioning.patch
# (fc) 2.20.0-2mdv allow window dragging toolbars / menubar (GNOME bug #611313)
Patch20:	gtk+-2.24.7-window-dragging.patch
# (fc) 2.20.0-3mdv allow specifying icon padding for tray icon (GNOME bug #583273) (Fedora)
Patch21:	gtk+-2.20.0-icon-padding.patch

BuildRequires:	cups-devel
BuildRequires:	pkgconfig(krb5)
BuildRequires:	pkgconfig(com_err)
BuildRequires:	fam-devel
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(atk) >= 1.29.2
BuildRequires:	pkgconfig(cairo) >= 1.12.0
BuildRequires:	pkgconfig(gdk-pixbuf-2.0) >= 2.21.0
BuildRequires:	pkgconfig(glib-2.0) >= 2.25.10
BuildRequires:	pkgconfig(gobject-introspection-1.0) >= 0.9.5
BuildRequires:	pkgconfig(pango) >= 1.20.0
BuildRequires:	pkgconfig(pangocairo) >= 1.20.0
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xdamage)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xrender)
%if %{enable_tests}
BuildRequires:	x11-server-xvfb
# gw tests will fail without this
BuildRequires:	fonts-ttf-dejavu
%endif
%if %{enable_gtkdoc}
BuildRequires:	gtk-doc >= 0.9
BuildRequires:	sgml-tools
BuildRequires:	texlive-texinfo
%endif

Requires:	%{name}-common = %{version}-%{release}
# MD to pull in all the orphaned module loaders
Requires:	fontconfig
Requires:	gdk-pixbuf2.0
Requires:	gio2.0
Requires:	pango-modules
%if !%{enable_bootstrap}
Suggests:	xdg-user-dirs-gtk
Suggests:	breeze-gtk
Suggests:	gtk2-modules
%endif
Provides:	gtk2 = %{version}-%{release}
Provides:	%{pkgname}2 = %{version}-%{release}
#(proyvind): to ensure we have g_malloc0_n & g_malloc_n (required by trigger)
#            provided by the ABI
Conflicts:	glib2 < 2.24

%description
The gtk+ package contains the GIMP ToolKit (GTK+), a library for creating
graphical user interfaces for the X Window System.  GTK+ was originally
written for the GIMP (GNU Image Manipulation Program) image processing
program, but is now used by several other programs as well.

If you are planning on using the GIMP or another program that uses GTK+,
you'll need to have the gtk+ package installed.

%package common
Summary:	%{summary}
Group:		%{group}
BuildArch:	noarch
Conflicts:	%{name} <= 2.24.8-2

%description common
This package contains the common files for the GTK+2.0 graphical user
interface.

%package -n %{modules}
Summary:	%{summary}
Group:		%{group}
Requires:	%{name} = %{version}-%{release}
Provides:	gtk2-modules = %{version}-%{release}
Conflicts:	%{_lib}gtk+2.0_0 < 2.24.8-4
Conflicts:	%{_lib}gtk+2.0 < 2.24.8-7
#(proyvind): to ensure we have g_malloc0_n & g_malloc_n (required by trigger)
#            provided by the ABI
Conflicts:	glib2 < 2.24
Conflicts:	%{_lib}gail18 < 2.24.8-3
%if !%{enable_bootstrap}
Suggests:	%{_lib}gtk-aurora-engine
%endif

%description -n %{modules}
This package contains the immodules, engines and printbackends libraries
for %{name} to function properly.

%package -n %{libgdk}
Summary:	X11 backend of The GIMP ToolKit (GTK+)
Group:		System/Libraries
Obsoletes:	%{_lib}%{pkgname}-x11-%{api}_%{major} < 2.24.17-2
Obsoletes:	%{_lib}gtk+%{api}_%{major} < 2.24.17-2

%description -n %{libgdk}
This package contains a shared library for %{name}.

%package -n %{libgtk}
Summary:	X11 backend of The GIMP ToolKit (GTK+)
Group:		System/Libraries
Obsoletes:	%{_lib}%{pkgname}-x11-%{api}_%{major} < 2.24.17-2
Obsoletes:	%{_lib}gtk+%{api}_%{major} < 2.24.17-2

%description -n %{libgtk}
This package contains a shared library for %{name}.

%package -n %{girgdk}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}gtk+-x11-2.0_0 < 2.24.8-3
Conflicts:	%{_lib}gtk+-gir2.0 < 2.24.17-2

%description -n %{girgdk}
GObject Introspection interface description for %{name}.

%package -n %{girgdkx11}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}gtk+-x11-2.0_0 < 2.24.8-3
Conflicts:	%{_lib}gtk+-gir2.0 < 2.24.17-2

%description -n %{girgdkx11}
GObject Introspection interface description for %{name}.

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}gtk+-x11-2.0_0 < 2.24.8-3
Conflicts:	%{_lib}gtk+-gir2.0 < 2.24.17-2

%description -n %{girname}
GObject Introspection interface description for %{name}.

%package -n %{devname}
Summary:	Development files for GTK+ (GIMP ToolKit) applications
Group:		Development/GNOME and GTK+
Requires:	%{libgdk} = %{version}-%{release}
Requires:	%{libgtk} = %{version}-%{release}
Requires:	%{girgdk} = %{version}-%{release}
Requires:	%{girgdkx11} = %{version}-%{release}
Requires:	%{girname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains the development files for %{name}.

%package -n %{libgail}
Summary:	GNOME Accessibility Implementation Library
Group:		System/Libraries

%description -n %{libgail}
Gail is the GNOME Accessibility Implementation Library

%package -n %{devgail}
Summary:	Development libraries, include files for GAIL
Group:		Development/GNOME and GTK+
Provides:	gail-devel = %{version}-%{release}
Requires:	%{libgail} = %{version}-%{release}

%description -n %{devgail}
Gail is the GNOME Accessibility Implementation Library

%prep
%setup -qn %{pkgname}-%{version}
%autopatch -p1

#needed by patches 4 & 13
#gw disable it for bootstrapping
mkdir -p m4
sed -i 's/HAVE_GTK_DOC/ENABLE_GTK_DOC/' gtk-doc.make
autoreconf -fi

%build
# fix crash in nautilus (GNOME bug #596977)
export CFLAGS=`echo %{optflags} | sed -e 's/-fomit-frame-pointer//g'`

#CONFIGURE_TOP=..
export CPPFLAGS="-DGTK_COMPILATION"
%configure \
	--disable-static \
	--enable-xinerama \
	--enable-xkb \
	--enable-shm \
%if %{enable_gtkdoc}
	--enable-gtk-doc=yes \
%endif
	--with-xinput=yes

# fight unused direct deps
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0/g' libtool

%make

%check
%if %{enable_tests}
XDISPLAY=$(i=1; while [ -f /tmp/.X$i-lock ]; do i=$(($i+1)); done; echo $i)
%{_bindir}/Xvfb :$XDISPLAY &
export DISPLAY=:$XDISPLAY
make check
kill $(cat /tmp/.X$XDISPLAY-lock) ||:
%endif

%install
%makeinstall_std mandir=%{_mandir} RUN_QUERY_IMMODULES_TEST=false RUN_QUERY_LOADER_TEST=false

mkdir -p %{buildroot}%{_sysconfdir}/gtk-%{api}
touch %{buildroot}%{_sysconfdir}/gtk-%{api}/gtk.immodules.%{_lib}
mkdir -p %{buildroot}%{_libdir}/gtk-%{api}/modules

# handle biarch packages
progs="gtk-query-immodules-%{api}"
mkdir -p %{buildroot}%{_libdir}/gtk-%{api}/bin
for f in $progs; do
  mv -f %{buildroot}%{_bindir}/$f %{buildroot}%{_libdir}/gtk-%{api}/bin/
  cat > %{buildroot}%{_bindir}/$f << EOF
#!/bin/sh
lib=%{_lib}
case ":\$1:" in
:lib*:) lib="\$1"; shift 1;;
esac
exec %{_prefix}/\$lib/gtk-%{api}/bin/$f \${1+"\$@"}
EOF
  chmod +x %{buildroot}%{_bindir}/$f
done

%find_lang gtk20
%find_lang gtk20-properties
cat gtk20-properties.lang >> gtk20.lang

%post -n %{modules}
if [ "$1" = "2" ]; then
    if [ -f %{_sysconfdir}/gtk-%{api}/gtk.immodules ]; then
	rm -f %{_sysconfdir}/gtk-%{api}/gtk.immodules
    fi
fi
%{_libdir}/gtk-%{api}/bin/gtk-query-immodules-%{api} > %{_sysconfdir}/gtk-%{api}/gtk.immodules.%{_lib}

%triggerin -n %{modules} -- %{_libdir}/gtk-%{api}/%{binary_version}/immodules/*.so
%{_libdir}/gtk-%{api}/bin/gtk-query-immodules-%{api} > %{_sysconfdir}/gtk-%{api}/gtk.immodules.%{_lib}

%triggerpostun -n %{modules} -- %{_libdir}/gtk-%{api}/%{binary_version}/immodules/*.so
if [ -x %{_libdir}/gtk-%{api}/bin/gtk-query-immodules-%{api} ]; then
    %{_libdir}/gtk-%{api}/bin/gtk-query-immodules-%{api} > %{_sysconfdir}/gtk-%{api}/gtk.immodules.%{_lib}
fi

%files
%{_bindir}/gtk-query-immodules-%{api}
%{_bindir}/gtk-update-icon-cache

%files common -f gtk20.lang
%{_datadir}/themes/
%dir %{_sysconfdir}/gtk-%{api}
%config(noreplace) %{_sysconfdir}/gtk-%{api}/im-multipress.conf

%files -n %{modules}
%ghost %verify (not md5 mtime size) %config(noreplace) %{_sysconfdir}/gtk-%{api}/gtk.immodules.%{_lib}
%dir %{_libdir}/gtk-%{api}
%dir %{_libdir}/gtk-%{api}/bin
%{_libdir}/gtk-%{api}/bin/gtk-query-immodules-%{api}
%dir %{_libdir}/gtk-%{api}/modules
%dir %{_libdir}/gtk-%{api}/%{binary_version}
%dir %{_libdir}/gtk-%{api}/%{binary_version}/immodules
%dir %{_libdir}/gtk-%{api}/%{binary_version}/engines
%dir %{_libdir}/gtk-%{api}/%{binary_version}/printbackends
%{_libdir}/gtk-%{api}/%{binary_version}/immodules/*.so
%{_libdir}/gtk-%{api}/%{binary_version}/engines/*.so
%{_libdir}/gtk-%{api}/%{binary_version}/printbackends/*.so
# from gail lib
%{_libdir}/gtk-2.0/modules/libferret.so
%{_libdir}/gtk-2.0/modules/libgail.so

%files -n %{libgdk}
%{_libdir}/libgdk-x11-%{api}.so.%{major}*

%files -n %{libgtk}
%{_libdir}/libgtk-x11-%{api}.so.%{major}*

%files -n %{girgdk}
%{_libdir}/girepository-1.0/Gdk-%{api}.typelib

%files -n %{girgdkx11}
%{_libdir}/girepository-1.0/GdkX11-%{api}.typelib

%files -n %{girname}
%{_libdir}/girepository-1.0/Gtk-%{api}.typelib

%files -n %{devname}
%doc docs/*.txt AUTHORS NEWS README*
%doc %{_datadir}/gtk-doc/html/gdk2/
%doc %{_datadir}/gtk-doc/html/gtk2/
%{_bindir}/gtk-demo
%{_bindir}/gtk-builder-convert
%{_datadir}/aclocal/*
%{_datadir}/gtk-%{api}/
%{_includedir}/gtk-unix-print-%{api}/
%dir %{_includedir}/gtk-%{api}
%{_includedir}/gtk-%{api}/gdk
%{_includedir}/gtk-%{api}/gtk
%{_libdir}/gtk-%{api}/include
%{_libdir}/pkgconfig/gdk-%{api}.pc
%{_libdir}/pkgconfig/gtk+-%{api}.pc
%{_libdir}/pkgconfig/gtk+-unix-print-%{api}.pc
%{_libdir}/libgdk-x11-%{api}.so
%{_libdir}/libgtk-x11-%{api}.so
%{_datadir}/gir-1.0/Gdk-2.0.gir
%{_datadir}/gir-1.0/GdkX11-2.0.gir
%{_datadir}/gir-1.0/Gtk-2.0.gir
%{_libdir}/pkgconfig/*x11*

%files -n %{libgail}
%{_libdir}/libgailutil.so.%{gail_major}*

%files -n %{devgail}
%doc %{_datadir}/gtk-doc/html/gail-libgail-util
%{_libdir}/libgailutil.so
%{_includedir}/gail-1.0/
%{_libdir}/pkgconfig/gail.pc
