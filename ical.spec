Summary:	An X Window System-based calendar program
Name:		ical
Version:	2.3.3
Release:	5

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



%changelog
* Sat Feb 05 2011 Funda Wang <fwang@mandriva.org> 2.3.3-3mdv2011.0
+ Revision: 636004
- tighten BR

* Thu Feb 18 2010 Funda Wang <fwang@mandriva.org> 2.3.3-2mdv2011.0
+ Revision: 507436
- fix build with gcc 4.4
- rediff locincpth patch

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Fri Dec 05 2008 Adam Williamson <awilliamson@mandriva.org> 2.3.3-1mdv2009.1
+ Revision: 310150
- %%buildroot not $RPM_BUILD_ROOT
- drop some unnecessary old workarounds
- clean requires
- add varnames.patch (fix variable names issue for tcl 8.5 and 8.6)
- add tcl8.6.patch (fix for tcl 8.6)
- add tcl_relocate.patch (install to new locations per policy)
- new release 2.3.3

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 2.3.2-4mdv2009.0
+ Revision: 247149
- rebuild

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 2.3.2-2mdv2008.1
+ Revision: 140756
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - buildrequires X11-devel instead of XFree86-devel

* Mon Oct 01 2007 Adam Williamson <awilliamson@mandriva.org> 2.3.2-2mdv2008.0
+ Revision: 94318
- rebuild against tcl / tk 8.5 (#34293)
- add several doc files
- update ical-icons.tar.bz2 for xdg icon spec
- drop old menu and X-Mandriva category
- correct autoconf buildrequires
- new license policy

  + Thierry Vignaud <tv@mandriva.org>
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'


* Wed Nov 08 2006 Pascal Terjan <pterjan@mandriva.org> 2.3.2-1mdv2007.0
+ Revision: 78512
- XDG menu
- 2.3.2
- New URL
- Dropped old patches
- mkrel
- BuildRequires autoconf
- XDG menu
- Import ical

* Sun Jan 01 2006 Oden Eriksson <oeriksson@mandriva.com> 2.2-33mdk
- rebuilt against soname aware deps (tcl/tk)
- fix deps

* Fri Nov 19 2004 Michael Scherer <misc@mandrake.org> 2.2-32mdk 
- add Requires tcl tk

* Sat Aug 28 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.2-31mdk
- Fix menu

* Fri Jun 04 2004 Montel Laurent <lmontel@mandrakesoft.com> 2.2-30mdk
- Rebuild

* Wed May 05 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.2-29mdk
- fix buildrequires

