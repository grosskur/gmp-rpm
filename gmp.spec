%define configure  CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ; CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ; FFLAGS="${FFLAGS:-%optflags}" ; export FFLAGS ; ./configure %{_target_platform}  --prefix=%{_prefix} --exec-prefix=%{_exec_prefix} --bindir=%{_bindir} --datadir=%{_datadir}  --libdir=%{_libdir} --mandir=%{_mandir}  --infodir=%{_infodir}

Summary: A GNU arbitrary precision library.
Name: gmp
Version: 4.1
Release: 3
URL: http://www.gnu.org/
Source: ftp://ftp.gnu.org/pub/gnu/gmp/gmp-%{version}.tar.bz2
Patch: gmp-4.0.1-s390.patch
Copyright: LGPL 
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
The gmp package contains GNU MP, a library for arbitrary precision
arithmetic, signed integers operations, rational numbers and floating
point numbers. GNU MP is designed for speed, for both small and very
large operands. GNU MP is fast because it uses fullwords as the basic
arithmetic type, it uses fast algorithms, it carefully optimizes
assembly code for many CPUs' most common inner loops, and it generally
emphasizes speed over simplicity/elegance in its operations.

Install the gmp package if you need a fast arbitrary precision
library.

%package devel
Summary: Development tools for the GNU MP arbitrary precision library.
Group: Development/Libraries
Requires: %{name} = %{version}
PreReq: /sbin/install-info

%description devel
The static libraries, header files and documentation for using the GNU
MP arbitrary precision library in applications.

If you want to develop applications which will use the GNU MP library,
you'll need to install the gmp-devel package.  You'll also need to
install the gmp package.

%prep
%setup -q
%patch -p1

%build
%configure --enable-mpbsd
make

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
%{makeinstall}
install -m 644 gmp-mparam.h ${RPM_BUILD_ROOT}%{_includedir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
/sbin/install-info %{_infodir}/gmp.info.gz %{_infodir}/dir

%preun devel
if [ "$1" = 0 ]; then
	/sbin/install-info --delete %{_infodir}/gmp.info.gz %{_infodir}/dir
fi

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYING NEWS README
%{_libdir}/libgmp.so.*
%{_libdir}/libmp.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/libmp.so
%{_libdir}/libgmp.so
%{_libdir}/libmp.a
%{_libdir}/libgmp.a
%{_includedir}/mp.h
%{_includedir}/gmp.h
%{_includedir}/gmp-mparam.h
%{_infodir}/gmp.info*

%changelog
* Mon Jul  8 2002 Trond Eivind Glomsrød <teg@redhat.com> 4.1-3
- Redefine the configure macro, the included configure 
  script isn't happy about the rpm default one (#68190). Also, make
  sure the included libtool isn't replaced,

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sat May 25 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to version 4.1
- patch s390 gmp-mparam.h to match other archs.

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Mar 11 2002 Trond Eivind Glomsrød <teg@redhat.com> 4.0.1-3
- Use standard %%configure macro and edit %%{_tmppath}

* Tue Feb 26 2002 Trond Eivind Glomsrød <teg@redhat.com> 4.0.1-2
- Rebuild

* Tue Jan 22 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 4.0.1
- bzip2 src

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Mon Feb 05 2001 Philipp Knirsch <pknirsch@redhat.de>
- Fixed bugzilla bug #25515 where GMP wouldn't work on IA64 as IA64 is not
correctly identified as a 64 bit platform.

* Mon Dec 18 2000 Preston Brown <pbrown@redhat.com>
- include bsd mp library

* Tue Oct 17 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 3.1.1

* Sun Sep  3 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- update to 3.1

* Sat Aug 19 2000 Preston Brown <pbrown@redhat.com>
- devel subpackage depends on main package so that .so symlink is OK.

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat Jun  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- switch to the configure and makeinstall macros
- FHS-compliance fixing
- move docs to non-devel package

* Fri Apr 28 2000 Bill Nottingham <notting@redhat.com>
- libtoolize for ia64

* Fri Apr 28 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- update to 3.0.1

* Thu Apr 27 2000 Jakub Jelinek <jakub@redhat.com>
- sparc64 fixes for 3.0

* Wed Apr 26 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- update to 3.0

* Mon Feb 14 2000 Matt Wilson <msw@redhat.com>
- #include <string.h> in files that use string functions

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix description and summary

* Mon Dec 06 1999 Michael K. Johnson <johnsonm@redhat.com>
- s/GPL/LGPL/
- build as non-root (#7604)

* Mon Sep 06 1999 Jakub Jelinek <jj@ultra.linux.cz>
- merge in some debian gmp fixes
- Ulrich Drepper's __gmp_scale2 fix
- my mpf_set_q fix
- sparc64 fixes

* Wed Apr 28 1999 Cristian Gafton <gafton@redhat.com>
- add sparc patch for PIC handling

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 8)

* Thu Feb 11 1999 Michael Johnson <johnsonm@redhat.com>
- include the private header file gmp-mparam.h because several
  apps seem to assume that they are building against the gmp
  source tree and require it.  Sigh.

* Tue Jan 12 1999 Michael K. Johnson <johnsonm@redhat.com>
- libtoolize to work on arm

* Thu Sep 10 1998 Cristian Gafton <gafton@redhat.com>
- yet another touch of the spec file

* Wed Sep  2 1998 Michael Fulbright <msf@redhat.com>
- looked over before inclusion in RH 5.2

* Sat May 24 1998 Dick Porter <dick@cymru.net>
- Patch Makefile.in, not Makefile
- Don't specify i586, let configure decide the arch

* Sat Jan 24 1998 Marc Ewing <marc@redhat.com>
- started with package from Toshio Kuratomi <toshiok@cats.ucsc.edu>
- cleaned up file list
- fixed up install-info support

