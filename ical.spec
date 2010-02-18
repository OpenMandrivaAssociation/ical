Summary:	An X Window System-based calendar program
Name:		ical
Version:	2.3.3
Release:	%{mkrel 2}

Source0:	http://www.annexia.org/_file/%{name}-%{version}.tar.gz
Source1:	ical-icons.tar.bz2
Patch0:		ical-2.3.3-no-locincpth.patch
Patch1:		ical-2.2-duplicates.patch
Patch2:		ical-2.2-alarm-arrow.patch
Patch3:		ical-2.2-autoflags.patch
Patch4:		ical-2.3.3-tcl_relocate.patch
Patch5:		ical-2.3.3-tcl8.6.patch
# Fix use of variable names of the style foo(done): recent Tcl versions
# reject this with error "upvar won't create a scalar variable that
# looks like an array element" - AdamW 2008/10
Patch6:		ical-2.3.3-varnames.patch
Patch7:		ical-2.3.3-gcc4.4.patch

URL:		http://www.annexia.org/freeware/ical/
License:	BSD-like
Group:		Office
BuildRequires:	tk
BuildRequires:	tk-devel
BuildRequires:	tcl
BuildRequires:	tcl-devel
BuildRequires:	X11-devel
BuildRequires:	autoconf
Requires:	tcl
Requires:	tk
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Ical is an X Window System based calendar program. Ical will easily
create/edit/delete entries, create repeating entries, remind you about
upcoming appointments, print and list item occurrences, and allow
shared calendars between different users.

%prep
%setup -q
%patch0 -p1 -b .no-locincpth
%patch1 -p1 -b .duplicates
%patch2 -p1 -b .alarm-arrow
%patch3 -p1 -b .autoflags
%patch4 -p1 -b .tcl_relocate
%patch5 -p1 -b .tcl86
%patch6 -p1 -b .varnames
%patch7 -p0 -b .gcc

%build
autoreconf
pushd types
autoconf
popd

%configure2_5x --with-tclsh=%{_bindir}/tclsh --with-tclconfig=%{_libdir} --with-tclscripts=%{tcl_sitelib} --with-tkscripts=%{_datadir}/tk%{tcl_version}
%make CXXLINKER="g++ %{ldflags}"

%install
rm -rf %{buildroot}
#mkdir -p %{buildroot}/etc/X11/wmconfig
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_prefix}/lib
mkdir -p %{buildroot}%{_mandir}/man1

%makeinstall
install -m644 doc/ical.man %{buildroot}%{_mandir}/man1/ical.1

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{name}
Comment=An X Window System-based calendar program
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Office;Calendar;
EOF

#mdk icons
install -d %{buildroot}%{_iconsdir}
tar jxvf %{SOURCE1} -C %{buildroot}%{_iconsdir}

#nuke unpackaged files
rm -f %{buildroot}%{_prefix}/man/man1/ical.1

%if %mdkversion < 200900
%post
%update_menus
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%clean_icon_cache hicolor
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYRIGHT ANNOUNCE CHANGES.html README TODO
%doc doc/ical.html doc/ical.doc
%doc doc/interface.html doc/interface.doc
%{_bindir}/ical*
%{_mandir}/man1/ical.1*
%{_prefix}/lib/ical
%{tcl_sitelib}/%{name}
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/applications/mandriva-%{name}.desktop

