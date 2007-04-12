%define name	ical
%define version	2.3.2
%define release	%mkrel 1

Summary:	An X Window System-based calendar program
Name:		%{name}
Version:	%{version}
Release:	%{release}

Source0:	http://www.annexia.org/_file/%{name}-%{version}.tar.bz2
Source1:	ical-icons.tar.bz2
Patch4:		ical-2.2-no-locincpth.patch
Patch5:		ical-2.2-duplicates.patch
Patch6:		ical-2.2-alarm-arrow.patch
Patch7:		ical-2.2-autoflags.patch

Url:		http://www.annexia.org/freeware/ical/
License:	BSD-Style
Group:		Office
BuildRequires:	tk tk-devel tcl tcl-devel XFree86-devel autoconf2.5
Requires:       tcl tk
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Ical is an X Window System based calendar program. Ical will easily
create/edit/delete entries, create repeating entries, remind you about
upcoming appointments, print and list item occurrences, and allow
shared calendars between different users.

%prep
%setup -q
%patch4 -p1 -b .no-locincpth
%patch5 -p1 -b .duplicates
%patch6 -p1 -b .alarm-arrow
%patch7 -p1 -b .autoflags
autoconf
# FIXME: make it lib64 aware, better fix tcl/tk for 9.2
perl -pi -e "/(TCL|TK)_EXEC_PREFIX/ and s|/lib\b|/%{_lib}|g" configure

cd types
autoconf
cd -

%build
# FIXME: get it right for 9.2
%configure2_5x --with-tclsh=%{_bindir}/tclsh --with-tclconfig=%{_libdir} 
%make

%install
rm -rf $RPM_BUILD_ROOT
#mkdir -p $RPM_BUILD_ROOT/etc/X11/wmconfig
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1

%makeinstall
install -m644 doc/ical.man $RPM_BUILD_ROOT%{_mandir}/man1/ical.1

#install menu
install -d $RPM_BUILD_ROOT%{_menudir}
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(ical): needs="X11" icon="ical.png" section="Office/Time Management" \
title="Ical" longtitle="Calendar program" command="%{_bindir}/ical" \
xdg="true"
EOF

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{name}
Comment=An X Window System-based calendar program
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-Office-TimeManagement;Office;Calendar;
Encoding=UTF-8
EOF

#mdk icons
install -d $RPM_BUILD_ROOT%{_iconsdir}
tar jxvf %{SOURCE1} -C $RPM_BUILD_ROOT%{_iconsdir}

#nuke unpackaged files
rm -f $RPM_BUILD_ROOT%{_prefix}/man/man1/ical.1

%post
## menu
%update_menus

%postun
## menu
%clean_menus

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc doc/ical.html doc/ical.doc 
%doc doc/interface.html doc/interface.doc
%{_bindir}/ical*
%{_mandir}/man1/ical.1*
%{_prefix}/lib/ical
%{_menudir}/ical
%{_iconsdir}/*.png
%{_liconsdir}/*.png
%{_miconsdir}/*.png
%{_datadir}/applications/mandriva-%{name}.desktop


