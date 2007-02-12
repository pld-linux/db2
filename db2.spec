Summary:	BSD database library for C
Summary(pl.UTF-8):   Biblioteka bazodanowa z BSD dla C
Name:		db2
Version:	2.4.14
Release:	8
Group:		Libraries
License:	BSD
# alternative site (sometimes working): http://www.berkeleydb.com/
# Source0Download: http://dev.sleepycat.com/downloads/releasehistorybdb.html
# Source0:	http://downloads.sleepycat.com/db-2.7.7.tar.gz
# Taken from glibc 2.1.3
Source0:	%{name}-glibc-2.1.3.tar.gz
# Source0-md5:	6e48a57b362f2324831a1751c618c875
# Patch to make it standalone
Patch0:		%{name}-glibc-2.1.3.patch
Patch1:		%{name}-libdb2.patch
URL:		http://www.sleepycat.com/
BuildConflicts:	glibc-db2
Obsoletes:	glibc-db2
Conflicts:	glibc < 2.1.90
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This library used to be part of the glibc
package.

%description -l pl.UTF-8
Berkeley Database (Berkeley DB) to zestaw narzędzi programistycznych
zapewniających obsługę baz danych w aplikacjach tradycyjnych jak i
klient-serwer. Ta biblioteka była częścią glibc.

%package devel
Summary:	Header files for Berkeley database library
Summary(pl.UTF-8):   Pliki nagłówkowe do biblioteki Berkeley Database
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	glibc-db2-devel
Conflicts:	glibc-devel < 2.1.90

%description devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. Berkeley DB includes B tree, Hashing,
Fixed and Variable-length record access methods.

This package contains the header files, and documentation for building
programs which use Berkeley DB.

%description devel -l pl.UTF-8
Berkeley Database (Berkeley DB) to zestaw narzędzi programistycznych
zapewniających obsługę baz danych w aplikacjach tradycyjnych jak i
klient-serwer. Berkeley DB obsługuje dostęp do bazy przez B-drzewa i
funkcje mieszające ze stałą lub zmienną wielkością rekordu.

Ten pakiet zawiera pliki nagłówkowe i dokumentację do budowania
programów używających Berkeley DB.

%package static
Summary:	Static libraries for Berkeley database library
Summary(pl.UTF-8):   Statyczne biblioteki Berkeley Database
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	glibc-db2-static
Conflicts:	glibc-static < 2.1.90

%description static
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. Berkeley DB includes B tree, Hashing,
Fixed and Variable-length record access methods.

This package contains the static libraries for building programs which
use Berkeley DB.

%description static -l pl.UTF-8
Berkeley Database (Berkeley DB) to zestaw narzędzi programistycznych
zapewniających obsługę baz danych w aplikacjach tradycyjnych jak i
klient-serwer. Berkeley DB obsługuje dostęp do bazy przez B-drzewa i
funkcje mieszające ze stałą lub zmienną wielkością rekordu.

Ten pakiet zawiera statyczne biblioteki do budowania programów
używających Berkeley DB.

%prep
%setup -q -n db2
%patch0 -p1
%patch1 -p1

%build
%{__make} \
	CFLAGS="%{rpmcflags} -I. -I./include -include ./compat.h"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir}/db2,%{_libdir},%{_bindir}}

install libdb2.so.3 $RPM_BUILD_ROOT%{_libdir}
install libdb2.a $RPM_BUILD_ROOT%{_libdir}
install db.h db_185.h $RPM_BUILD_ROOT%{_includedir}/db2

for p in db_archive db_checkpoint db_deadlock db_dump db_load \
	db_printlog db_recover db_stat; do
	q="`echo $p | sed -e 's,^db_,db2_,'`"
		install $p $RPM_BUILD_ROOT%{_bindir}/$q
done

ln -sf libdb2.so.3 $RPM_BUILD_ROOT%{_libdir}/libdb2.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README LICENSE
%attr(755,root,root) %{_libdir}/libdb2.so.3

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/db2_archive
%attr(755,root,root) %{_bindir}/db2_checkpoint
%attr(755,root,root) %{_bindir}/db2_deadlock
%attr(755,root,root) %{_bindir}/db2_dump
%attr(755,root,root) %{_bindir}/db2_load
%attr(755,root,root) %{_bindir}/db2_printlog
%attr(755,root,root) %{_bindir}/db2_recover
%attr(755,root,root) %{_bindir}/db2_stat
%attr(755,root,root) %{_libdir}/libdb2.so
%dir %{_includedir}/db2
%{_includedir}/db2/db.h
%{_includedir}/db2/db_185.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libdb2.a
