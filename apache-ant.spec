Name     : apache-ant
Version  : 1.9.7
Release  : 5
URL      : http://apache.spinellicreations.com//ant/source/apache-ant-1.9.7-src.tar.gz
Source0  : http://apache.spinellicreations.com//ant/source/apache-ant-1.9.7-src.tar.gz
Summary  : No detailed summary available
Group    : Development/Tools
License  : Apache-2.0
BuildRequires: openjdk-dev openjdk
Buildrequires: apache-ant
Buildrequires: python3
Buildrequires: six
Buildrequires: lxml
Buildrequires: javapackages-tools

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

# Create ant directory
mkdir -p %{buildroot}/usr/bin
install -d -m 755 %{buildroot}/usr/share/java/ant
install -d -m 755 %{buildroot}/usr/share/maven-poms
install -d -m 755 %{buildroot}/usr/share/maven-metadata

# Remove unnecesary poms
rm %{buildroot}/usr/share/ant/lib/*.pom

# Symlinks to binaries
ln -s ../share/ant/bin/ant %{buildroot}/usr/bin/ant
ln -s ../share/ant/bin/antRun %{buildroot}/usr/bin/antRun

find -name build.xml -o -name pom.xml | xargs sed -i -e s/-SNAPSHOT//

for jar in build/lib/*.jar
do
    jarname=$(basename $jar .jar)
    pomname="JPP.ant-${jarname}.pom"

    # Install jars
    install -m 644 ${jar} %{buildroot}/usr/share/java/ant/${jarname}.jar
    ln -sf ../../java/ant/${jarname}.jar %{buildroot}/usr/share/ant/lib/${jarname}.jar

    # add backward compatibility for nodeps jar that is now part of main jar
    alias=
    [ $jarname == ant ] && alias=org.apache.ant:ant-nodeps,apache:ant,ant:ant
    [ $jarname == ant-launcher ] && alias=ant:ant-launcher

    # Install poms
    [ $jarname == ant-bootstrap ] && continue
    install -p -m 644 src/etc/poms/${jarname}/pom.xml %{buildroot}/usr/share/maven-poms/${pomname}

    python3 /usr/share/java-utils/maven_depmap.py \
    -n "" \
    --pom-base %{buildroot}/usr/share/maven-poms \
    --jar-base "%{buildroot}/usr/share/java" \
    %{buildroot}/usr/share/maven-metadata/ant-${jarname/ant-/}.xml \
    %{buildroot}/usr/share/maven-poms/${pomname} \
    %{buildroot}/usr/share/java/ant/${jarname}.jar \

done

for mod in ant ant-bootstrap ant-launcher; do
    ln -sf ant/${mod}.jar $RPM_BUILD_ROOT/usr/share/java
done

# ant-parent pom
install -p -m 644 src/etc/poms/pom.xml %{buildroot}/usr/share/maven-poms/JPP-ant-parent.pom

python3 /usr/share/java-utils/maven_depmap.py \
    -n "" \
    --pom-base %{buildroot}/usr/share/maven-poms \
    --jar-base "%{buildroot}/usr/share/java" \
    %{buildroot}/usr/share/maven-metadata/ant.xml \
    %{buildroot}/usr/share/maven-poms/JPP-ant-parent.pom

%files
%defattr(-,root,root,-)
/usr/bin/ant
/usr/bin/antRun
/usr/share/ant/bin/ant
/usr/share/ant/bin/antRun
/usr/share/maven-metadata/ant.xml
/usr/share/maven-poms/JPP-ant-parent.pom
/usr/share/ant/lib/ant-antlr.jar
/usr/share/ant/lib/ant-apache-bcel.jar
/usr/share/ant/lib/ant-apache-bsf.jar
/usr/share/ant/lib/ant-apache-log4j.jar
/usr/share/ant/lib/ant-apache-oro.jar
/usr/share/ant/lib/ant-apache-regexp.jar
/usr/share/ant/lib/ant-apache-resolver.jar
/usr/share/ant/lib/ant-apache-xalan2.jar
/usr/share/ant/lib/ant-bootstrap.jar
/usr/share/ant/lib/ant-commons-logging.jar
/usr/share/ant/lib/ant-commons-net.jar
/usr/share/ant/lib/ant-jai.jar
/usr/share/ant/lib/ant-javamail.jar
/usr/share/ant/lib/ant-jdepend.jar
/usr/share/ant/lib/ant-jmf.jar
/usr/share/ant/lib/ant-jsch.jar
/usr/share/ant/lib/ant-junit.jar
/usr/share/ant/lib/ant-junit4.jar
/usr/share/ant/lib/ant-launcher.jar
/usr/share/ant/lib/ant-netrexx.jar
/usr/share/ant/lib/ant-swing.jar
/usr/share/ant/lib/ant-testutil.jar
/usr/share/ant/lib/ant.jar
/usr/share/java/ant/ant-antlr.jar
/usr/share/java/ant/ant-apache-bcel.jar
/usr/share/java/ant/ant-apache-bsf.jar
/usr/share/java/ant/ant-apache-log4j.jar
/usr/share/java/ant/ant-apache-oro.jar
/usr/share/java/ant/ant-apache-regexp.jar
/usr/share/java/ant/ant-apache-resolver.jar
/usr/share/java/ant/ant-apache-xalan2.jar
/usr/share/java/ant/ant-bootstrap.jar
/usr/share/java/ant/ant-commons-logging.jar
/usr/share/java/ant/ant-commons-net.jar
/usr/share/java/ant/ant-jai.jar
/usr/share/java/ant/ant-javamail.jar
/usr/share/java/ant/ant-jdepend.jar
/usr/share/java/ant/ant-jmf.jar
/usr/share/java/ant/ant-jsch.jar
/usr/share/java/ant/ant-junit.jar
/usr/share/java/ant/ant-junit4.jar
/usr/share/java/ant/ant-launcher.jar
/usr/share/java/ant/ant-netrexx.jar
/usr/share/java/ant/ant-swing.jar
/usr/share/java/ant/ant-testutil.jar
/usr/share/java/ant/ant.jar
/usr/share/java/ant-bootstrap.jar
/usr/share/java/ant-launcher.jar
/usr/share/java/ant.jar
/usr/share/maven-metadata/ant-ant.xml
/usr/share/maven-metadata/ant-antlr.xml
/usr/share/maven-metadata/ant-apache-bcel.xml
/usr/share/maven-metadata/ant-apache-bsf.xml
/usr/share/maven-metadata/ant-apache-log4j.xml
/usr/share/maven-metadata/ant-apache-oro.xml
/usr/share/maven-metadata/ant-apache-regexp.xml
/usr/share/maven-metadata/ant-apache-resolver.xml
/usr/share/maven-metadata/ant-apache-xalan2.xml
/usr/share/maven-metadata/ant-commons-logging.xml
/usr/share/maven-metadata/ant-commons-net.xml
/usr/share/maven-metadata/ant-jai.xml
/usr/share/maven-metadata/ant-javamail.xml
/usr/share/maven-metadata/ant-jdepend.xml
/usr/share/maven-metadata/ant-jmf.xml
/usr/share/maven-metadata/ant-jsch.xml
/usr/share/maven-metadata/ant-junit.xml
/usr/share/maven-metadata/ant-junit4.xml
/usr/share/maven-metadata/ant-launcher.xml
/usr/share/maven-metadata/ant-netrexx.xml
/usr/share/maven-metadata/ant-swing.xml
/usr/share/maven-metadata/ant-testutil.xml
/usr/share/maven-poms/JPP.ant-ant-antlr.pom
/usr/share/maven-poms/JPP.ant-ant-apache-bcel.pom
/usr/share/maven-poms/JPP.ant-ant-apache-bsf.pom
/usr/share/maven-poms/JPP.ant-ant-apache-log4j.pom
/usr/share/maven-poms/JPP.ant-ant-apache-oro.pom
/usr/share/maven-poms/JPP.ant-ant-apache-regexp.pom
/usr/share/maven-poms/JPP.ant-ant-apache-resolver.pom
/usr/share/maven-poms/JPP.ant-ant-apache-xalan2.pom
/usr/share/maven-poms/JPP.ant-ant-commons-logging.pom
/usr/share/maven-poms/JPP.ant-ant-commons-net.pom
/usr/share/maven-poms/JPP.ant-ant-jai.pom
/usr/share/maven-poms/JPP.ant-ant-javamail.pom
/usr/share/maven-poms/JPP.ant-ant-jdepend.pom
/usr/share/maven-poms/JPP.ant-ant-jmf.pom
/usr/share/maven-poms/JPP.ant-ant-jsch.pom
/usr/share/maven-poms/JPP.ant-ant-junit.pom
/usr/share/maven-poms/JPP.ant-ant-junit4.pom
/usr/share/maven-poms/JPP.ant-ant-launcher.pom
/usr/share/maven-poms/JPP.ant-ant-netrexx.pom
/usr/share/maven-poms/JPP.ant-ant-swing.pom
/usr/share/maven-poms/JPP.ant-ant-testutil.pom
/usr/share/maven-poms/JPP.ant-ant.pom
/usr/share/ant/manual/*
/usr/share/ant/CONTRIBUTORS
/usr/share/ant/INSTALL
/usr/share/ant/KEYS
/usr/share/ant/LICENSE
/usr/share/ant/NOTICE
/usr/share/ant/README
/usr/share/ant/WHATSNEW
/usr/share/ant/bin/ant.bat
/usr/share/ant/bin/ant.cmd
/usr/share/ant/bin/antRun.bat
/usr/share/ant/bin/antRun.pl
/usr/share/ant/bin/antenv.cmd
/usr/share/ant/bin/complete-ant-cmd.pl
/usr/share/ant/bin/envset.cmd
/usr/share/ant/bin/lcp.bat
/usr/share/ant/bin/runant.pl
/usr/share/ant/bin/runant.py
/usr/share/ant/bin/runrc.cmd
/usr/share/ant/contributors.xml
/usr/share/ant/etc/ant-bootstrap.jar
/usr/share/ant/etc/changelog.xsl
/usr/share/ant/etc/checkstyle/checkstyle-frames-sortby-check.xsl
/usr/share/ant/etc/checkstyle/checkstyle-frames.xsl
/usr/share/ant/etc/checkstyle/checkstyle-text.xsl
/usr/share/ant/etc/checkstyle/checkstyle-xdoc.xsl
/usr/share/ant/etc/coverage-frames.xsl
/usr/share/ant/etc/jdepend-frames.xsl
/usr/share/ant/etc/jdepend.xsl
/usr/share/ant/etc/junit-frames-xalan1.xsl
/usr/share/ant/etc/junit-frames.xsl
/usr/share/ant/etc/junit-noframes.xsl
/usr/share/ant/etc/log.xsl
/usr/share/ant/etc/maudit-frames.xsl
/usr/share/ant/etc/mmetrics-frames.xsl
/usr/share/ant/etc/tagdiff.xsl
/usr/share/ant/fetch.xml
/usr/share/ant/get-m2.xml
/usr/share/ant/lib/README
/usr/share/ant/lib/libraries.properties
/usr/share/ant/patch.xml
