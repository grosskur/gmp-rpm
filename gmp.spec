#
# Important for %{ix86}:
# This rpm has to be build on a CPU with sse2 support like Pentium 4 !
#

%define configure  CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ; CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ; FFLAGS="${FFLAGS:-%optflags}" ; export FFLAGS ; ./configure %{_target_platform}  --prefix=%{_prefix} --exec-prefix=%{_exec_prefix} --bindir=%{_bindir} --datadir=%{_datadir}  --libdir=%{_libdir} --mandir=%{_mandir}  --infodir=%{_infodir}

Summary: A GNU arbitrary precision library.
Name: gmp
Version: 4.1.3
Release: 1
URL: http://www.swox.com/gmp/
Source: ftp://ftp.gnu.org/pub/gnu/gmp/gmp-%{version}.tar.bz2
Patch0: gmp-4.0.1-s390.patch
Patch1: gmp-4.1.2-ppc64.patch
Patch2: gmp-4.1.2-autoconf.patch
License: LGPL 
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: automake16 autoconf libtool

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
%patch0 -p1
%patch1 -p1
%patch2 -p1

libtoolize --force
aclocal-1.6 -I mpn -I mpfr
automake-1.6
autoconf

%build
if as --help | grep -q execstack; then
  # the object files do not require an executable stack
  export CCAS="gcc -c -Wa,--noexecstack"
fi
mkdir base
cd base
ln -s ../configure .
%configure --enable-mpbsd --enable-mpfr --enable-cxx
perl -pi -e 's|hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=\"-L\\\$libdir\"|g;' libtool
export LD_LIBRARY_PATH=`pwd`/.libs
make %{?_smp_mflags}
cd ..
%ifarch %{ix86}
mkdir build-sse2
cd build-sse2
ln -s ../configure .
CFLAGS="-O2 -g -march=pentium4"
%configure --enable-mpbsd --enable-mpfr --enable-cxx pentium4-redhat-linux
perl -pi -e 's|hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=\"-L\\\$libdir\"|g;' libtool
export LD_LIBRARY_PATH=`pwd`/.libs
make %{?_smp_mflags}
cd ..
%endif

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
cd base
export LD_LIBRARY_PATH=`pwd`/.libs
%{makeinstall}
install -m 644 gmp-mparam.h ${RPM_BUILD_ROOT}%{_includedir}
rm -f $RPM_BUILD_ROOT%{_libdir}/lib{gmp,mp,gmpxx}.la
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}
ln -sf libgmpxx.so.3 $RPM_BUILD_ROOT%{_libdir}/libgmpxx.so
cd ..
%ifarch %{ix86}
cd build-sse2
export LD_LIBRARY_PATH=`pwd`/.libs
mkdir $RPM_BUILD_ROOT%{_libdir}/sse2
install -m 644 .libs/libgmp.so.3.* $RPM_BUILD_ROOT%{_libdir}/sse2
cp -a .libs/libgmp.so.3 $RPM_BUILD_ROOT%{_libdir}/sse2
chmod 644 $RPM_BUILD_ROOT%{_libdir}/sse2/libgmp.so.3
install -m 644 .libs/libgmpxx.so.3.* $RPM_BUILD_ROOT%{_libdir}/sse2
cp -a .libs/libgmpxx.so.3 $RPM_BUILD_ROOT%{_libdir}/sse2
chmod 644 $RPM_BUILD_ROOT%{_libdir}/sse2/libgmpxx.so.3
install -m 644 .libs/libmp.so.3.* $RPM_BUILD_ROOT%{_libdir}/sse2
cp -a .libs/libmp.so.3 $RPM_BUILD_ROOT%{_libdir}/sse2
chmod 644 $RPM_BUILD_ROOT%{_libdir}/sse2/libmp.so.3
cd ..
%endif

%check
cd base
export LD_LIBRARY_PATH=`pwd`/.libs
make %{?_smp_mflags} check
cd ..
%ifarch %{ix86}
cd build-sse2
export LD_LIBRARY_PATH=`pwd`/.libs
make %{?_smp_mflags} check
cd ..
%endif

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
%doc COPYING COPYING.LIB NEWS README
%{_libdir}/libgmp.so.*
%{_libdir}/libmp.so.*
%{_libdir}/libgmpxx.so.*
%ifarch %{ix86}
%{_libdir}/sse2/*
%endif

%files devel
%defattr(-,root,root)
%{_libdir}/libmp.so
%{_libdir}/libgmp.so
%{_libdir}/libgmpxx.so
%{_libdir}/libmp.a
%{_libdir}/libgmp.a
%{_libdir}/libgmpxx.a
%{_libdir}/libmpfr.a
%{_includedir}/*.h
%{_infodir}/gmp.info*
%{_infodir}/mpfr.info*

%changelog
* Mon May 24 2004 Thomas Woerner <twoerner@redhat.com> 4.1.3-1
- new version 4.1.3

* Wed Mar 31 2004 Thomas Woerner <twoerner@redhat.com> 4.1.2-14
- dropped RPATH (#118506)

* Sat Mar 06 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- also build SSE2 DSOs, patch from Ulrich Drepper

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan 29 2004 Thomas Woerner <twoerner@redhat.com> 4.1.2-11
- BuildRequires for automake16

* Mon Dec 01 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- fix symlink to libgmpxx.so.3  #111135
- add patch to factorize.c from gmp homepage

* Thu Oct 23 2003 Joe Orton <jorton@redhat.com> 4.1.2-9
- build with -Wa,--noexecstack

* Thu Oct 23 2003 Joe Orton <jorton@redhat.com> 4.1.2-8
- build assembly code with -Wa,--execstack
- use parallel make
- run tests, and fix C++ therein

* Thu Oct 02 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- enable mpfr  #104395
- enable cxx  #80195
- add COPYING.LIB
- add fixes from gmp web-site
- remove some cruft patches for older libtool releases

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun 03 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- make configure.in work with newer autoconf

* Sun Jun 01 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- do not set extra_functions for s390x  #92001

* Thu Feb 13 2003 Elliot Lee <sopwith@redhat.com> 4.1.2-3
- Add ppc64 patch, accompanied by running auto*

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 01 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 4.1.2

* Tue Dec 03 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 4.1.1
- remove un-necessary patches
- adjust s390/x86_64 patch

* Sun Oct 06 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add s390x patch
- disable current x86-64 support in longlong.h

* Mon Jul  8 2002 Trond Eivind Glomsrød <teg@redhat.com> 4.1-4
- Add 4 patches, among them one for #67918
- Update URL
- s/Copyright/License/

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

