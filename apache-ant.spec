Name     : apache-ant
Version  : 1.9.7
Release  : 1
URL      : http://apache.spinellicreations.com//ant/source/apache-ant-1.9.7-src.tar.gz
Source0  : http://apache.spinellicreations.com//ant/source/apache-ant-1.9.7-src.tar.gz
Summary  : No detailed summary available
Group    : Development/Tools
License  : Apache-2.0
BuildRequires: openjdk-dev openjdk

%description
A     N     T
What is it?
-----------

Ant is a Java based build tool. In theory it is kind of like "make"
without makes wrinkles and with the full portability of pure java code.

%prep
%setup -q -n apache-ant-1.9.7

%build
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk/
mkdir dist
sh build.sh -Ddist.dir=dist dist

%install
rm -rf %{buildroot}
export ANT_HOME=%{buildroot}/usr/share/ant
sh build.sh install
mkdir -p %{buildroot}/usr/bin
ln -s ../share/ant/bin/ant %{buildroot}/usr/bin/ant


%files
%defattr(-,root,root,-)
/usr/bin/ant
/usr/share/ant
