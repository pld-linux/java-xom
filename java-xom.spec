#
# Conditional build:
%bcond_with	javadoc		# don't build javadoc
%bcond_without	tests		# don't build and run tests

%define		srcname	xom
%define		jaxenver 1.1.1
Summary:	Yet another API for processing XML
Name:		java-xom
Version:	1.1
Release:	4
License:	LGPL v2.1, BSD-like
Group:		Libraries/Java
Source0:	http://www.cafeconleche.org/XOM/xom-%{version}-src.tar.gz
# Source0-md5:	e5ae82568d7b1faeb950140c34fbbcb1
Source1:	http://dist.codehaus.org/jaxen/distributions/jaxen-%{jaxenver}-src.tar.gz
# Source1-md5:	b598ae6b7e765a92e13667b0a80392f4
Patch0:		%{name}-jaxen-build.patch
URL:		http://www.cafeconleche.org/XOM/
BuildRequires:	ant
BuildRequires:	java-junit
BuildRequires:	java-xalan
BuildRequires:	java-xerces
BuildRequires:	java-xml-commons-external
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
XOM is an open source, tree-based API for processing XML with Java
that strives for correctness, simplicity, and performance, in that
order.

%package javadoc
Summary:	Online manual for XOM
Summary(pl.UTF-8):	Dokumentacja online do XOM
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Documentation for XOM.

%description javadoc -l pl.UTF-8
Dokumentacja do XOM.

%description javadoc -l fr.UTF-8
Javadoc pour XOM.

%package examples
Summary:	Examples for XOM
Summary(pl.UTF-8):	Przykłady dla pakietu XOM
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description examples
Demonstrations and samples for %{srcname}.

%description examples -l pl.UTF-8
Pliki demonstracyjne i przykłady dla pakietu %{srcname}.

%prep
%setup -q -n XOM -a1
%patch -P0 -p1

install -d build
mv jaxen-%{jaxenver} build/jaxen

cat > build.properties << EOF
xml-apis.jar=$(find-jar xml-apis)
parser.jar=$(find-jar xerces-j2)
serializer.jar=$(find-jar serializer)
xslt.jar=$(find-jar xalan.jar)
junit.jar=$(find-jar junit.jar)
EOF

# do not allow empty jars
grep '=$' build.properties && exit 1

# We do not need these jars. We want to use system libs.
find -name '*.jar' | xargs rm -v

%build
ANT_OPTS=-Xss64M %ant -propertyfile build.properties minimal jar
%if %{with javadoc}
%ant javadoc
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

# jars
cp -a build/%{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

cp -a build/%{srcname}-%{version}-minimal.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-minimal-%{version}.jar
ln -s %{srcname}-minimal-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-minimal.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a build/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

# examples
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{srcname}-%{version}/nu/xom/samples/
cp -a src/nu/xom/samples/* $RPM_BUILD_ROOT%{_examplesdir}/%{srcname}-%{version}/nu/xom/samples/

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%doc README.txt Todo.txt
%{_javadir}/*.jar

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{srcname}-%{version}

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
