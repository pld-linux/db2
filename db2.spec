Summary:	BSD database library for C
Name:		db2
Version:	2.4.14
Release:	6
Group:		Libraries
Group(de):	Libraries
Group(fr):	Librairies
Group(pl):	Biblioteki
License:	BSD
URL:		http://www.sleepycat.com
# Source0:	http://www.sleepycat.com/update/2.7.7/db-2.7.7.tar.gz
# Taken from glibc 2.1.3
Source0:	%{name}-glibc-2.1.3.tar.gz
# Patch to make it standalone
Patch0:		%{name}-glibc-2.1.3.patch
Patch1:		%{name}-libdb2.patch
PreReq:		/sbin/ldconfig
Conflicts:	glibc < 2.1.90
BuildConflicts:	glibc-db2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	glibc-db2

%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This library used to be part of the glibc
package.

%package devel
Summary:	Development libraries and header files for Berkeley database library
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}
Conflicts:	glibc-devel < 2.1.90
Obsoletes:	glibc-db2-devel

%description devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. Berkeley DB includes B tree, Hashing,
Fixed and Variable-length record access methods.

This package contains the header files, libraries, and documentation
for building programs which use Berkeley DB.

%package static
Summary:	Static libraries for Berkeley database library
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-devel = %{version}
Conflicts:	glibc-static < 2.1.90
Obsoletes:	glibc-db2-static

%description static
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. Berkeley DB includes B tree, Hashing,
Fixed and Variable-length record access methods.

This package contains the static libraries for building programs which
use Berkeley DB.

%prep
%setup -q -n db2
%patch0 -p1
%patch1 -p1

%build
%{__make} CFLAGS="%{?debug:-O0 -g}%{!?debug:$RPM_OPT_FLAGS} -I. -I./include -include ./compat.h"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/lib,%{_includedir}/db2,%{_libdir},%{_bindir}}

install libdb2.so.3 $RPM_BUILD_ROOT/lib/
install libdb2.a $RPM_BUILD_ROOT%{_libdir}
install db.h db_185.h $RPM_BUILD_ROOT%{_includedir}/db2

for p in db_archive db_checkpoint db_deadlock db_dump db_load \
	db_printlog db_recover db_stat; do
	q="`echo $p | sed -e 's,^db_,db2_,'`"
		install $p $RPM_BUILD_ROOT%{_bindir}/$q
done

ln -sf ../../lib/libdb2.so.3 $RPM_BUILD_ROOT%{_libdir}/libdb2.so

gzip -9nf README LICENSE

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.gz LICENSE.gz
%attr(755,root,root) /lib/libdb2.so.3

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/db2
%{_includedir}/db2/db.h
%{_includedir}/db2/db_185.h
%attr(755,root,root) %{_libdir}/libdb2.so
%attr(755,root,root) %{_bindir}/db2_archive
%attr(755,root,root) %{_bindir}/db2_checkpoint
%attr(755,root,root) %{_bindir}/db2_deadlock
%attr(755,root,root) %{_bindir}/db2_dump
%attr(755,root,root) %{_bindir}/db2_load
%attr(755,root,root) %{_bindir}/db2_printlog
%attr(755,root,root) %{_bindir}/db2_recover
%attr(755,root,root) %{_bindir}/db2_stat

%files static
%defattr(644,root,root,755)
%{_libdir}/libdb2.a
